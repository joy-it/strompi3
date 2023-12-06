#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import os
import smtplib
from email.mime.text import MIMEText
GPIO.setmode(GPIO.BCM)

# Here you can choose the connected GPIO-Pin
GPIO_TPIN = 21

# Here you can choose whether you want to receive an email when the Raspberry Pi restarts - 1 to activate - 0 to deactivate
Restart_Mail = 1

# This is The config for the EMAIL notification
#----------------------------------------------
SERVER =    'SMTP.Server.Com'
PORT =      587
EMAIL =    'Example@Example.com'
PASSWORT =  'Password'
EMPFAENGER =    ['Empfänger@Example.com' ,]
SUBJECT_Powerfail =   'Raspberry Pi Powerfail!'  #Powerfail Email Betreff
SUBJECT_Powerback =   'Raspberry Pi Powerback!'  #Powerback Email Betreff
SUBJECT_Restart =     'Raspberry Pi Restart!'    #Restart Email Betreff
#----------------------------------------------

print ("E-Mail notification in  case of Powerfailure (CTRL-C for exit)")
# Set pin as input
GPIO.setup(GPIO_TPIN,GPIO.IN,pull_up_down = GPIO.PUD_UP)


    
def Sendmail_Powerback():
    BODY =      """
    <html>
     <head></head>
      <body>
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg .tg-0ord{text-align:right}
    .tg .tg-qnmb{font-weight:bold;font-size:16px;text-align:center}
    </style>
    <table class="tg">
     <tr>
      <th class="tg-qnmb" colspan="2">StromPi hat Spannung wiedererkannt!</th>
     </tr>
    </table>
     </body>
    </html>
    """

    session = smtplib.SMTP(SERVER, PORT)
    session.set_debuglevel(1)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(EMAIL, PASSWORT)
    msg = MIMEText(BODY, 'html')
    msg['Subject'] = SUBJECT_Powerback
    msg['From'] = EMAIL
    msg['To'] = ", ".join(EMPFAENGER)
    session.sendmail(EMAIL, EMPFAENGER, msg.as_string())
    Detect_event_GPIOFALLING()
 
def Sendmail_Restart():
    BODY =      """
    <html>
     <head></head>
      <body>
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg .tg-0ord{text-align:right}
    .tg .tg-qnmb{font-weight:bold;font-size:16px;text-align:center}
    </style>
    <table class="tg">
     <tr>
      <th class="tg-qnmb" colspan="2">Ihr Raspberry Pi wurde neugestartet.</th>
     </tr>
    </table>
     </body>
    </html>
    """

    session = smtplib.SMTP(SERVER, PORT)
    session.set_debuglevel(1)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(EMAIL, PASSWORT)
    msg = MIMEText(BODY, 'html')
    msg['Subject'] = SUBJECT_Restart
    msg['From'] = EMAIL
    msg['To'] = ", ".join(EMPFAENGER)
    session.sendmail(EMAIL, EMPFAENGER, msg.as_string())
    Detect_event_GPIOFALLING()
 
def Sendmail_Powerfail():
    BODY =      """
    <html>
     <head></head>
      <body>
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
    .tg .tg-0ord{text-align:right}
    .tg .tg-qnmb{font-weight:bold;font-size:16px;text-align:center}
    </style>
    <table class="tg">
     <tr>
      <th class="tg-qnmb" colspan="2">StromPi hat einen STROMAUSFALL erkannt!!!!</th>
     </tr>
    </table>
     </body>
    </html>
    """

    session = smtplib.SMTP(SERVER, PORT)
    session.set_debuglevel(1)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(EMAIL, PASSWORT)
    msg = MIMEText(BODY, 'html')
    msg['Subject'] = SUBJECT_Powerfail
    msg['From'] = EMAIL
    msg['To'] = ", ".join(EMPFAENGER)
    session.sendmail(EMAIL, EMPFAENGER, msg.as_string())
    Detect_Powerback()

def Detect_Powerback():
  while True:
    if GPIO.input(GPIO_TPIN)==0:
      time.sleep(1)
    else:
      print ("StromPi PowerBack Detected!")
      Sendmail_Powerback()
    

def Detect_event_GPIOFALLING():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TPIN,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_TPIN, GPIO.FALLING, callback=Power_Lost, bouncetime=300)
    print ("\n\n\n\n\nSendmail in case of Powerfailure (CTRL-C for exit)")
  
    while True:             
        time.sleep(0.1)

def Power_Lost(a):

    print ("Raspberry Pi Powerfail detected")                               
    print ("Powerfail_Email sent")
    Sendmail_Powerfail()
time.sleep(5) 
if Restart_Mail == 1:
  Sendmail_Restart()
  
try:
    GPIO.add_event_detect(GPIO_TPIN, GPIO.FALLING, callback=Power_Lost, bouncetime=300)
    while True: 
        time.sleep(0.1)

except KeyboardInterrupt:
    print ("\nKeyboard Interrupt")
finally:
    GPIO.cleanup()
    print ("Cleaned up Pins")

