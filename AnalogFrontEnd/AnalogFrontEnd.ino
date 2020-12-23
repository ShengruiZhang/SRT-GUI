/*  Team 21039: Radio Telescope
    Created 2020.10.22
    
    Arduino for handling Brake Solenoid and analog signal from the Anemometer
    
    Function: ADC analog IN -> Pin A0
              Brake Control -> TBD (Digital Pin)
*/

char Command = 0;

void setup() {
	// Upon power up, turn on the LED as indicator
	pinMode(13, OUTPUT);
	digitalWrite(13, HIGH);

	// Set Serial timeout = 5s
	Serial.setTimeout(5000);

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
		Serial.println("Return ADC value");
	}
	// 'B' received, activate brakes
	else if ( Command == 'B' ) {
		Serial.println("Engage brakes");
	}
	// 'C' received, deactivate brakes
	else if ( Command == 'C' ) {
		Serial.println("Release brakes");
	}
	else {
		Serial.println("Not valid op.");
	}
	
	// Clear command
	Command = 0;

}

/* Sends a byte to the Serial line every 1s, until a byte is received */
void WaitingHost() {
	while ( (Serial.available() <= 0) ) {
		Serial.println("Waiting...");
		delay(1000);
	}
}
