# Team 21039 - Radio Telescope
# Modules for AFE
#   Analog Front-End, handles the control of brakes and ADC for anemometer

import serial


# Open Serial port for AFE
#
# Input: Name of the serial port, Baud rate
# Return: the serial object
#
def Init(_port_, _Baud_):

    try:
        _AFE_ = serial.Serial(_port_, _Baud_, timeout=0.025)
        return _AFE_

    except Exception as err:
        print(err)


# Activate AFE
#
# Input: The serial object
# Return: void
#
# Activate the AFE by sending an arbitrary byte
#
def Activate(_AFE_):
    _AFE_.is_open
    _AFE_.write(b'K')
    print('AFE Response: ',  _AFE_.readline().decode('ascii'))


# Engage brake
#
# Input: The serial object
# Return: ACK from AFE
#
# Engage the brake by sending 'B' to AFE
#
def EngageBrake(_AFE_):
    _AFE_.is_open
    _AFE_.write(b'B')
    return _AFE_.readline().decode('ascii')


# Release brake
#
# Input: The serial object
# Return: ACK from AFE
#
# Release the brake by sending 'C' to AFE
#
def ReleaseBrake(_AFE_):
    _AFE_.is_open
    _AFE_.write(b'C')
    return _AFE_.readline().decode('ascii')


# Get the mapped wind speed in m/s
#
# Input: The serial object
# Return: wind speed
#
def GetWindRaw(_AFE_):
    _AFE_.is_open
    _AFE_.write(b'A')
    #test = _AFE_.readline().decode('ascii')

    return _AFE_.readline().decode('ascii')


# Get the mapped wind speed in m/s
#
# Input: The serial object
# Return: mapped wind speed
#
def GetWind(_AFE_):

    _AFE_.is_open

    count = 0

    while True:

        try:
            wind = _AFE_.readline().decode('ascii')

        except Exception as error:
            print(error)
            count += 1

        if wind != '':
            break

        if count >= 10:
            return ''

    return wind


# Close Serial port
#
# Input: The serial object
# Return: void
#
def CloseSerial(_AFE_):
    _AFE_.close()
    print(f'isSerialOpen: {_AFE_.is_open}')


