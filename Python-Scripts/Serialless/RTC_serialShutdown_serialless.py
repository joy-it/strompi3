#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
import serial
import os
GPIO.setmode(GPIO.BCM)

# Here you can choose the connected GPIO-Pin and the ShutdownTimer
GPIO_TPIN = 21
ShutdownTimer = 10

sendmail = os.path.dirname(os.path.abspath(__file__))
sendmail +="/sendmail.py"

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
strompi_time = datetime.datetime(2000 + strompi_year, strompi_month, strompi_day, strompi_hour, strompi_min, strompi_sec, 0)

command = 'set-time %02d %02d %02d' % (int(rpi_time.strftime('%H')),int(rpi_time.strftime('%M')),int(rpi_time.strftime('%S')))



if rpi_time > strompi_time:
    serial_port.write(str.encode('set-date %02d %02d %02d %02d') % (int(rpi_time.strftime('%d')),int(rpi_time.strftime('%m')),int(rpi_time.strftime('%Y'))%100,int(rpi_time.isoweekday())))
    sleep(0.5)
    serial_port.write(str.encode('\x0D'))
    sleep(1)
    serial_port.write(str.encode('set-clock %02d %02d %02d') % (int(rpi_time.strftime('%H')),int(rpi_time.strftime('%M')),int(rpi_time.strftime('%S'))))
    sleep(0.5)
    serial_port.write(str.encode('\x0D'))

    print ("-----------------------------------------")
    print ("The date und time has been synced: Raspberry Pi -> StromPi")
    print ("-----------------------------------------")

else:
    os.system('sudo date +%%y%%m%%d --set=%02d%02d%02d' % (strompi_year, strompi_month, strompi_day))
    os.system('sudo date +%%T -s "%02d:%02d:%02d"' % (strompi_hour, strompi_min, strompi_sec))
    print ("-----------------------------------------")
    print ("The date und time has been synced: StromPi -> Raspberry Pi")
    print ("-----------------------------------------")
	
if serial_port.isOpen(): serial_port.close()
serial_port.open()
	
serial_port.write(str.encode('quit'))
time.sleep(0.1)
serial_port.write(str.encode('\x0D'))
time.sleep(0.2)
serial_port.write(str.encode('set-config 0 2'))
time.sleep(0.1)
serial_port.write(str.encode('\x0D'))
time.sleep(0.2)
print ("Enabled Serialless")


print ("Safe Shutdown in the case of Powerfailure (CTRL-C for exit)")
# Set pin as input
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TPIN,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    
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
