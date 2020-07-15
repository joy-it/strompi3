#!/usr/bin/python
# -*- coding: utf-8 -*-
# Initialization
import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)

# Here you can choose the connected GPIO-Pin and the ShutdownTimer
GPIO_TPIN = 21
ShutdownTimer = 10

print ("Safe Shutdown in the case of Powerfailure (CTRL-C for exit)")
# Set pin as input
GPIO.setup(GPIO_TPIN,GPIO.IN,pull_up_down = GPIO.PUD_UP)

Current_State  = 1
Previous_State = 1
    
def Detect_event_GPIOFALLING():
    GPIO.remove_event_detect(GPIO_TPIN)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TPIN,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_TPIN, GPIO.FALLING, callback=Power_Lost, bouncetime=300)
    while True:
        time.sleep(0.1)

def Power_Lost(GPIO_TPIN):
    GPIO.remove_event_detect(GPIO_TPIN)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TPIN,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_TPIN, GPIO.RISING, callback=Shutdown_Interrupt, bouncetime=300)
    x=0
    print ("Raspberry Pi Powerfail detected")  #print Primary power source failed
    while x != ShutdownTimer:                  #while loop that will loop until x is = ShutdownTimer    
        time.sleep(1)                        #wait for 1 second
        x = x + 1                            #increase x by 1
        if GPIO.input(GPIO_TPIN):
          break
    if x >= ShutdownTimer:                           
        print ("Raspberry Pi Shutdown!")                                #print shutdown message
        os.system("sudo shutdown -h now")                           #give the command to shutdown the raspberry
        x=0
    
def Shutdown_Interrupt(GPIO_TPIN):
    print ("Raspberry Pi Power Back Detected!")                   #Print powerback detected
    Detect_event_GPIOFALLING()
    x=0
try:
    GPIO.add_event_detect(GPIO_TPIN, GPIO.FALLING, callback=Power_Lost, bouncetime=300)
    while True: 
        time.sleep(0.1)

except KeyboardInterrupt:
    print ("\nKeyboard Interrupt")
finally:
    GPIO.cleanup()
    print ("Cleaned up Pins")
