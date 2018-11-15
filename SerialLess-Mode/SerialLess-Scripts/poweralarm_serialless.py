#!/usr/bin/python
# Initialization
import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)

# Here you can choose the connected GPIO-Pin
GPIO_TPIN = 21

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