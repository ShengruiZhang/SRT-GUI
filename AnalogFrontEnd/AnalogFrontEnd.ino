/*  Team 21039: Radio Telescope
    Created 2020.10.22
    
    Arduino for handling Brake Solenoid and analog signal from the Anemometer
    
    Function: ADC analog IN -> pin A0
              Brake Control -> TBD (Digital pin)

*/

char Command = 0;

float wind = 0.0;

/* Using last 4 bit for Status
	bit 0: Brake Status
	bit 1: no use
	bit 2: AFE Status
	bit 3: Indicator Switch
*/
//volatile unsigned int Status = 0;
volatile unsigned char Status = 0x0008;

void setup() {

	// Upon power up, turn on the LED as Indicator
	pinMode(13, OUTPUT);
	digitalWrite(13, HIGH);

	// Use pin 12 for brake control
	pinMode(12, OUTPUT);

	digitalWrite(12, LOW);

	// Set the analog reference voltage to default
	pinMode(A0, INPUT);
	analogReference(DEFAULT);

	Serial.setTimeout(2000);
	Serial.begin(57600, SERIAL_8N2);

	// Keep sending a byte to host computer and wait for responds
	WaitingHost();

	// Turn off indicator after a byte is received
	digitalWrite(13, LOW);
}

void loop() {
	// Get a byte from Serial line
	Serial.readBytes(&Command, 1);

	// 'A' received, return ADC value
	if ( Command == 'A' ) {
		wind = map(analogRead(A0), 82, 410, 0, 32.4);
		//Serial.print(String(analogRead(A0), HEX));
		Serial.print(wind);
		Serial.print('\r');
		Status |= 0x0002;
	}

	// 'B' received, activate brakes
	else if ( Command == 'B' ) {
		digitalWrite(12, HIGH);
		digitalWrite(13, HIGH);
		Serial.print("Brakes Engaged\r");
		Status |= 0x0001;
	}

	// 'C' received, deactivate brakes
	else if ( Command == 'C' ) {
		digitalWrite(12, LOW);
		digitalWrite(13, LOW);
		Serial.print("Brakes Released\r");
		Status &= 0x000E;
	}

	//  'E', toggle LED Indicator
	else if ( Command == 'E') {
		Status ^= 0x08;
	}

	//  'S', return AFE status
	else if ( Command == 'S') {
		Serial.print(String(Status, HEX));
		Serial.print('\r');
	}

	// Anything else
	else {
		Serial.println(Command);
	}

	// Clear command
	Command = 0;

	// Wait until data presents
	while ( Serial.available() <= 0 ) {
	}
}

/* Sends a byte to the Serial line every 1s, until a byte is received */
void WaitingHost() {
	int _temp_ = 0;
	unsigned int _counter_ = 1;
	while ( (Serial.available() <= 0) ) {
		// Sends 10 bytes in 1s interval
		Serial.print(_counter_);
		Serial.print(": Waiting\n\r");

		delay(1500);

		if ( _counter_ == 0xFFFF ) _counter_ = 1;
		else ++_counter_;
	}
	// Empty the data
	_temp_ = Serial.read();
	Serial.print("AFE Active\r");
	Status = 0x000C;
}
