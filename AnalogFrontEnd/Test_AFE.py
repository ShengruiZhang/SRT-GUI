# Test program for Analog Front-End
#   Rest the Arduino AFE before running this
#   Argument 1 sets the baud rate

import serial
import time
import sys

print(f"Arguments count: {len(sys.argv)}")
for i, arg in enumerate(sys.argv):
    print(f"Arguments {i:>2}: {arg}")

<<<<<<< HEAD
AFE = serial.Serial('/dev/ttyUSB0', sys.argv[1], timeout=2)
=======
# For GNU/Linux
AFE = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
# For Windows, replace COM with the respective one
#AFE = serial.Serial(COM12, 9600, timeout=2)
>>>>>>> 01773a916c5f6d6848e72683d0b8545099699bd5

# Verify the Serial Port
print(f'Current Serial Port: {AFE.name}')

counter = 0;
while counter < 10:
    # Read one byte
    # The data read from serial is in binary format,
    #   here decode such as ASCII
    line = AFE.readline().decode('ascii')
    print(f'{counter} {line}', end='')
    counter += 1

# Send an arbitrary byte to activate the Arduino
print("Activate AFE...")
#AFE.write('K'.encode('utf-8'))
AFE.write(b'K')
print( AFE.readline().decode('ascii'), end='' )
time.sleep(1)

counter = 0
while counter < 20:
    # Get ADC value
    AFE.write(b'A')
    line = AFE.readline().decode('ascii')
    print(f'ADC: {line}', end='')
    counter += 1
    time.sleep(1)

counter = 0
while counter < 10:
    # Toggle Brakes
    AFE.write(b'B')
    print( AFE.readline().decode('ascii'), end='' )

    time.sleep(2)

    AFE.write(b'C')
    print( AFE.readline().decode('ascii'), end='' )
    counter += 1

AFE.close()
