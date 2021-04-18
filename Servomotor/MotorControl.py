# Team 21039 - Radio Telescope
# Date: 2020 Fall - 2021 Spring
#
# Modules for Servomotor Controls
#######################################

import serial
from time import sleep
import binascii
from datetime import datetime as dt

_Baud_SilverMax_ = 57600

# Open Serial port for Servomotor: Azimuth
#
# Input: Name of the serial port, Baud rate
# Return: The serial object
#
# This sets serial 8N2, 25ms timeout
#
def Init(_port_):

    _Servo_ = serial.Serial(_port_,
                            _Baud_SilverMax_,
                            bytesize=8, parity='N', stopbits=2,
                            timeout=0.025)

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
# Refer to Command Reference page 11, and User Manual page 60 and 156
#
def ReadPSW(_Serial_):

    print('Reading PSW')

    # Poll without cmd number
    _Serial_.write(b'@16 \r')

    _response_ = _Serial_.readline().decode('ascii')

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
# Refer to Command Reference page 14, and User Manual page 63 and 156
#
def ReadISW(_Serial_):

    print('Reading ISW')

    _Serial_.write(b'@16 20 \r')

    _response_ = _Serial_.readline().decode('ascii')

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


# Manual Jogging Servomotor based on input Serial object
#
# Input:    Serial object, Jogging distance
# Return:   void
#
# Refer to Command Reference page 99, user manual 43 (acceleration)
#   MRV is used here
#
def Jogging(_Serial_, _dist_, _acc_, _vel_):

    _command_ = "@16 135 " + str(_dist_) + ' ' + str(acc2nat(_acc_)) + ' ' + str(rps2nat(_vel_)) + " 0 0 \r"

    if (ReadPSW(_Serial_) & 0x2000) == 0x2000:
        _Serial_.write(_command_.encode())
    else:
        print('There is an on-going motion.')

    print(_Serial_.readline())
    print()


# Move the telescope, given input coord
#   This assumes the stow position is 30 deg pass zenith
#
# Input:    Serial object of both SilverMax, AZ coord, ALT coord
# Return:   void
#
# Refer to Command Reference page 96
#   MAV is used
#
def Entry(_Serial_AZ_, _Serial_ALT_, _AZ_, _ALT_):

    _command_ = "@16 134 " + str(round(_AZ_ * 9365)) + ' ' + str(acc2nat(2)) + ' ' + str(rps2nat(5)) + " 0 0 \r"

    _Serial_AZ_.write(_command_.encode())

    print(_Serial_AZ_.readline())

    _command_ = "@16 134 " + str( round((90 - _ALT_) * 1857) ) + ' ' + str(acc2nat(1)) + ' ' + str(rps2nat(1)) + " 0 0 \r"

    _Serial_ALT_.write(_command_.encode())

    print(_Serial_ALT_.readline())


# Move the telescope, given input coord
#   This assumes the stow position is 30 deg pass zenith
#
# Input:    Serial object AZ, AZ coord in degrees
# Return:   void
#
# Refer to Command Reference page 96
#   MAV is used
#
def Entry_AZ(_Serial_AZ_, _AZ_):

    _command_ = "@16 134 " + str(round(_AZ_ * 9365)) + ' ' + str(acc2nat(2)) + ' ' + str(rps2nat(5)) + " 0 0 \r"

    _Serial_AZ_.write(_command_.encode())

    print(_Serial_AZ_.readline())


# Move the telescope, given input coord
#   This assumes the stow position is 30 deg pass zenith
#
# Input:    Serial object of ALT, ALT coord in degrees
# Return:   void
#
# Refer to Command Reference page 96
#   MAV is used
#
def Entry_ALT(_Serial_ALT_, _ALT_):

    _command_ = "@16 134 " + str( round((90 - _ALT_) * 1857) ) + ' ' + str(acc2nat(1)) + ' ' + str(rps2nat(1)) + " 0 0 \r"

    _Serial_ALT_.write(_command_.encode())

    print(_Serial_ALT_.readline())


# Stowing the telescope, move it back to the stow Position (aka. home Position)
#
# Input:    Serial object, Jogging distance
# Return:   void
#
# Refer to Command Reference page 96
#   MAV is used
#
def Stow(_Serial_, _dist_, _acc_, _vel_):

    _command_ = "@16 134 " + str(_dist_) + ' ' + str(acc2nat(_acc_)) + ' ' + str(rps2nat(_vel_)) + " 0 0 \r"

    _Serial_.write(_command_.encode())

    print(_Serial_.readline())


# Software restart the Servomotor
#
# Input:    Serial object
# Return:   void
#
# Refer to Command Reference page 19
#
def Restart(_Serial_):

    _command_ = "@16 4 \r"

    _Serial_.write(_command_.encode())


# Stop the SilverMax
#
# Input:    Serial object
# Return:   0 if ACK received, otherwise 1
#
# Refer to Command Reference page 20, User Manual page 156
#   STP is used here
#
def Stop(_Serial_):

    _command_ = "@16 3 0 \r"

    _Serial_.write(_command_.encode())

    lines = _Serial_.readline().decode('ascii')

    try:
        if lines[0] == '*' and lines[1] == "10":
            return 0
        else:
            return 1

    except IndexError as ie:
        print('Servo did not respond within the given time.')


# Stop the SilverMax with Deceleration argument
#
# Input:    Serial object, Deceleration
# Return:   0 if ACK received, otherwise 1
#
# Refer to Command Reference page 20, User Manual page 156
#   STP is used here
#
def Stop2(_Serial_, _acc_):

    # DEBUG FOR ALT LIMIT
    _command_ = "@16 3 " + str( acc2nat(_acc_) ) + "  \r"

    _Serial_.write(_command_.encode())

    lines = _Serial_.readline().decode('ascii')

    try:
        if lines[0] == '*' and lines[1] == "10":
            return 0
        else:
            return 1

    except IndexError as ie:
        print('Servo did not respond within the given time.')


# Get SilverMax temperature
#
# Input:    Serial object
# Return:   temperature of SilverMax
#
# Refer to User Manual page 190
#   TODO Reading register 215 lower word
#
def GetTemp(_Serial_):

    _tempRaw_ = ReadRegister(_Serial_, 215)

    print(_tempRaw_)

    lines = _tempRaw_.split()


# Get SilverMax voltage
#
# Input:    Serial object
# Return:   Voltage of SilverMax
#
# Refer to User Manual page 190
# Reading register 214 high word and 216 low word
#
def GetVoltage(_Serial_):

    line1 = ReadRegister(_Serial_, 216)

    line2 = ReadRegister(_Serial_, 214)

    voltage = round( int(line2[3], 16) / int(line1[4], 16), 2 )

    return voltage


# Get abs Position of SilverMax
#
# Input:    Serial object
# Return:   signed abs Position in counts
#
# Refer to User Manual page 189
#
def GetPosAbs(_Serial_):

    _abs_ = ReadRegister(_Serial_, 1)

    try:
        if _abs_[0] == '#' and _abs_[1] == "10":
            return twos_comp((_abs_[3] + _abs_[4]), 32)

    except IndexError as ie:
        print('Error: SilverMax didn\'t respond, check Servomotor connection')
        print(str(ie))


# Read SilverMax register
#
# Input:    Serial object, register number
# Return:   Data of the register
#
# Refer to Command Reference page 159
#   RRG is used here
#
def ReadRegister(_Serial_, _reg_):

    _command_ = "@16 12 " + str(_reg_) + " \r"

    _Serial_.write(_command_.encode())

    return _Serial_.readline().decode('ascii').split()


# Store abs Position to SilverMax NVMEM
#
# Input:    Serial object
# Return:   void
#
# Refer to User Manual page 98 and Command Reference 162
#   RSN is used here
#
def SaveAbsPos(_Serial_):

    # store to NVMEM address 1000
    _command_ = "@16 198 1 1612 \r"

    _Serial_.write(_command_.encode())

    print(_Serial_.readline().decode('ascii'))


# Zero Target and Position
#
# Input:    Serial object
# Return:   SilverMax response
#
# Refer to Command Reference page 174
#   ZTP is used here
#
def Zero(_Serial_):

    _command_ = "@16 145 " + " \r"

    _Serial_.write(_command_.encode())

    return _Serial_.readline().decode('ascii')


# Check if the motion exceeds the mechanical travel of Azimuth
#
# Input:    Azimuth abs Position
# Return:   Abs Position of the AZ Servo
#
def LimitAZ(_Serial_):

    _absAZ_ = GetPosAbs(_Serial_)

    if _absAZ_ < -842857:

        Stop(_Serial_)

        # Allow it to move
        sleep(1.5)

        print('The motion exceeds the AZ travel limit: NEGATIVE TURN')

        # Move it away
        Jogging(_Serial_, 4000, 2, 2)

        # Allow it to move
        sleep(1.5)

    elif _absAZ_ > 4214285:

        Stop(_Serial_)

        # Allow it to move
        sleep(1.5)

        print('The motion exceeds the AZ travel limit: POSITIVE TURN')

        # Move it away
        Jogging(_Serial_, -4000, 2, 2)

        # Allow it to move
        sleep(1.5)

    return GetPosAbs(_Serial_)


# Check if the motion exceeds the mechanical travel of Altitude
#
# Input:    Altitude Serial object
# Return:   Abs Position of the ALT Servo
#
# Assume ALT Servo is zeroed at zenith
#
def LimitALT_zenith(_Serial_):

    _absALT_ = GetPosAbs(_Serial_)

    if _absALT_ < -74280:

        Stop2(_Serial_, 10)

        # Allow it to move
        sleep(1.5)

        print('The motion exceeds the ALT travel limit: HIGH')

        # Move it away
        Stow(_Serial_, -74200, 2, 5)

        # Allow it to move
        sleep(1.5)

    elif _absALT_ > 144846:

        Stop2(_Serial_, 10)

        # Allow it to move
        sleep(1.5)

        print('The motion exceeds the ALT travel limit: LOW')

        # Move it away
        Stow(_Serial_, 142989, 2, 5)

        # Allow it to move
        sleep(1.5)

    return GetPosAbs(_Serial_)


# Check if the motion exceeds the mechanical travel of Altitude
#
# Input:    Altitude Serial object
# Return:   Abs Position of the ALT Servo
#
# Assume ALT Servo is zeroed at 30 deg pass zenith
#
def LimitALT(_Serial_):

    _absALT_ = GetPosAbs(_Serial_)

    if _absALT_ < -928:

        Stop(_Serial_)

        print('The motion exceeds the ALT travel limit: HIGH')

        # Move it away
        Jogging(_Serial_, 4000, 2, 2)

        # Allow it to move
        sleep(1.5)

    elif _absALT_ > 200556:

        Stop(_Serial_)

        print('The motion exceeds the ALT travel limit: LOW')

        # Move it away
        Jogging(_Serial_, -4000, 2, 2)

        # Allow it to move
        sleep(1.5)

    return GetPosAbs(_Serial_)


# Convert human-readable velocity(rpm) into native units of SilverMax
#
# Input:    velocity in rpm
# Return:   velocity in native units
#
# Refer to User Manual page 43
#
def rpm2nat(_rpm_):
    return  round(_rpm_ * 536870.911)


# Convert human-readable velocity(rps) into native units of SilverMax
#
# Input:    velocity in rps
# Return:   velocity in native units
#
# Refer to User Manual page 43
#
def rps2nat(_rps_):
    return  round(_rps_ * 60 * 536870.911)


# Convert human-readable acceleration(rps/s) into native units of SilverMax
#
# Input:    acceleration in rps/s
# Return:   acceleration in native units
#
# Refer to User Manual page 43
#
def acc2nat(_acc_):
    return round(_acc_ * 3865)


# Convert native SilverMax counts to numerical degrees
#
# Input:    alt SilverMax counts
# Return:   numerical degrees
#
# Refer to /docs/gear_ratio
#
def nat2alt(_counts_):
    return  round(_counts_ * 0.000538)


# Convert native SilverMax counts to numerical degrees
#
# Input:    az SilverMax counts
# Return:   numerical degrees
#
# Refer to /docs/gear_ratio
#
def nat2az(_counts_):
    return  round(_counts_ * 0.000107)


# Convert Hex two's complement to signed decimal
#
# Input:    32-bit Hex
# Return:   signed decimal number
#
def twos_comp(_hex_, bits):
    val = int(_hex_, 16)
    if( val & (1 << (bits-1)) ) != 0:
        val -= 1 << bits
    return val
