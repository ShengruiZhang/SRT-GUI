# Test program for Servomotor control module
import MotorControl as mc
from datetime import datetime as dt

#absPos = open('absPos.dat', 'a')

mc.LoadAbsPosExt()

#a='F000'
#b='9B40'
#az = int(a+b,16)
#az=str(az) + '\n'
#
#with open('absPos.dat', 'a') as absPos:
#
#    absPos.writelines(dt.now().strftime('%Y-%m-%d %H:%M:%S\n'))
#
#a='020E'
#b='9C4F'
#alt = int(a+b,16)
#alt=str(alt) + '\n'
#
#with open('absPos.dat', 'a') as absPos:
#
#    absPos.writelines(az+alt+'\n')

#mc.CloseSerial(motor)
