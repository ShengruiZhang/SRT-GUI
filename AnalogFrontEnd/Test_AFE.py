# Test program for Analog Front-End
import serial
import time
import sys

print(f"Arguments count: {len(sys.argv)}")
for i, arg in enumerate(sys.argv):
    print(f"Arguments {i:>2}: {arg}")

AFE = serial.Serial('/dev/ttyUSB0', sys.argv[1], timeout=2)

# Verify the Serial Port
print(f'Current Serial Port: {AFE.name}')

counter = 0;
while counter <= 20:
    # Read one byte
    # The data read from serial is in binary format,
    #   here decode such as ASCII
    line = AFE.readline().decode('ascii')
    print(f'{counter} {line}', end='')
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
