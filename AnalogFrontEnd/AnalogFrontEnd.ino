/*  Team 21039: Radio Telescope
    Created 2020.10.22
    
    Arduino for handling Brake Solenoid and analog signal from the Anemometer
    
    Function: ADC analog IN -> pin A0
              Brake Control -> D2
			  On-site E-Stop Sense -> D8

*/

char Command = 0;

float wind = 0.0;

/* Using last 4 bit for Status
	bit 0: Brake Status(0: engaged; 1: released))
	bit 1: E-Stop Tripped(0: reset; 1: set, tripped)
	bit 2: AFE Status(0: disabled; 1: enabled)
	bit 3: Indicator Switch(0: off; 1: on)
*/

volatile unsigned char Status = 0b1000;

void setup() {

	// Upon power up, turn on the LED as Indicator
	pinMode(13, OUTPUT);
	digitalWrite(13, HIGH);

	// Use pin 2 for brake control
	pinMode(2, OUTPUT);
	digitalWrite(2, LOW);

	// Use pin 8 for E-Stop sensing
	pinMode(8, INPUT);
	digitalWrite(8, HIGH);

	// Set the analog reference voltage to default
	pinMode(A0, INPUT);
	analogReference(DEFAULT);

	Serial.setTimeout(100);
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
		Serial.print(wind, 0);
		//Serial.print('\r');

		Status |= 0x0002;
	}

	// 'B' received, activate brakes
	else if ( Command == 'B' ) {

		digitalWrite(2, HIGH);
		digitalWrite(13, HIGH);

		Serial.print("Brakes Engaged\r");

		Status |= 0b0001;
	}

	// 'C' received, deactivate brakes
	else if ( Command == 'C' ) {

		digitalWrite(12, LOW);
		digitalWrite(13, LOW);

		Serial.print("Brakes Released\r");

		Status &= 0b1110;
	}

	//  'E', toggle LED Indicator
	else if ( Command == 'E') {
		Status ^= 0b1000;
	}

	//  'S', return AFE status
	else if ( Command == 'S') {
		Serial.print(String(Status, HEX));
		Serial.print('\r');
	}

	/*
	// Anything else
	else {
		Serial.println(Command);
	}
	*/

	// Clear command
	Command = 0;

	// Wait until data presents
	while ( Serial.available() <= 0 );
	
}

/* Sends a byte to the Serial line every 20ms, until a byte is received */
void WaitingHost() {

	int _temp_ = 0;
	unsigned int _counter_ = 1;

	while ( (Serial.available() <= 0) ) {

		// Sends 10 bytes in 1s interval
		//Serial.print(_counter_);
		//Serial.print(": Waiting\n\r");

		//if ( _counter_ == 0xFFFF ) _counter_ = 1;
		//else ++_counter_;
	}

	// Empty the data
	_temp_ = Serial.read();

	//Serial.print("AFE Active\r");

	Status = 0b1100;
}
