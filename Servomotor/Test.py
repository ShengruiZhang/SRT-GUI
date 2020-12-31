# Test program for Servomotor control module
import MotorControl as mc
# 
# motor = mc.Init('/dev/ttyUSB0', 57600)
# 
# mc.MRV(motor, '30000000')
# 
# mc.CloseSerial(motor)

#ISW = '#10 0014 00F3 \r'

#mc.GetStr(ISW)

mc.ReadISW()

mc.ReadPSW()
