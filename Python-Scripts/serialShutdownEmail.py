#!/usr/bin/env python
import time
import serial
import os

sendmail = os.path.dirname(os.path.abspath(__file__))
sendmail +="/sendmail.py"

ser = serial.Serial(
 port='/dev/serial0',
 baudrate = 38400,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=3
)


while 1:
 x=ser.readline()
 if x==('xxxShutdownRaspberryPixxx\n'):
  print "Shutdown"
  execfile(sendmail)
  time.sleep(2)
  os.system("sudo shutdown -h now")
