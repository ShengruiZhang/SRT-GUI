/*  Team 21039: Radio Telescope
    Created 2020.10.22
    
    Arduino for handling Brake Solenoid and analog signal from the Anemometer
    
    Function: ADC analog IN -> Pin A0
              Brake Control -> TBD (Digital Pin)

*/

char Command = 0;

/* Using last 4 bit for Status
	bit 0: Brake Status
	bit 1: no use
	bit 2: AFE Status
	bit 3: Indicator Switch
*/
volatile unsigned int Status = 0;

void setup() {

	Status = 0x0000;

	// Upon power up, turn on the LED as indicator
	pinMode(13, OUTPUT);
	digitalWrite(13, HIGH);

	// Use pin 12 for brake control
	pinMode(12, OUTPUT);
	// Engage brake when power up
	digitalWrite(12, HIGH);
// Set the analog reference voltage to default
	analogReference(DEFAULT);

	// Set Serial timeout = 5s
	Serial.setTimeout(2000);
	// RS-232 Baud rate = 9600
	Serial.begin(9600);

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
		Serial.print(String(analogRead(A0), HEX));
		Serial.print('\n');
		Status |= 0x0002;
	}

	// 'B' received, activate brakes
	else if ( Command == 'B' ) {
		digitalWrite(12, HIGH);
		Serial.print("Brakes Engaged\n");
		Status |= 0x0001;
	}

	// 'C' received, deactivate brakes
	else if ( Command == 'C' ) {
		digitalWrite(12, LOW);
		Serial.print("Brakes Released\n");
		Status &= 0x000E;
	}

	//  'S', return AFE status
	else if ( Command == 'S') {
		Serial.print(String(Status, HEX));
		Serial.print('\n');
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
	while ( (Serial.available() <= 0) ) {
		// Sends 10 bytes in 1s interval
		Serial.print("Waiting Host\n");
		delay(1000);
	}
	// Empty the data
	_temp_ = Serial.read();
	Serial.print("AFE Active\n");
	Status = 0x000C;
}
