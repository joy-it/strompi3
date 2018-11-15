#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
import serial
import os
GPIO.setmode(GPIO.BCM)

# Here you can choose the connected GPIO-Pin
GPIO_TPIN = 21

serial_port = serial.Serial(
 port='/dev/serial0',
 baudrate = 38400,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=3
)

if serial_port.isOpen(): serial_port.close()
serial_port.open()


serial_port.write('Q')
sleep(1)
serial_port.write('\x0D')
sleep(1)
serial_port.write('date-rpi')
sleep(0.1)
serial_port.write('\x0D')
data = serial_port.read(9999);
date = int(data)

strompi_year = date // 10000
strompi_month = date % 10000 // 100
strompi_day = date % 100

sleep(0.1)
serial_port.write('time-rpi')
sleep(0.1)
serial_port.write('\x0D')
data = serial_port.read(9999);
timevalue = int(data)

strompi_hour = timevalue // 10000
strompi_min = timevalue % 10000 // 100
strompi_sec = timevalue % 100

rpi_time = datetime.datetime.now().replace(microsecond=0)
strompi_time = datetime.datetime(2000 + strompi_year, strompi_month, strompi_day, strompi_hour, strompi_min, strompi_sec, 0)

command = 'set-time %02d %02d %02d' % (int(rpi_time.strftime('%H')),int(rpi_time.strftime('%M')),int(rpi_time.strftime('%S')))

if rpi_time > strompi_time:
    serial_port.write('set-date %02d %02d %02d %02d' % (int(rpi_time.strftime('%d')),int(rpi_time.strftime('%m')),int(rpi_time.strftime('%Y'))%100,int(rpi_time.isoweekday())))
    sleep(0.5)
    serial_port.write('\x0D')
    sleep(1)
    serial_port.write('set-clock %02d %02d %02d' % (int(rpi_time.strftime('%H')),int(rpi_time.strftime('%M')),int(rpi_time.strftime('%S'))))
    sleep(0.5)
    serial_port.write('\x0D')

    print '-----------------------------------------'
    print 'The date und time has been synced: Raspberry Pi -> StromPi'
    print '-----------------------------------------'

else:
    os.system('sudo date +%%y%%m%%d --set=%02d%02d%02d' % (strompi_year, strompi_month, strompi_day))
    os.system('sudo date +%%T -s "%02d:%02d:%02d"' % (strompi_hour, strompi_min, strompi_sec))
    print '-----------------------------------------'
    print 'The date und time has been synced: StromPi -> Raspberry Pi'
    print '-----------------------------------------'


print "Safe Shutdown in the case of Powerfailure (CTRL-C for exit)"
# Set pin as input
GPIO.setup(GPIO_TPIN,GPIO.IN,pull_up_down = GPIO.PUD_UP)

Current_State  = 1
Previous_State = 1

try:
    print "Waiting for Initialization"
    while GPIO.input(GPIO_TPIN)==0:
     Current_State  = 1
     time.sleep(1)

    time.sleep(1)

    print "Ready"

    while True :
     Current_State = GPIO.input(GPIO_TPIN)
     if Current_State==0 and Previous_State==1:
      Previous_State=0
      execfile("sendmail.py")
     elif Current_State==1 and Previous_State==0:
      Previous_State=1
      time.sleep(0.01)

except KeyboardInterrupt:
    print "Quit"
    GPIO.cleanup()
