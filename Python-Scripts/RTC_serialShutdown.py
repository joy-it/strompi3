#!/usr/bin/env python
import time
from time import sleep
import datetime
import serial
import os


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


while 1:
 x=serial_port.readline()
 if x==('xxxShutdownRaspberryPixxx\n'):
  print "Shutdown"
  time.sleep(1)
  os.system("sudo shutdown -h now")
