import serial
import threading
from time import sleep
import time
import datetime
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO_TPIN = 21

serial_port = serial.Serial()

serial_port.baudrate = 38400
serial_port.port = '/dev/serial0'
serial_port.timeout = 1
serial_port.bytesize = 8
serial_port.stopbits = 1
serial_port.parity = serial.PARITY_NONE





try:
    GPIO.setup(GPIO_TPIN,GPIO.OUT)
    #GPIO.output(GPIO_TPIN, GPIO.HIGH)
    #print ("HIGH")
    #time.sleep(3)
    GPIO.output(GPIO_TPIN, GPIO.LOW)
    print ("Setting GPIO to LOW to Disable Serialless Mode.")
    print ("This will take approx. 10 seconds.")
    time.sleep(10)
    GPIO.cleanup()
    print ("Serialless Mode is Disabled!")
	

    if serial_port.isOpen(): serial_port.close()
    serial_port.open()


    serial_port.write(str.encode('Q'))
    sleep(1)
    serial_port.write(str.encode('\x0D'))
    sleep(1)
    serial_port.write(str.encode('date-rpi'))
    sleep(0.1)
    serial_port.write(str.encode('\x0D'))
    data = serial_port.read(9999);
    date = int(data)
    strompi_year = date // 10000
    strompi_month = date % 10000 // 100
    strompi_day = date % 100
    sleep(0.1)
    serial_port.write(str.encode('time-rpi'))
    sleep(0.1)
    serial_port.write(str.encode('\x0D'))
    data = serial_port.read(9999);
    timevalue = int(data)
    strompi_hour = timevalue // 10000
    strompi_min = timevalue % 10000 // 100
    strompi_sec = timevalue % 100
    rpi_time = datetime.datetime.now().replace(microsecond=0)
    strompi_time = datetime.datetime(2000 + strompi_year, strompi_month, strompi_day, strompi_hour, strompi_min,strompi_sec, 0)
    if rpi_time > strompi_time:
        print ("Setting Time!")
        serial_port.write(str.encode('set-date %02d %02d %02d %02d' % (
        int(rpi_time.strftime('%d')), int(rpi_time.strftime('%m')), int(rpi_time.strftime('%Y')) % 100,
        int(rpi_time.isoweekday()))))
        sleep(0.5)
        serial_port.write(str.encode('\x0D'))
        sleep(1)
        serial_port.write(str.encode('set-clock %02d %02d %02d' % (
        int(rpi_time.strftime('%H')), int(rpi_time.strftime('%M')), int(rpi_time.strftime('%S')))))
        sleep(0.5)
        serial_port.write(str.encode('\x0D'))
		
		
    breakS = 0.1
    breakL = 0.2
    serial_port = serial.Serial()
    serial_port.baudrate = 38400
    serial_port.port = '/dev/serial0'
    serial_port.timeout = 1
    serial_port.bytesize = 8
    serial_port.stopbits = 1
    serial_port.parity = serial.PARITY_NONE
	
    if serial_port.isOpen(): serial_port.close()
    serial_port.open()
	
    serial_port.write(str.encode('quit'))
    time.sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    time.sleep(breakL)
    serial_port.write(str.encode('set-config 0 2'))
    time.sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    time.sleep(breakL)
    print ("Enabled Serialless")

except KeyboardInterrupt:
    print('interrupted!')
    GPIO.cleanup()

serial_port.close()