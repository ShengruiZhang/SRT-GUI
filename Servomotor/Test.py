# Test program for Servomotor control module
import MotorControl as mc
import serial

#Servo_AZ = mc.Init('/dev/ttyUSB0', 57600)

mc.GetStr('#10 0014 00F3 \r')

