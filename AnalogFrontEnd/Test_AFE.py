# Test program for Analog Front-End
import serial
import time

# For GNU/Linux
AFE = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
# For Windows, replace COM with the respective one
#AFE = serial.Serial(COM12, 9600, timeout=2)

# Verify the Serial Port
print(AFE.name)

counter = 0;

while counter <= 20:
    # Read one byte
    line = AFE.readline()
    print(counter)
    print(line)
    counter += 1

# Send a byte to activate the Arduino
print("Activating")
#AFE.write('K'.encode('utf-8'))
AFE.write(b'K')
time.sleep(1)

counter = 0
while counter <= 20:
    # Get ADC value
    AFE.write('A'.encode('utf-8'))
    line = AFE.readline()
    print("ADC: ", line)
    counter += 1
    time.sleep(1)

counter = 0
while counter <= 20:
    # Toggle Brakes
    AFE.write(b'B')
    print(AFE.readline())

    time.sleep(2)
    AFE.write(b'C')
    print(AFE.readline())
    counter += 1

AFE.close()
