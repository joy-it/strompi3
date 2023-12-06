#!/usr/bin/python
# -*- coding: utf-8 -*-
# Initialization
import RPi.GPIO as GPIO
import time
import os
import serial
GPIO.setmode(GPIO.BCM)
GPIO_TPIN = 21

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