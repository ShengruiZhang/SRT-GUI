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
_Baud_SilverMax_ = 57600

def Init(_port_):

    _Servo_ = serial.Serial(_port_, _Baud_SilverMax_,
                            bytesize=8, parity='N', stopbits=2, timeout=2)

    return _Servo_


# Close Serial port
#
# Input: The serial object
# Return: void
#
def CloseSerial(_Serial_):
    _Serial_.close()


# Read the Polling Status Word (POL)
#
# Input:    Serial object
# Return:   print the status of each bit
#           The binary int of PSW
#
# Refer to Command Reference page 11, and User Manual page 60
#
def ReadPSW():

    print('Reading PSW')

    # Poll without cmd number
    #_Serial_.write(b'@16 \r')

    # TESTING making up PSW
    #_response_ = _Serial_.readline().decode('ascii')
    _response_ = '# 10 0000 0300 \r'

    lines = _response_.split()

    if _response_ == '* 10 \r':

        print('SilverMax responsed without status')

    elif lines[0] == '#' and lines[1] == '10':

        print(f'SilverMax Responsed: {_response_}')

        bits = bin(int(lines[3], 16))[2:].zfill(16)

        print(f'Binary: {int(bits)}')

        if int(bits) & 0x8000:
            print('Bit 15 Set: Immediate command finished executing')
        else:
            print('Bit 15: Immediate command is being executed')

        if int(bits) & 0x4000:
            print('Bit 14 Set: NVM checksum error')
        else:
            print('Bit 14: NVM checksum normal')

        if int(bits) & 0x2000:
            print('Bit 13 Set: Commands in Pgm. Buffer finished executing')
        else:
            print('Bit 13: Commands in Pgm. Buffer are being executed')

        if int(bits) & 0x1000:
            print('Bit 12 Set: Error with command execution')
        else:
            print('Bit 12: No error with command execution')

        if int(bits) & 0x0800:
            print('Bit 11 Set: Move stopped due to a stop on input cond.')
        else:
            print('Bit 11: Move stopped normally')

        if int(bits) & 0x0400:
            print('Bit 10 Set: Low/Over voltage detected')
        else:
            print('Bit 10: Voltage is normal')

        if int(bits) & 0x0200:
            print('Bit 9 Set: Holding Error Occured')
        else:
            print('Bit 9: No holding error occured')

        if int(bits) & 0x0100:
            print('Bit 8 Set: Moving Error Occured')
        else:
            print('Bit 8: No moivng error occured')

        if int(bits) & 0x0080:
            print('Bit 7 Set: SilverMax receiver overflowed')
        else:
            print('Bit 7: SilverMax receiver is normal')

        if int(bits) & 0x0040:
            print('Bit 6 Set: CKS Cond. Met')
        else:
            print('Bit 6: CKS Cond. Not Met')

        if int(bits) & 0x0020:
            print('Bit 5 Set: Last msg received was too long')
        else:
            print('Bit 5: Last msg received within lenghth')

        if int(bits) & 0x0010:
            print('Bit 4 Set: Last byte received has framing error')
        else:
            print('Bit 4: Last byte recieved correctly')

        if int(bits) & 0x0008:
            print('Bit 3 Set: SilverMax shut down because kill cond. met')
        else:
            print('Bit 3: SilverMax is operational')

        if int(bits) & 0x0004:
            print('Bit 2 Set: Soft stop limit reached')
        else:
            print('Bit 2: Soft stop limit not reached')

        if int(bits) & 0x0002:
            print('Bit 1 Set: Last packet dumped due to checksum error')
        else:
            print('Bit 1: Last packet had no checksum error')

        if int(bits) & 0x0001:
            print('Bit 0 Set: Some packets aborted')
        else:
            print('Bit 0: Packets received normally')

    else:

        print(f'SilverMax Responsed: {_response_}')

    print()

    return int(bits)


# Read the Internal Status Word (RIS)
#
# Input:    Serial object
# Return:   Print the status of each bit
#           The binary int of ISW
#
# Refer to Command Reference page 14, and User Manual page 63
#
def ReadISW():

    print('Reading ISW')

    #_Serial_.write(b'@16 20 \r')

    # For testing, making up ISW
    _response_ = '# 10 0014 00F3'
    #_response_ = _Serial_.readline().decode('ascii')

    print(f'SilverMax Responsed: {_response_}')

    lines = _response_.split()

    if lines[0] == '#' and lines[1] == '10':

        bits = bin(int(lines[3], 16))[2:].zfill(16)

        print(f'Binary: {int(bits)}')

        if int(bits) & 0x8000:
            print('Bit 15: Reserved bit')

        if int(bits) & 0x4000:
            print('Bit 14 Set: Low voltage detected')
        else:
            print('Bit 14: Low voltage not detected')

        if int(bits) & 0x2000:
            print('Bit 13 Set: Over voltage detected')
        else:
            print('Bit 13: Over voltage not detected')

        if int(bits) & 0x1000:
            print('Bit 12 Set: Wait timer expired')
        else:
            print('Bit 12: Wait timer not expired')

        if int(bits) & 0x0800:
            print('Bit 11 Set: Input Found On Last Move True')
        else:
            print('Bit 11: Input Found On Last Move False')

        if int(bits) & 0x0400:
            print('Bit 10 Set: Halt command received')
        else:
            print('Bit 10: No Halt command received')

        if int(bits) & 0x0200:
            print('Bit 9 Set: Holding Error Occured')
        else:
            print('Bit 9: No holding error occured')

        if int(bits) & 0x0100:
            print('Bit 8 Set: Moving Error Occured')
        else:
            print('Bit 8: No moivng error occured')

        if int(bits) & 0x0080:
            print('Bit 7: Over Temp. Cond. disabled')
        else:
            print('Bit 7: Over Temp. Cond. enabled')

        if int(bits) & 0x0040:
            print('Bit 6: I/O #3 is High')
        else:
            print('Bit 6: I/O #3 is Low')

        if int(bits) & 0x0020:
            print('Bit 5: I/O #2 is High')
        else:
            print('Bit 5: I/O #2 is Low')

        if int(bits) & 0x0010:
            print('Bit 4: I/O #1 is High')
        else:
            print('Bit 4: I/O #1 is Low')

        if int(bits) & 0x0008:
            print('Bit 3: none')
        else:
            print('Bit 3: none')

        if int(bits) & 0x0004:
            print('Bit 2: none')
        else:
            print('Bit 2: none')

        if int(bits) & 0x0002:
            print('Bit 1: none')
        else:
            print('Bit 1: none')

        if int(bits) & 0x0001:
            print('Bit 0 Set: Index sensor detected')
        else:
            print('Bit 0: Warning: No index sensor detected')

    print()

    return int(bits)


def MRV(_Serial_, _vel_):

    _command_ = "@16 135 -44000 10000 "

    #_command_ = _command_ + _vel_ + " 0 0 \r"
    _command_ += _vel_ + " 0 0 \r"

    print(_command_.encode())

    #_Serial_.write(b'@16 135 -14000 20000 30000000 0 0 \r')
    _Serial_.write(_command_.encode())

    print(_Serial_.readline().decode('ascii'))


# Manual Jogging: Azimuth Servomotor
#
# Input:    Serial object
# Return:   void
#
# Refer to Command Reference page 14, and User Manual page 63
#   MRV is used here
#
def Jogging(_Serial_, _dir_):

    if _dir_== 1:
        # 2000 counts -> clockwise, half rev of Servomotor
        _command_ = "@16 135 2000 20000 30000000 0 0 \r"

    elif _dir_ == 0:
        # counter-clockwise
        _command_ = "@16 135 -2000 20000 30000000 0 0 \r"

    _Serial_.write(_command_.encode())

    print(_Serial_.readline().decode('ascii'))


# Stop the SilverMax
#
# Input:    Serial object
# Return:   void
#
# Refer to Command Reference page 20
#   STP is used here
#
def Stop(_Serial_):
    _command_ = "@16 3 0 \r"

    _Serial_.write(_command_.encode())

    print(_Serial_.readline().decode('ascii')

# Testing for spliting strings
#
# Input: Text strings
# Return: Lines separated by space
#
def GetStr(rawStr):
    lines = rawStr.split()
    print(lines[2])
    bits = bin(int(lines[2], 16))[2:].zfill(16)
    print(bits)
