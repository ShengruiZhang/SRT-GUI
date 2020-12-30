# Modules for Servomotor Controls

import serial
import time
import binascii

# Open Serial port for Servomotor: Azimuth
#
# Input: Name of the serial port, Baud rate
# Return: The serial object
#
# This sets serial 8N2, 2s timeout
#
def Init(_port_, _Baud_):

    _Servo_ = serial.Serial(_port_, _Baud_,
            bytesize=8, parity='N', stopbits=2, timeout=2)


# Close Serial port
#
# Input: The serial object
# Return: void
#
def CloseSerial(_Serial_):
    _Serial_.close()


# Read the Internal Status Word (RIS)
#
# Input: Serial object
# Return: TODO
#
# Refer to Command Reference, page 14
#
def ReadISW(_Serial_):
    _Serial_.write(b'@16 20 \r')
    response = _Serial_.readline().decode('ascii')


# Testing for spliting strings
#
# Input:
# Return:
#
def GetStr(rawStr):
    lines = rawStr.split()
    print(lines[2])
    bits = bin(int(lines[2], 16))[2:].zfill(16)
    print(bits)
