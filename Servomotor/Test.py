# Test program for Servomotor control module
import MotorControl as mc

motor = mc.Init('/dev/ttyUSB0')

mc.ReadPSW(motor)

mc.GetPositionABS(motor)

mc.Jogging(motor, 1)

mc.GetPositionABS(motor)

mc.ReadPSW(motor)

mc.CloseSerial(motor)
