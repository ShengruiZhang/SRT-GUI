# Modules for AFE
#   Analog Front-End, handles the control of brakes and ADC for anemometer

import serial
import time

# Open Serial port for AFE
#
# Input: Name of the serial port, Baud rate
# Return: the serial object
#
# This also set the timeout for readline to 2s
#
def Init(_port_, _Baud_):
    _AFE_ = serial.Serial(_port_, _Baud_, timeout=2)
    return _AFE_


# Activate AFE
#
# Input: The serial object
# Return: void
#
# Activate the AFE by sending an arbitrary byte
#
def Activate(_AFE_):
    _AFE_.is_open

    while True:
        # Here K stands for ACK, but it can be anything
        _AFE_.write(b'K')
        time.sleep(2)
        if _AFE_.readline().decode('ascii') == 'AFE Active\n':
            print('AFE is now active')
            break


# Get the raw ADC value
#
# Input: The serial object
# Return: Raw ADC value
#
def GetWindRaw(_AFE_):
    _AFE_.is_open
    _AFE_.write(b'A')
    return _AFE_.readline().decode('ascii')


# Close Serial port
#
# Input: The serial object
# Return: Raw ADC value
#
def CloseSerial(_Serial_):
    _Serial_.close()
    print(f'isSerialOpen: {_Serial_.is_open}')
