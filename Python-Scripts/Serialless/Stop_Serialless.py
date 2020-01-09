#!/usr/bin/python
# -*- coding: utf-8 -*-
# Initialization
import RPi.GPIO as GPIO
import time
import os
import serial
GPIO.setmode(GPIO.BCM)
GPIO_TPIN = 21


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