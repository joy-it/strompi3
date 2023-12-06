import serial
from time import sleep
import datetime
import os
import time
from time import sleep
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
#need sudo apt-get install python3-pil python3-pil.imagetk

wide_range_volt_min = 4.8
battery_volt_min = 0.5
mUSB_volt_min = 4.1
TimeSynctmp = 0



breakS = 0.1
breakL = 0.5

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
sleep(breakS)
serial_port.write(str.encode('\x0D'))
sleep(breakL)
serial_port.write(str.encode('status-rpi'))
sleep(1)
serial_port.write(str.encode('\x0D'))
sp3_time = serial_port.readline(9999);
sp3_date = serial_port.readline(9999);
sp3_weekday = serial_port.readline(9999);
sp3_modus = serial_port.readline(9999);
sp3_alarm_enable = serial_port.readline(9999);
sp3_alarm_mode = serial_port.readline(9999);
sp3_alarm_hour = serial_port.readline(9999);
sp3_alarm_min = serial_port.readline(9999);
sp3_alarm_day = serial_port.readline(9999);
sp3_alarm_month = serial_port.readline(9999);
sp3_alarm_weekday = serial_port.readline(9999);
sp3_alarmPoweroff = serial_port.readline(9999);
sp3_alarm_hour_off = serial_port.readline(9999);
sp3_alarm_min_off = serial_port.readline(9999);
sp3_shutdown_enable = serial_port.readline(9999);
sp3_shutdown_time = serial_port.readline(9999);
sp3_warning_enable = serial_port.readline(9999);
sp3_serialLessMode = serial_port.readline(9999);
sp3_intervalAlarm = serial_port.readline(9999);
sp3_intervalAlarmOnTime = serial_port.readline(9999);
sp3_intervalAlarmOffTime = serial_port.readline(9999);
sp3_batLevel_shutdown = serial_port.readline(9999);
sp3_batLevel = serial_port.readline(9999);
sp3_charging = serial_port.readline(9999);
sp3_powerOnButton_enable = serial_port.readline(9999);
sp3_powerOnButton_time = serial_port.readline(9999);
sp3_ADC_Wide = float(serial_port.readline(9999))/1000;
sp3_ADC_BAT = float(serial_port.readline(9999))/1000;
sp3_ADC_USB = float(serial_port.readline(9999))/1000;
sp3_ADC_OUTPUT = float(serial_port.readline(9999))/1000;
sp3_output_status = serial_port.readline(9999);
sp3_powerfailure_counter = serial_port.readline(9999);
sp3_firmwareVersion = serial_port.readline(9999);
sp3_modus_temp = int(sp3_modus)
Alarm_Powerofffailmin = 0
Alarm_Powerofffailhour = 0

def enabled_disabled_converter(argument):
    switcher = {
        0: 'Disabled',
        1: 'Enabled',
    }
    return switcher.get(argument, 'nothing')

def weekday_converter(argument):
    switcher = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday',
    }
    return switcher.get(argument, 'nothing')

def strompi_mode_converter(argument):
    switcher = {
        1: 'mUSB -> Wide',
        2: 'Wide -> mUSB',
        3: 'mUSB -> Battery',
        4: 'Wide -> Battery',
        5: "mUSB -> Wide -> Battery",
        6: "Wide -> mUSB -> Battery",
    }
    return switcher.get(argument, 'nothing')

def alarm_mode_converter(argument):
    switcher = {
        1: 'Time-Alarm',
        2: 'Date-Alarm',
        3: 'Weekday-Alarm',
        4: 'Minute Wakeup-Alarm',
    }
    return switcher.get(argument, 'nothing')

def batterylevel_shutdown_converter(argument):
    switcher = {
        0: 'Disabled',
        1: '10%',
        2: '25%',
        3: '50%',
    }
    return switcher.get(argument, 'nothing')

def output_status_converter(argument):
    switcher = {
        0: 'Power-Off', #only for Debugging-Purposes
        1: 'mUSB',
        2: 'Wide',
        3: 'Battery',
    }
    return switcher.get(argument, 'nothing')

def batterylevel_converter(batterylevel,charging):

    if charging:
        switcher = {
            1: ' [10%] [charging]',
            2: ' [25%] [charging]',
            3: ' [50%] [charging]',
            4: ' [100%] [charging]',
        }
        return switcher.get(batterylevel, 'nothing')
    else:
        switcher = {
            1: ' [10%]',
            2: ' [25%]',
            3: ' [50%]',
            4: ' [100%]',
        }
        return switcher.get(batterylevel, 'nothing')

def Set_Alarm_Mode(sp3_alarm_mode):
    if sp3_alarm_mode == "1":
        serial_port.write(str.encode('set-config ' + '2 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '3 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '4 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
        serial_port.write(str.encode('set-config ' + '26 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

    elif sp3_alarm_mode == "2":
        serial_port.write(str.encode('set-config ' + '2 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '3 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '4 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
        serial_port.write(str.encode('set-config ' + '26 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

    elif sp3_alarm_mode == "3":
        serial_port.write(str.encode('set-config ' + '2 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '3 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '4 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
        serial_port.write(str.encode('set-config ' + '26 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
    if sp3_alarm_mode == "4":
        serial_port.write(str.encode('set-config ' + '2 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '3 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-config ' + '4 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
        serial_port.write(str.encode('set-config ' + '26 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
def Set_Warning_enable(sp3_warning_enable):
    if (sp3_warning_enable == "1") or (sp3_warning_enable == "0"):
        if type(sp3_warning_enable) == str:
            serial_port.write(str.encode('set-config ' + '16 ' + sp3_warning_enable))
        else:
            serial_port.write(str.encode('set-config ' + '16 ' + sp3_warning_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
		
def Set_PoweroffMode(sp3_poweroffMode):
    if (sp3_poweroffMode == "1") or (sp3_poweroffMode == "0"):
        if type(sp3_poweroffMode) == str:
            serial_port.write(str.encode('set-config ' + '25 ' + sp3_poweroffMode))
        else:
            serial_port.write(str.encode('set-config ' + '25 ' + sp3_poweroffMode.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
		
def Set_wakeupweekend_enable(sp3_wakeupweekend_enable):
    if (sp3_wakeupweekend_enable == "1") or (sp3_wakeupweekend_enable == "0"):
        if type(sp3_wakeupweekend_enable) == str:
            serial_port.write(str.encode('set-config ' + '28 ' + sp3_wakeupweekend_enable))
        else:
            serial_port.write(str.encode('set-config ' + '28 ' + sp3_wakeupweekend_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
def Set_Shutdown_enable(sp3_shutdown_enable):
    if (sp3_shutdown_enable == "1") or (sp3_shutdown_enable == "0"):
        if type(sp3_shutdown_enable) == str:
            serial_port.write(str.encode('set-config ' + '14 ' + sp3_shutdown_enable))
        else:
            serial_port.write(str.encode('set-config ' + '14 ' + sp3_shutdown_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
		
def Set_Batlevel_Shutdown(sp3_batLevel_shutdown):
    if (sp3_batLevel_shutdown == "1") or (sp3_batLevel_shutdown == "0") or (sp3_batLevel_shutdown == "2") or (sp3_batLevel_shutdown == "3"):
        if type(sp3_batLevel_shutdown) == str:
            serial_port.write(str.encode('set-config ' + '18 ' + sp3_batLevel_shutdown))
        else:
            serial_port.write(str.encode('set-config ' + '18 ' + sp3_batLevel_shutdown.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
		
def Set_Serialless_mode(sp3_serialLessMode):
    if (sp3_serialLessMode == "1") or (sp3_serialLessMode == "0"):
        if type(sp3_serialLessMode) == str:
            serial_port.write(str.encode('set-config ' + '17 ' + sp3_serialLessMode))
        else:
            serial_port.write(str.encode('set-config ' + '17 ' + sp3_serialLessMode.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
		
def Set_PoweronButton(sp3_powerOnButton_enable):
    if (sp3_powerOnButton_enable == "1") or (sp3_powerOnButton_enable == "0"):
        if type(sp3_powerOnButton_enable) == str:
            serial_port.write(str.encode('set-config ' + '22 ' + sp3_powerOnButton_enable))
        else:
            serial_port.write(str.encode('set-config ' + '22 ' + sp3_powerOnButton_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
def Use_Modusreset(modusreset):
    if modusreset == 1:
        serial_port.write(str.encode('set-config ' + '0 1'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)


    elif modusreset != 1:
        serial_port.write(str.encode('set-config ' + '0 0'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
		
def Set_WakeUpAlarm(sp3_alarm_enable):
    if (sp3_alarm_enable == "1") or (sp3_alarm_enable == "0"):
        if type(sp3_alarm_enable) == str:
            serial_port.write(str.encode('set-config ' + '13 ' + sp3_alarm_enable))
        else:
            serial_port.write(str.encode('set-config ' + '13 ' + sp3_alarm_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
def Set_Intervalmode(sp3_intervalAlarm):
    if (sp3_intervalAlarm == "1") or (sp3_intervalAlarm == "0"):
        if type(sp3_intervalAlarm) == str:
            serial_port.write(str.encode('set-config ' + '19 ' + sp3_intervalAlarm))
        else:
            serial_port.write(str.encode('set-config ' + '19 ' + sp3_intervalAlarm.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

def Set_Alarm_Poweroff(sp3_alarmPoweroff):
    if (sp3_alarmPoweroff == "1") or (sp3_alarmPoweroff == "0"):
        if type(sp3_alarmPoweroff) == str:
            serial_port.write(str.encode('set-config ' + '5 ' +  sp3_alarmPoweroff))
        else:
            serial_port.write(str.encode('set-config ' + '5 ' + sp3_alarmPoweroff.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

def Set_Alarm_min(sp3_alarm_min, Alarm_Powerofffailmin):
    sp3_alarm_min = ''.join([i for i in sp3_alarm_min if i.isdigit()])
    if sp3_alarm_min.isdigit():
        sp3_alarm_minint = int(sp3_alarm_min)
        if (sp3_alarm_minint < 61) and (sp3_alarm_minint >= 0): 
            serial_port.write(str.encode('set-config ' + '8 ' +  sp3_alarm_min))
        else:
            Alarm_Powerofffailmin = 1
    else:
        Alarm_Powerofffailmin = 1		
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

def Set_Alarm_hour(sp3_alarm_hour):
    sp3_alarm_hour = ''.join([i for i in sp3_alarm_hour if i.isdigit()])
    if sp3_alarm_hour.isdigit():
        sp3_alarm_hourint = int(sp3_alarm_hour)
        if (sp3_alarm_hourint < 25) and (sp3_alarm_hourint >= 0): 
            serial_port.write(str.encode('set-config ' + '9 ' +  sp3_alarm_hour))
        else:
            Alarm_Powerofffailhour = 1
    else:
        Alarm_Powerofffailhour = 1      
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)	
    
def Set_Alarm_hour_off(sp3_alarm_hour_off):
    sp3_alarm_hour_off = ''.join([i for i in sp3_alarm_hour_off if i.isdigit()])
    if sp3_alarm_hour_off.isdigit():
        sp3_alarm_hour_off2 = int(sp3_alarm_hour_off)
        if (sp3_alarm_hour_off2 < 61) and (sp3_alarm_hour_off2 >= 0):
            serial_port.write(str.encode('set-config ' + '7 ' + str(sp3_alarm_hour_off)))
        else:
            ShutdownTimeError = 1 #("You can only use Digits between 0 and 65535 for the shutdown timer")
    else:
        ShutdownTimeError = 1 #("You can only use Digits between 0 and 65535 for the shutdown timer")
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)   
	
def Set_Alarm_min_off(sp3_alarm_min_off):
    sp3_alarm_min_off = ''.join([i for i in sp3_alarm_min_off if i.isdigit()])
    if sp3_alarm_min_off.isdigit():
        sp3_alarm_min_off2 = int(sp3_alarm_min_off)
        if (sp3_alarm_min_off2 < 61) and (sp3_alarm_min_off2 >= 0):
            serial_port.write(str.encode('set-config ' + '6 ' + str(sp3_alarm_min_off)))
        else:
            ShutdownTimeError = 1 #("You can only use Digits between 0 and 65535 for the shutdown timer")
    else:
        ShutdownTimeError = 1 #("You can only use Digits between 0 and 65535 for the shutdown timer")
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL) 
	
def Set_Alarm_Day(sp3_alarm_day):
    sp3_alarm_day = ''.join([i for i in sp3_alarm_day if i.isdigit()])
    if sp3_alarm_day.isdigit():
        sp3_alarm_dayint = int(sp3_alarm_day)
        if (sp3_alarm_dayint <= 31) and (sp3_alarm_dayint >= 0): 
            serial_port.write(str.encode('set-config ' + '10 ' +  sp3_alarm_day))
        else:
            Alarm_Dayerror = 1
    else:
        Alarm_Dayerror = 1      
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)	
	
def Set_Alarm_Weekday(sp3_alarm_weekday):
    if sp3_alarm_weekday.isdigit():
        serial_port.write(str.encode('set-config ' + '12 ' + sp3_alarm_weekday))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

def Set_IntervalAlarmOffTime(sp3_intervalAlarmOffTime): #21
    sp3_intervalAlarmOffTime = ''.join([i for i in sp3_intervalAlarmOffTime if i.isdigit()])
    if sp3_intervalAlarmOffTime.isdigit():
        sp3_intervalAlarmOffTimeint = int(sp3_intervalAlarmOffTime)
        if (sp3_intervalAlarmOffTimeint < 65535) and (sp3_intervalAlarmOffTimeint > 0):
            serial_port.write(str.encode('set-config ' + '21 ' + str(sp3_intervalAlarmOffTime)))
        else:
            IntervalOffTimeError = 1 
    else:
        IntervalOffTimeError = 1 
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
def Set_IntervalAlarmOnTime(sp3_intervalAlarmOnTime): #20
    sp3_intervalAlarmOnTime = ''.join([i for i in sp3_intervalAlarmOnTime if i.isdigit()])
    if sp3_intervalAlarmOnTime.isdigit():
        sp3_intervalAlarmOnTimeint = int(sp3_intervalAlarmOnTime)
        if (sp3_intervalAlarmOnTimeint < 65535) and (sp3_intervalAlarmOnTimeint > 0):
            serial_port.write(str.encode('set-config ' + '20 ' + str(sp3_intervalAlarmOnTime)))
        else:
            IntervalOnTimeError = 1 
    else:
        IntervalOnTimeError = 1 
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
def Set_RTC():
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
		
def Set_RTC_Manual(SetClockHstr, SetClockMstr, SetDateDstr, SetDateM, SetDateWD, SetDateYstr):
    SetDateWDstr = str(SetDateWD)
    SetDateMstr = ''.join([i for i in SetDateM if i.isdigit()])
    SetClockHstr = ''.join([i for i in SetClockHstr if i.isdigit()])
    SetClockMstr = ''.join([i for i in SetClockMstr if i.isdigit()])
    SetDateDstr = ''.join([i for i in SetDateDstr if i.isdigit()])
    SetDateYstr = ''.join([i for i in SetDateYstr if i.isdigit()])
    if (SetDateWDstr == "1 = Monday") or (SetDateWDstr == "Monday"):
        SetDateWDstr = "1"
    if (SetDateWDstr == "2 = Tuesday") or (SetDateWDstr == "Tuesday"):
        SetDateWDstr = "2"
    if (SetDateWDstr == "3 = Wednesday") or (SetDateWDstr == "Wednesday"):
        SetDateWDstr = "3"
    if (SetDateWDstr == "4 = Thursday") or (SetDateWDstr == "Thursday"):
        SetDateWDstr = "4"
    if (SetDateWDstr == "5 = Friday") or (SetDateWDstr == "Friday"):
        SetDateWDstr = "5"
    if (SetDateWDstr == "6 = Saturday") or (SetDateWDstr == "Saturday"):
        SetDateWDstr = "6"
    if (SetDateWDstr == "7 = Sunday") or (SetDateWDstr == "Sunday"):
        SetDateWDstr = "7"
    if SetDateWDstr.isdigit():
        SetDateWD = int(SetDateWDstr)
        if (SetDateWD <= 7) and (SetDateWD >= 1):
            SetDateWDError = 0
        else:
            SetDateWDError = 1
    else:
        SetDateWDError = 1
		
		
    SetDateM = int(SetDateMstr)

    SetDateD = 0
    SetDateY = 0
    SetClockM = 0
    SetClockH = 0


    SetClockS = '00'
    if SetClockHstr.isdigit():
        SetClockH = int(SetClockHstr)
        if (SetClockH < 24) and (SetClockH >= 0):
            SetClockHError = 0
        else:
            SetClockHError = 1
    else:
        SetClockHError = 1
    if SetClockMstr.isdigit():
        SetClockM = int(SetClockMstr)
        if (SetClockM < 60) and (SetClockM >= 0):
            SetClockMError = 0
        else:
            SetClockMError = 1
    else:
        SetClockMError = 1

    if SetDateDstr.isdigit():
        SetDateD = int(SetDateDstr)
        if (SetDateD < 32) and (SetDateD >= 1):
            SetDateDError = 0
        else:
            SetDateDError = 1
    else:
        SetDateDError = 1
    if SetDateYstr.isdigit():
        SetDateY = int(SetDateYstr)
        if (SetDateY <= 99) and (SetDateY >= 0):
            SetDateYError = 0
        else:
            SetDateYError = 1
    else:
        SetDateYError = 1
    if (SetDateM <= 12) and (SetDateM >= 1):
        SetDateMError = 0
    else:
        SetDateMError = 1
		



    if (SetClockHError == 0) and (SetClockMError == 0) and (SetDateWDError == 0) and (SetDateDError == 0) and (SetDateMError == 0) and (SetDateYError == 0):
        serial_port.write(str.encode('quit'))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-date ' + SetDateDstr + ' ' + SetDateMstr + ' ' + SetDateYstr + ' ' + SetDateWDstr))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)

        serial_port.write(str.encode('set-clock ' + SetClockHstr + ' ' + SetClockMstr + ' ' + SetClockS))
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)
    else:
        sleep(breakS)
        serial_port.write(str.encode('\x0D'))
        sleep(breakL)	
    Refresh_Status()

def SetDateYFocusIn(SetDateYstr):
    SetDateYstr = tkSetDateY.get()
    SetDateYstr = ''.join([i for i in SetDateYstr if i.isdigit()])
    tkSetDateY.set(SetDateYstr)
	
def SetDateYFocusOut(SetDateYstr):
    SetDateYstr = ''.join([i for i in SetDateYstr if i.isdigit()])
    tkSetDateY.set(SetDateYstr + " Year")

def SetDateDFocusIn(SetDateDstr):
    SetDateDstr = tkSetDateD.get()
    SetDateDstr = ''.join([i for i in SetDateDstr if i.isdigit()])
    tkSetDateD.set(SetDateDstr) 

def SetDateDFocusOut(SetDateDstr):
    SetDateDstr = ''.join([i for i in SetDateDstr if i.isdigit()])
    tkSetDateD.set(SetDateDstr + " Day")
	
def SetClockHFocusIn(SetClockHstr):
    SetClockHstr = tkSetClockH.get()
    SetClockHstr = ''.join([i for i in SetClockHstr if i.isdigit()])
    tkSetClockH.set(SetClockHstr) 
	
def SetClockHFocusOut(SetClockHstr):
    SetClockHstr = ''.join([i for i in SetClockHstr if i.isdigit()])
    tkSetClockH.set(SetClockHstr + " Hours")
	
def SetClockMFocusIn(SetClockMstr):
    SetClockMstr = tkSetClockM.get()
    SetClockMstr = ''.join([i for i in SetClockMstr if i.isdigit()])
    tkSetClockM.set(SetClockMstr) 
	
def SetClockMFocusOut(SetClockMstr):
    SetClockMstr = ''.join([i for i in SetClockMstr if i.isdigit()])
    tkSetClockM.set(SetClockMstr + " Minutes")
	
def Set_PowerSaveMode(sp3_powersave_enable):
    if (sp3_powersave_enable == "1") or (sp3_powersave_enable == "0"):
        if type(sp3_powersave_enable) == str:
            serial_port.write(str.encode('set-config ' + '24 ' + sp3_powersave_enable))
        else:
            serial_port.write(str.encode('set-config ' + '24 ' + sp3_powersave_enable.decode(encoding='UTF-8', errors='strict')))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

def Set_powerofftimer(sp3_poweroff_time):
    sp3_poweroff_time = ''.join([i for i in sp3_poweroff_time if i.isdigit()])
    if sp3_poweroff_time.isdigit():
        sp3_poweroff_timeint = int(sp3_poweroff_time)
        if (sp3_poweroff_timeint < 65535) and (sp3_poweroff_timeint > 0):
            serial_port.write(str.encode('set-config ' + '27 ' + str(sp3_poweroff_time)))
        else:
            powerOffTimeError = 1 
    else:
        powerOffTimeError = 1 
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
def Upload_to_StromPi():
    sp3_powerOnButton_timestr = tkButton_time.get()
    sp3_modusstr = tkmode.get()
    sp3_shutdown_enablestr = tkShutdownMode.get()
    sp3_batLevel_shutdownstr = tkBatShutdown.get()
    sp3_serialLessModestr = tkSerialless.get()
    sp3_warning_enablestr = tkPowerfailWarning.get()
    sp3_powerOnButton_enablestr = tkPoweronButton.get()
    sp3_shutdown_timestr = tkshutdown_time.get()
    sp3_alarm_modestr = tkAlarm_Mode.get()
    sp3_alarm_enablestr = tkWakeupAlarm.get()
    sp3_intervalAlarmstr = tkIntervalAlarm.get()
    sp3_alarmPoweroffstr = tkAlarmPoweroff.get()
    sp3_alarm_min = tkAlarmPoweroffmin.get()
    sp3_alarm_hour = tkAlarmPoweroffhour.get()
    sp3_alarm_day = tkAlarmPoweroffday.get()
    sp3_alarm_weekdaystr = tkAlarmPoweroffweekday.get()
    sp3_alarm_monthstr = tkAlarmPoweroffmonth.get()
    sp3_alarm_min_off = tkAlarmminoff.get()
    sp3_alarm_hour_off = tkAlarmhouroff.get()
    sp3_intervalAlarmOnTime = tkIntervalAlarmOnTime.get()
    sp3_intervalAlarmOffTime = tkIntervalAlarmOffTime.get()
    sp3_timesetting = tkTimeSync.get()
    TimeSyncRB1test = TimeSyncRB1.get()
    sp3_powersave_enablestr = tkPowerSave.get()
    sp3_poweroffModestr = tkPoweroffMode.get()
    sp3_wakeupweekend_enablestr = tkwakeupweekend_enable.get()	
	
    sp3_wakeupweekend_enable = sp3_wakeupweekend_enablestr[0]
    sp3_alarmPoweroff = sp3_alarmPoweroffstr[0]
    sp3_alarm_weekday = sp3_alarm_weekdaystr[0]
    sp3_alarm_month = sp3_alarm_monthstr[0]
    sp3_alarm_month2 = sp3_alarm_monthstr[1]
    sp3_modus = sp3_modusstr[0]
    sp3_modus_temp = sp3_modus
    sp3_serialLessMode = sp3_serialLessModestr[0]
    sp3_batLevel_shutdown = sp3_batLevel_shutdownstr[0]
    sp3_warning_enable = sp3_warning_enablestr[0]
    sp3_powerOnButton_enable = sp3_powerOnButton_enablestr[0]
    sp3_shutdown_enable = sp3_shutdown_enablestr[0]
    sp3_alarm_mode = sp3_alarm_modestr[0]
    sp3_alarm_enable = sp3_alarm_enablestr [0]
    sp3_intervalAlarm = sp3_intervalAlarmstr [0]
    sp3_powersave_enable = sp3_powersave_enablestr [0]
    sp3_poweroffMode = sp3_poweroffModestr [0]
    SetClockHstr = tkSetClockH.get()
    SetClockMstr = tkSetClockM.get()
    SetDateDstr = tkSetDateD.get()
    SetDateM = tkSetDateM.get()
    SetDateWD = tkSetDateWD.get()
    SetDateYstr = tkSetDateY.get()
    sp3_poweroff_time = tkPoweroff_time.get()


    breakS = 0.1
    breakL = 0.2
    
    if serial_port.isOpen(): serial_port.close()
    serial_port.open()

    serial_port.write(str.encode('quit'))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
    
    if TimeSyncRB1test == 2:
        Set_RTC()
    elif TimeSyncRB1test == 3:
        Set_RTC_Manual(SetClockHstr, SetClockMstr, SetDateDstr, SetDateM, SetDateWD, SetDateYstr)
	
    if (sp3_modus == "0") or (sp3_modus == "1") or (sp3_modus == "2") or (sp3_modus == "3") or (sp3_modus == "4") or (sp3_modus == "5") or (sp3_modus == "6"):
        modusreset = 1
        serial_port.write(str.encode('set-config ' + '1 ' +  sp3_modus))
    else:
        modusreset = 0
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
        
    Set_Alarm_Mode(sp3_alarm_mode) #2-4 and 26
	
    Set_Alarm_Poweroff(sp3_alarmPoweroff) #5
	
    Set_Alarm_min(sp3_alarm_min, Alarm_Powerofffailmin) #6

    Set_Alarm_hour(sp3_alarm_hour) #7
	
    Set_Alarm_min_off(sp3_alarm_min_off) #8

    Set_Alarm_hour_off(sp3_alarm_hour_off) #9
     		
    Set_Alarm_Day(sp3_alarm_day) #10
	

    if sp3_alarm_month2 == "1":
        serial_port.write(str.encode('set-config ' + '11 ' + '11'))
    elif sp3_alarm_month2 == "0":
        serial_port.write(str.encode('set-config ' + '11 ' + '10'))
    elif sp3_alarm_month2 == "2":
        serial_port.write(str.encode('set-config ' + '11 ' + '12'))
    else:
        serial_port.write(str.encode('set-config ' + '11 ' + sp3_alarm_month))
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
    Set_Alarm_Weekday(sp3_alarm_weekday) #12
    
    Set_WakeUpAlarm(sp3_alarm_enable) #13
     
    Set_Shutdown_enable(sp3_shutdown_enable) #14
    sp3_shutdown_timestr = ''.join([i for i in sp3_shutdown_timestr if i.isdigit()])
    if sp3_shutdown_timestr.isdigit():
        sp3_shutdown_time = int(sp3_shutdown_timestr)
        if (sp3_shutdown_time < 65535) and (sp3_shutdown_time > 0):
            serial_port.write(str.encode('set-config ' + '15 ' + str(sp3_shutdown_time)))
        else:
            ShutdownTimeError = 1 
    else:
        ShutdownTimeError = 1 
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)    
		
    Set_Warning_enable(sp3_warning_enable) #16
        
    Set_Serialless_mode(sp3_serialLessMode) #17
        
    Set_Batlevel_Shutdown(sp3_batLevel_shutdown) #18
	
    Set_Intervalmode(sp3_intervalAlarm) #19
	
    Set_IntervalAlarmOnTime(sp3_intervalAlarmOnTime) #20
	
    Set_IntervalAlarmOffTime(sp3_intervalAlarmOffTime) #21

    Set_PoweronButton(sp3_powerOnButton_enable) #22
    
    sp3_powerOnButton_timestr = ''.join([i for i in sp3_powerOnButton_timestr if i.isdigit()])
    if sp3_powerOnButton_timestr.isdigit():
        sp3_powerOnButton_time = int(sp3_powerOnButton_timestr)
        if (sp3_powerOnButton_time < 65535) and (sp3_powerOnButton_time > 0):
            serial_port.write(str.encode('set-config ' + '23 ' + str(sp3_powerOnButton_time)))
        else:
            ButtonTimeError = 1 #("You can only use Digits between 0 and 65535 for the Button timer")
    else:
        ButtonTimeError = 1 #("You can only use Digits between 0 and 65535 for the Button timer")
			
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)
	
    Set_PowerSaveMode(sp3_powersave_enable) #24
	
    Set_PoweroffMode(sp3_poweroffMode) #25
	
    Set_powerofftimer(sp3_poweroff_time)#27
	
    Set_wakeupweekend_enable(sp3_wakeupweekend_enable)#28

    Use_Modusreset(modusreset)
     
    Refresh_Status()

def Refresh_Status():

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
    sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    sleep(breakL)

    serial_port.write(str.encode('status-rpi'))
    sleep(1)
    serial_port.write(str.encode('\x0D'))
    sp3_time = serial_port.readline(9999);
    sp3_date = serial_port.readline(9999);
    sp3_weekday = serial_port.readline(9999);
    sp3_modus = serial_port.readline(9999);
    sp3_alarm_enable = serial_port.readline(9999);
    sp3_alarm_mode = serial_port.readline(9999);
    sp3_alarm_hour = serial_port.readline(9999);
    sp3_alarm_min = serial_port.readline(9999);
    sp3_alarm_day = serial_port.readline(9999);
    sp3_alarm_month = serial_port.readline(9999);
    sp3_alarm_weekday = serial_port.readline(9999);
    sp3_alarmPoweroff = serial_port.readline(9999);
    sp3_alarm_hour_off = serial_port.readline(9999);
    sp3_alarm_min_off = serial_port.readline(9999);
    sp3_shutdown_enable = serial_port.readline(9999);
    sp3_shutdown_time = serial_port.readline(9999);
    sp3_warning_enable = serial_port.readline(9999);
    sp3_serialLessMode = serial_port.readline(9999);
    sp3_intervalAlarm = serial_port.readline(9999);
    sp3_intervalAlarmOnTime = serial_port.readline(9999);
    sp3_intervalAlarmOffTime = serial_port.readline(9999);
    sp3_batLevel_shutdown = serial_port.readline(9999);
    sp3_batLevel = serial_port.readline(9999);
    sp3_charging = serial_port.readline(9999);
    sp3_powerOnButton_enable = serial_port.readline(9999);
    sp3_powerOnButton_time = serial_port.readline(9999);
    sp3_powersave_enable = serial_port.readline(9999);
    sp3_poweroffMode = serial_port.readline(9999);
    sp3_poweroff_time_enable = serial_port.readline(9999);
    sp3_poweroff_time = serial_port.readline(9999);
    sp3_wakeupweekend_enable = serial_port.readline(9999);
    sp3_ADC_Wide = float(serial_port.readline(9999))/1000;
    sp3_ADC_BAT = float(serial_port.readline(9999))/1000;
    sp3_ADC_USB = float(serial_port.readline(9999))/1000;
    sp3_ADC_OUTPUT = float(serial_port.readline(9999))/1000;
    sp3_output_status = serial_port.readline(9999);
    sp3_powerfailure_counter = serial_port.readline(9999);
    sp3_firmwareVersion = serial_port.readline(9999);
	
   
	
    sp3_modus_temp = int(sp3_modus)
	
    strompi_year = int(sp3_date) // 10000
    strompi_month = int(sp3_date) % 10000 // 100
    strompi_day = int(sp3_date) % 100

    strompi_hour = int(sp3_time) // 10000
    strompi_min = int(sp3_time) % 10000 // 100
    strompi_sec = int(sp3_time) % 100


    sp3_poweroff_time_enable = int(sp3_poweroff_time_enable.decode())
    if sp3_poweroff_time_enable == 1:
        sp3_alarm_mode = "4"
    tkmode.set(strompi_mode_converter((int(sp3_modus))))
    tkshutdown_time.set(str(sp3_shutdown_time, 'utf-8').rstrip('\n') + ' Seconds')
    tkButton_time.set(str(sp3_powerOnButton_time, 'utf-8').rstrip('\n') + ' Seconds')
    tkShutdownMode.set(enabled_disabled_converter(int(sp3_shutdown_enable)))
    tkBatShutdown.set(batterylevel_shutdown_converter(int(sp3_batLevel_shutdown)))
    tkSerialless.set(enabled_disabled_converter(int(sp3_serialLessMode)))
    tkPowerfailWarning.set(enabled_disabled_converter(int(sp3_warning_enable)))
    tkPoweronButton.set(enabled_disabled_converter(int(sp3_powerOnButton_enable)))
    tkAlarm_Mode.set('Alarm-Mode: ' + alarm_mode_converter(int(sp3_alarm_mode)))
    tkPowerSave.set('Power Save Mode: ' + enabled_disabled_converter(int(sp3_powersave_enable)))
    tkwakeupweekend_enable.set('Weekend Wakeup: ' + enabled_disabled_converter(int(sp3_wakeupweekend_enable)))
    #tkTimeSync.set('No Change')
    tkWakeupAlarm.set('WakeUp-Alarm: ' + enabled_disabled_converter(int(sp3_alarm_enable)))
    tkIntervalAlarm.set('Interval-Alarm: ' + enabled_disabled_converter(int(sp3_intervalAlarm)))
    tkAlarmPoweroff.set('PowerOff-Alarm: ' + enabled_disabled_converter(int(sp3_alarmPoweroff)))
    tkAlarmPoweroffmin.set(str(sp3_alarm_min_off, 'utf-8').rstrip('\n').zfill(2) + ' Minutes')
    tkAlarmPoweroffhour.set(str(sp3_alarm_hour_off, 'utf-8').rstrip('\n').zfill(2) + ' Hours')
    tkAlarmPoweroffmonth.set(str(sp3_alarm_month, 'utf-8').rstrip('\n').zfill(2))
    tkAlarmPoweroffweekday.set(weekday_converter(int(sp3_alarm_weekday)))
    tkAlarmPoweroffday.set(str(sp3_alarm_day, 'utf-8').rstrip('\n').zfill(2) + ' Day')
    tkAlarmhouroff.set(str(sp3_alarm_hour, 'utf-8').rstrip('\n').zfill(2) + ' Hours')
    tkAlarmminoff.set(str(sp3_alarm_min, 'utf-8').rstrip('\n').zfill(2) + ' Minutes')
    tkIntervalAlarmOffTime.set(str(sp3_intervalAlarmOffTime, 'utf-8').rstrip('\n').zfill(2) + ' Minutes')
    tkIntervalAlarmOnTime.set(str(sp3_intervalAlarmOnTime, 'utf-8').rstrip('\n').zfill(2) + ' Minutes')
    tkSetClockH.set(str(strompi_hour).zfill(2) + ' Hours')
    tkSetClockM.set(str(strompi_min).zfill(2) + ' Minutes')
    tkSetDateD.set(str(strompi_day).zfill(2) + ' Day')
    tkSetDateM.set(str(strompi_month).zfill(2))
    tkSetDateWD.set(weekday_converter(int(sp3_weekday)))
    tkSetDateY.set(str(strompi_year).zfill(2) + ' Year')
    tkPoweroffMode.set('Poweroff Mode: ' + enabled_disabled_converter(int(sp3_poweroffMode)))
    tkPoweroff_time.set(str(sp3_poweroff_time, 'utf-8').rstrip('\n').zfill(2) + ' Minutes')
	
    serial_port.close()

def alarmPoweroffhourFocusIn(alarmPoweroffhour):
    alarmPoweroffhour = tkAlarmPoweroffhour.get()
    alarmPoweroffhour = ''.join([i for i in alarmPoweroffhour if i.isdigit()])
    tkAlarmPoweroffhour.set(alarmPoweroffhour) 
	
def alarmPoweroffhourFocusOut(alarmPoweroffhour):
    alarmPoweroffhour = ''.join([i for i in alarmPoweroffhour if i.isdigit()])
    tkAlarmPoweroffhour.set(alarmPoweroffhour + " Hours")

def alarmPoweroffminFocusIn(alarmPoweroffmin):
    alarmPoweroffmin = tkAlarmPoweroffmin.get()
    alarmPoweroffmin = ''.join([i for i in alarmPoweroffmin if i.isdigit()])
    tkAlarmPoweroffmin.set(alarmPoweroffmin) 
	
def alarmPoweroffminFocusOut(alarmPoweroffmin):
    alarmPoweroffmin = ''.join([i for i in alarmPoweroffmin if i.isdigit()])
    tkAlarmPoweroffmin.set(alarmPoweroffmin + " Minutes")

def alarmPoweroffdayFocusIn(alarmPoweroffday):
    alarmPoweroffday = tkAlarmPoweroffday.get()
    alarmPoweroffday = ''.join([i for i in alarmPoweroffday if i.isdigit()])
    tkAlarmPoweroffday.set(alarmPoweroffday) 
	
def alarmPoweroffdayFocusOut(alarmPoweroffday):
    alarmPoweroffday = ''.join([i for i in alarmPoweroffday if i.isdigit()])
    tkAlarmPoweroffday.set(alarmPoweroffday + " Day")

def WakeUpMinFocusIn(WakeUpMin):
    WakeUpMin = tkAlarmminoff.get()
    WakeUpMin = ''.join([i for i in WakeUpMin if i.isdigit()])
    tkAlarmminoff.set(WakeUpMin) 
	
def WakeUpMinFocusOut(WakeUpMin):
    WakeUpMin = ''.join([i for i in WakeUpMin if i.isdigit()])
    tkAlarmminoff.set(WakeUpMin + " Minutes")

def WakeUpHourFocusIn(WakeUpHour):
    WakeUpHour = tkAlarmhouroff.get()
    WakeUpHour = ''.join([i for i in WakeUpHour if i.isdigit()])
    tkAlarmhouroff.set(WakeUpHour) 
	
def WakeUpHourFocusOut(WakeUpHour):
    WakeUpHour = ''.join([i for i in WakeUpHour if i.isdigit()])
    tkAlarmhouroff.set(WakeUpHour + " Hours")
	
def AlarmminonFocusIn(IntervalAlarmOnTime):
    IntervalAlarmOnTime = tkIntervalAlarmOnTime.get()
    IntervalAlarmOnTime = ''.join([i for i in IntervalAlarmOnTime if i.isdigit()])
    tkIntervalAlarmOnTime.set(IntervalAlarmOnTime) 
	
def AlarmminonFocusOut(IntervalAlarmOnTime):
    IntervalAlarmOnTime = ''.join([i for i in IntervalAlarmOnTime if i.isdigit()])
    tkIntervalAlarmOnTime.set(IntervalAlarmOnTime + " Minutes")
	
def AlarmminoffFocusIn(IntervalAlarmOffTime):
    IntervalAlarmOffTime = tkIntervalAlarmOffTime.get()
    IntervalAlarmOffTime = ''.join([i for i in IntervalAlarmOffTime if i.isdigit()])
    tkIntervalAlarmOffTime.set(IntervalAlarmOffTime) 
	
def AlarmminoffFocusOut(IntervalAlarmOffTime):
    IntervalAlarmOffTime = ''.join([i for i in IntervalAlarmOffTime if i.isdigit()])
    tkIntervalAlarmOffTime.set(IntervalAlarmOffTime + " Minutes")
	
def ShutdownTimeFocusIn(ShutdownTime):
    ShutdownTime = tkshutdown_time.get()
    ShutdownTime = ''.join([i for i in ShutdownTime if i.isdigit()])
    tkshutdown_time.set(ShutdownTime) 
	
def ShutdownTimeFocusOut(ShutdownTime):
    ShutdownTime = ''.join([i for i in ShutdownTime if i.isdigit()])
    tkshutdown_time.set(ShutdownTime + " Seconds")
	
def PoweronButtonTimeFocusIn(PoweronButtonTime):
    PoweronButtonTime = tkButton_time.get()
    PoweronButtonTime = ''.join([i for i in PoweronButtonTime if i.isdigit()])
    tkButton_time.set(PoweronButtonTime) 
	
def PoweronButtonTimeFocusOut(PoweronButtonTime):
    PoweronButtonTime = ''.join([i for i in PoweronButtonTime if i.isdigit()])
    tkButton_time.set(PoweronButtonTime + " Seconds")
	
def PoweroffTimeFocusIn(Poweroff_time_tmp):
    Poweroff_time_tmp = tkPoweroff_time.get()
    Poweroff_time_tmp = ''.join([i for i in Poweroff_time_tmp if i.isdigit()])
    tkPoweroff_time.set(Poweroff_time_tmp)
	
def PoweroffTimeFocusOut(Poweroff_time_tmp):
    Poweroff_time_tmp = ''.join([i for i in Poweroff_time_tmp if i.isdigit()])
    tkPoweroff_time.set(Poweroff_time_tmp + " Minutes")
#----------------Graphic User Interface------------------------
fenster = tk.Tk()
fenster.title("Strompi V3 Serial Config Tool")
fenster.resizable(width="false", height="false")
fenster.minsize(width=250, height=250)
fenster.maxsize(width=2000, height=3000)
mainframe = Frame(fenster)
mainframe.configure(background="#275c6b")
mainframe.grid(column=2000,row=20, rowspan=20, columnspan=2000)
mainframe.columnconfigure(1000, weight = 1)
mainframe.rowconfigure(1000, weight = 1)
#Choice Variables
modechoices = [ '1 = mUSB -> Wide', '2 = Wide -> mUSB', '3 = mUSB -> Battery', '4 = Wide -> Battery', '5 = mUSB -> Wide -> Battery', '6 = Wide -> mUSB -> Battery']
EnableDisableChoice = [ '0 = disable' ,  '1 = enable']
BatShutdownChoices = ['0 = disable', '1 = below 10%', '2 = below 25%', '3 = below 50%']
TimeSyncChoices = ['No Change','Sync with StromPi3', 'Manual Setting']
Alarm_ModeChoices = ['1 = Daily time alarm', '2 = Date controlled time alarm', '3 = Weekly time alarm', '4 = Minute Wakeup-Alarm']
Month_Choices = ['1 = January', '2 = February', '3 = March', '4 = April', '5 = May', '6 = June', '7 = July', '8 = August', '9 = September', '10 = October', '11 = November', '12 = December'] 
Day_Choices = ['1 = Monday', '2 = Tuesday', '3 = Wednesday', '4 = Thursday', '5 = Friday', '6 = Saturday', '7 = Sunday']
#Create Variables
tkshutdown_time = StringVar(fenster)
tkButton_time = StringVar(fenster)
tkmode = StringVar(fenster)
tkShutdownMode = StringVar(fenster)
tkBatShutdown = StringVar(fenster)
tkSerialless = StringVar(fenster)
tkPowerfailWarning = StringVar(fenster)
tkPoweronButton = StringVar(fenster)
tkTimeSync = StringVar(fenster)
tkSetClockH = StringVar(fenster)
tkSetClockM = StringVar(fenster)
tkSetDateD = StringVar(fenster)
tkSetDateM = StringVar(fenster)
tkSetDateWD = StringVar(fenster)
tkSetDateY = StringVar(fenster)
tkAlarm_Mode = StringVar(fenster)
tkIntervalAlarm = StringVar(fenster)
tkWakeupAlarm = StringVar(fenster)
tkAlarmPoweroff = StringVar(fenster)
tkAlarmPoweroffmin = StringVar(fenster)
tkAlarmPoweroffhour = StringVar(fenster)
tkAlarmPoweroffweekday = StringVar(fenster)
tkAlarmPoweroffmonth = StringVar(fenster)
tkAlarmPoweroffday = StringVar(fenster)
tkAlarmminoff = StringVar(fenster)
tkAlarmhouroff = StringVar(fenster)
tkIntervalAlarmOnTime = StringVar(fenster)
tkIntervalAlarmOffTime = StringVar(fenster)
tkPowerSave = StringVar(fenster)
tkPoweroffMode = StringVar(fenster)
tkPoweroff_time = StringVar(fenster)
tkwakeupweekend_enable = StringVar(fenster)
#Frames
SetClockFrame1 = LabelFrame(mainframe, text="Real Time Clock Settings", fg="snow", bg="#275c6b")
SetClockFrame1.grid(row = 1, column = 1, columnspan=3, rowspan=1, padx=30, pady=20, sticky=NW)
EnableDisableFrame = LabelFrame(mainframe, text="Options Without Timesettings:", fg="snow", bg="#275c6b")
EnableDisableFrame.grid(row = 1, column = 0, columnspan=1, rowspan=1, sticky=W, padx=30, pady=10)
SetShutdownFrame = LabelFrame(mainframe, text="Shutdown Timer", fg="snow", bg="#275c6b")
SetShutdownFrame.grid(row = 1, column = 1, columnspan=2, rowspan=1, sticky=SW, padx=30, pady=10)
PowerOnButtonFrame = LabelFrame(mainframe, text="PowerOnButton", fg="snow", bg="#275c6b")
PowerOnButtonFrame.grid(row = 2, column = 1, columnspan=2, rowspan=1, sticky=W, padx=30, pady=10)
IntervalAlarmFrame = LabelFrame(mainframe, text="Interval Timer", fg="snow", bg="#275c6b")
IntervalAlarmFrame.grid(row = 4, column = 0, columnspan=3, rowspan=1, sticky=W, padx=30, pady=10)
AlarmModeFrame = LabelFrame(mainframe, text="Alarm Modes", fg="snow", bg="#275c6b")
AlarmModeFrame.grid(row = 3, column = 0, columnspan=3, rowspan=1, sticky=W, padx=30, pady=10)
PowerOffModeFrame = LabelFrame(mainframe, text="Poweroff Mode", fg="snow", bg="#275c6b")
PowerOffModeFrame.grid(row = 2, column = 0, columnspan=1, rowspan=1, sticky=W, padx=30, pady=10)
#Create GUI Objects
#--------------------------------------------------------------------------------------------------------------
#sp3_poweroff_time GUI OBJECTS
poweroff_timelbl = Label(AlarmModeFrame, text="Minute Wakeup Time:", fg="snow", bg="#275c6b").grid(row = 18, column = 3, columnspan=1, rowspan=1, sticky=W)
poweroff_timeEntry = Entry(AlarmModeFrame, textvariable=tkPoweroff_time)
poweroff_timeEntry.grid(row = 19, column = 3, columnspan=1, rowspan=1, sticky=W)
poweroff_timeEntry.insert(0, "0")
poweroff_timeEntry.bind("<FocusIn>", (lambda event: PoweroffTimeFocusIn(tkPoweroff_time.get())))
poweroff_timeEntry.bind("<FocusOut>", (lambda event: PoweroffTimeFocusOut(tkPoweroff_time.get())))
#Powerpath GUI Objects
modepopupMenu = OptionMenu(EnableDisableFrame, tkmode, *modechoices)
modepopupMenu.configure(background="snow")
modelbl = Label(EnableDisableFrame, text="Choose StromPi V3 Powerpath Mode:", fg="snow", bg="#275c6b").grid(row = 0, column = 0, columnspan=1, rowspan=1, sticky=W)
modepopupMenu.grid(row = 1, column =0, columnspan=1, rowspan=1, sticky=W)
#Shutdown Mode GUI Objects
ShutdownModepopupMenu = OptionMenu(SetShutdownFrame, tkShutdownMode, *EnableDisableChoice)
ShutdownModelbl = Label(SetShutdownFrame, text="Choose Shutdown Mode:                    ", fg="snow", bg="#275c6b").grid(row = 8, column = 0, columnspan=1, rowspan=1, sticky=W)
ShutdownModepopupMenu.grid(row = 9, column =0, columnspan=1, rowspan=1, sticky=W)
ShutdownModepopupMenu.configure(background="snow")
#Batery Level Shutdown GUI Objects
BatShutdownpopupMenu = OptionMenu(EnableDisableFrame, tkBatShutdown, *BatShutdownChoices)
BatShutdownlbl = Label(EnableDisableFrame, text="Choose Battery Shutdown Mode:", fg="snow", bg="#275c6b").grid(row = 4, column = 0, columnspan=1, rowspan=1, sticky=W)
BatShutdownpopupMenu.grid(row = 5, column =0, columnspan=1, rowspan=1, sticky=W)
BatShutdownpopupMenu.configure(background="snow")
#Serialless GUI Objects
SeriallesspopupMenu = OptionMenu(EnableDisableFrame, tkSerialless, *EnableDisableChoice)
Seriallesslbl = Label(EnableDisableFrame, text="Choose Serialless Mode:", fg="snow", bg="#275c6b").grid(row = 6, column = 0, columnspan=1, rowspan=1, sticky=W)
SeriallesspopupMenu.grid(row = 7, column =0, columnspan=1, rowspan=1, sticky=W)
SeriallesspopupMenu.configure(background="snow")
#Seriallesslbl.configure(background="snow")
PowerfailpopupMenu = OptionMenu(EnableDisableFrame, tkPowerfailWarning, *EnableDisableChoice)
Powerfaillbl = Label(EnableDisableFrame, text="Choose Powerfail Warning Mode:", fg="snow", bg="#275c6b").grid(row = 2, column = 0, columnspan=1, rowspan=1, sticky=W)
PowerfailpopupMenu.grid(row = 3, column =0, columnspan=1, rowspan=1, sticky=W)
PowerfailpopupMenu.configure(background="snow")
#PowerSaveMode GUI Objects
PowerSavepopupMenu = OptionMenu(EnableDisableFrame, tkPowerSave, *EnableDisableChoice)
PowerSavelbl = Label(EnableDisableFrame, text="Choose Power Save Mode:          ", fg="snow", bg="#275c6b").grid(row = 10, column = 0, columnspan=1, rowspan=1, sticky=W)
PowerSavepopupMenu.grid(row = 11, column =0, columnspan=1, rowspan=1, sticky=W)
PowerSavepopupMenu.configure(background="snow")
#sp3_wakeupweekend_enable GUI Objects
wakeupweekendpopupMenu = OptionMenu(AlarmModeFrame, tkwakeupweekend_enable, *EnableDisableChoice)
wakeupweekendlbl = Label(AlarmModeFrame, text="Activate WakeupAlarm on weekend?:", fg="snow", bg="#275c6b").grid(row = 20, column = 0, columnspan=1, rowspan=1, sticky=W)
wakeupweekendpopupMenu.grid(row = 21, column =0, columnspan=1, rowspan=1, sticky=W)
wakeupweekendpopupMenu.configure(background="snow")
#PowerOnButton GUI Objects
PoweronButtonpopupMenu = OptionMenu(PowerOnButtonFrame, tkPoweronButton, *EnableDisableChoice)
PoweronButtonlbl = Label(PowerOnButtonFrame, text="Choose PowerOn-Button Mode:          ", fg="snow", bg="#275c6b").grid(row = 10, column = 0, columnspan=1, rowspan=1, sticky=W)
PoweronButtonpopupMenu.grid(row = 11, column =0, columnspan=1, rowspan=1, sticky=W)
PoweronButtonpopupMenu.configure(background="snow")
#sp3_shutdown_time GUI OBJECTS
ShutdownTimelbl = Label(SetShutdownFrame, text="Choose Shutdown timer:          ", fg="snow", bg="#275c6b").grid(row = 8, column = 1, columnspan=1, rowspan=1, sticky=W)
ShutdownTimeEntry = Entry(SetShutdownFrame, textvariable=tkshutdown_time)
ShutdownTimeEntry.grid(row = 9, column = 1, columnspan=1, rowspan=1, sticky=W)
ShutdownTimeEntry.insert(0, "0")
ShutdownTimeEntry.bind("<FocusIn>", (lambda event: ShutdownTimeFocusIn(tkshutdown_time.get())))
ShutdownTimeEntry.bind("<FocusOut>", (lambda event: ShutdownTimeFocusOut(tkshutdown_time.get())))
#sp3_powerOnButton_time GUI OBJECTS
PoweronButtonTimelbl = Label(PowerOnButtonFrame, text="Choose Button Shutdown time:", fg="snow", bg="#275c6b").grid(row = 10, column = 1, columnspan=1, rowspan=1, sticky=W)
PoweronButtonTimeEntry = Entry(PowerOnButtonFrame, textvariable=tkButton_time)
PoweronButtonTimeEntry.grid(row = 11, column = 1, columnspan=1, rowspan=1, sticky=W)
PoweronButtonTimeEntry.insert(0, "0")
PoweronButtonTimeEntry.bind("<FocusIn>", (lambda event: PoweronButtonTimeFocusIn(tkButton_time.get())))
PoweronButtonTimeEntry.bind("<FocusOut>", (lambda event: PoweronButtonTimeFocusOut(tkButton_time.get())))
#Alarm-Mode GUI OBJECTS
Alarm_ModepopupMenu = OptionMenu(AlarmModeFrame, tkAlarm_Mode, *Alarm_ModeChoices)
Powerfaillbl = Label(AlarmModeFrame, text="Choose Alarm Mode:", fg="snow", bg="#275c6b").grid(row = 14, column = 0, columnspan=1, rowspan=1, sticky=W)
Alarm_ModepopupMenu.grid(row = 15, column =0, columnspan=1, rowspan=1, sticky=W)
Alarm_ModepopupMenu.configure(background="snow")
#sp3_intervalAlarm GUI OBJECTS
IntervalAlarmpopupMenu = OptionMenu(IntervalAlarmFrame, tkIntervalAlarm, *EnableDisableChoice)
IntervalAlarmlbl = Label(IntervalAlarmFrame, text="Choose Interval-Alarm Mode:                             ", fg="snow", bg="#275c6b").grid(row = 12, column = 0, columnspan=1, rowspan=1, sticky=W)
IntervalAlarmpopupMenu.grid(row = 13, column =0, columnspan=1, rowspan=1, sticky=W)
IntervalAlarmpopupMenu.configure(background="snow")
#sp3_alarm_enable GUI OBJECTS
WakeupAlarmpopupMenu = OptionMenu(AlarmModeFrame, tkWakeupAlarm, *EnableDisableChoice)
WakeupAlarmlbl = Label(AlarmModeFrame, text="Choose WakeUp-Alarm Mode:", fg="snow", bg="#275c6b").grid(row = 16, column = 0, columnspan=1, rowspan=1, sticky=W)
WakeupAlarmpopupMenu.grid(row = 17, column =0, columnspan=1, rowspan=1, sticky=W)
WakeupAlarmpopupMenu.configure(background="snow")
#sp3_alarmPoweroff GUI OBJECTS
alarmPoweroffpopupMenu = OptionMenu(AlarmModeFrame, tkAlarmPoweroff, *EnableDisableChoice)
alarmPowerofflbl = Label(AlarmModeFrame, text="Choose Power-Off Alarm Mode:                          ", fg="snow", bg="#275c6b").grid(row = 18, column = 0, columnspan=1, rowspan=1, sticky=W)
alarmPoweroffpopupMenu.grid(row = 19, column =0, columnspan=1, rowspan=1, sticky=W)
alarmPoweroffpopupMenu.configure(background="snow")
#sp3_poweroffMode GUI OBJECTS
poweroffModepopupMenu = OptionMenu(PowerOffModeFrame, tkPoweroffMode, *EnableDisableChoice)
poweroffModelbl = Label(PowerOffModeFrame, text="Choose Poweroff Mode:                      ", fg="snow", bg="#275c6b").grid(row = 18, column = 0, columnspan=1, rowspan=1, sticky=W)
poweroffModepopupMenu.grid(row = 19, column =0, columnspan=1, rowspan=1, sticky=W)
poweroffModepopupMenu.configure(background="snow")
#sp3_alarmPoweroff Minute GUI OBJECTS
alarmPoweroffminlbl = Label(AlarmModeFrame, text="Choose Power-Off Minutes:", fg="snow", bg="#275c6b").grid(row = 18, column = 1, columnspan=1, rowspan=1, sticky=W)
alarmPoweroffminEntry = Entry(AlarmModeFrame, textvariable=tkAlarmPoweroffmin)
alarmPoweroffminEntry.grid(row = 19, column = 1, columnspan=1, rowspan=1, sticky=W)
alarmPoweroffminEntry.insert(0, "0")
alarmPoweroffminEntry.bind("<FocusIn>", (lambda event: alarmPoweroffminFocusIn(tkAlarmPoweroffmin.get())))
alarmPoweroffminEntry.bind("<FocusOut>", (lambda event: alarmPoweroffminFocusOut(tkAlarmPoweroffmin.get())))
#sp3_alarmPoweroff Hour GUI OBJECTS
alarmPoweroffhourlbl = Label(AlarmModeFrame, text="Choose Power-Off Hours:", fg="snow", bg="#275c6b").grid(row = 18, column = 2, columnspan=1, rowspan=1, sticky=W)
alarmPoweroffhourEntry = Entry(AlarmModeFrame, textvariable=tkAlarmPoweroffhour)
alarmPoweroffhourEntry.grid(row = 19, column = 2, columnspan=1, rowspan=1, sticky=W)
alarmPoweroffhourEntry.insert(0, "0")
alarmPoweroffhourEntry.bind("<FocusIn>", (lambda event: alarmPoweroffhourFocusIn(tkAlarmPoweroffhour.get())))
alarmPoweroffhourEntry.bind("<FocusOut>", (lambda event: alarmPoweroffhourFocusOut(tkAlarmPoweroffhour.get())))
#sp3_alarm_day GUI OBJECTS
alarmPoweroffdaylbl = Label(AlarmModeFrame, text="Choose Alarm Day:                    ", fg="snow", bg="#275c6b").grid(row = 14, column = 2, columnspan=1, rowspan=1, sticky=W)
alarmPoweroffdayEntry = Entry(AlarmModeFrame, textvariable=tkAlarmPoweroffday)
alarmPoweroffdayEntry.grid(row = 15, column = 2, columnspan=1, rowspan=1, sticky=W)
alarmPoweroffdayEntry.insert(0, "0")
alarmPoweroffdayEntry.bind("<FocusIn>", (lambda event: alarmPoweroffdayFocusIn(tkAlarmPoweroffday.get())))
alarmPoweroffdayEntry.bind("<FocusOut>", (lambda event: alarmPoweroffdayFocusOut(tkAlarmPoweroffday.get())))
#sp3_alarm_weekday GUI OBJECTS
AlarmPoweroffweekdaypopupMenu = OptionMenu(AlarmModeFrame, tkAlarmPoweroffweekday, *Day_Choices)
AlarmPoweroffweekdaylbl = Label(AlarmModeFrame, text="Choose Alarm Weekday:", fg="snow", bg="#275c6b").grid(row = 14, column = 1, columnspan=1, rowspan=1, sticky=W)
AlarmPoweroffweekdaypopupMenu.grid(row = 15, column =1, columnspan=1, rowspan=1, sticky=W)
AlarmPoweroffweekdaypopupMenu.configure(background="snow")
#sp3_alarm_month GUI OBJECTS
AlarmPoweroffmonthpopupMenu = OptionMenu(AlarmModeFrame, tkAlarmPoweroffmonth, *Month_Choices)
AlarmPoweroffmonthlbl = Label(AlarmModeFrame, text="Alarm Month:", fg="snow", bg="#275c6b").grid(row = 14, column = 3, columnspan=1, rowspan=1, sticky=W)
AlarmPoweroffmonthpopupMenu.grid(row = 15, column =3, columnspan=1, rowspan=1, sticky=W)
AlarmPoweroffmonthpopupMenu.configure(background="snow")
#sp3_alarm_min_off GUI OBJECTS
WakeUpMinlbl = Label(AlarmModeFrame, text="Setting WakeUp-Alarm minute:            ", fg="snow", bg="#275c6b").grid(row = 16, column = 1, columnspan=1, rowspan=1, sticky=W)
WakeUpMinEntry = Entry(AlarmModeFrame, textvariable=tkAlarmminoff)
WakeUpMinEntry.grid(row = 17, column = 1, columnspan=1, rowspan=1, sticky=W)
WakeUpMinEntry.insert(0, "0")
WakeUpMinEntry.bind("<FocusIn>", (lambda event: WakeUpMinFocusIn(tkAlarmminoff.get())))
WakeUpMinEntry.bind("<FocusOut>", (lambda event: WakeUpMinFocusOut(tkAlarmminoff.get())))
#sp3_alarm_hour_off GUI OBJECTS
WakeUpHourlbl = Label(AlarmModeFrame, text="Setting WakeUp-Alarm Hour:", fg="snow", bg="#275c6b").grid(row = 16, column = 2, columnspan=1, rowspan=1, sticky=W)
WakeUpHourEntry = Entry(AlarmModeFrame, textvariable=tkAlarmhouroff)
WakeUpHourEntry.grid(row = 17, column = 2, columnspan=1, rowspan=1, sticky=W)
WakeUpHourEntry.insert(0, "0")
WakeUpHourEntry.bind("<FocusIn>", (lambda event: WakeUpHourFocusIn(tkAlarmhouroff.get())))
WakeUpHourEntry.bind("<FocusOut>", (lambda event: WakeUpHourFocusOut(tkAlarmhouroff.get())))
#sp3_intervalAlarmOnTime GUI OBJECTS
Alarmminonlbl = Label(IntervalAlarmFrame, text="Interval On-Time in minutes:                ", fg="snow", bg="#275c6b").grid(row = 12, column = 1, columnspan=1, rowspan=1, sticky=W)
AlarmminonEntry = Entry(IntervalAlarmFrame, textvariable=tkIntervalAlarmOnTime)
AlarmminonEntry.grid(row = 13, column = 1, columnspan=1, rowspan=1, sticky=W)
AlarmminonEntry.insert(0, "0")
AlarmminonEntry.bind("<FocusIn>", (lambda event: AlarmminonFocusIn(tkIntervalAlarmOnTime.get())))
AlarmminonEntry.bind("<FocusOut>", (lambda event: AlarmminonFocusOut(tkIntervalAlarmOnTime.get())))
#sp3_intervalAlarmOffTime GUI OBJECTS
Alarmminofflbl = Label(IntervalAlarmFrame, text="Interval Off-Time in minutes:     ", fg="snow", bg="#275c6b").grid(row = 12, column = 2, columnspan=1, rowspan=1, sticky=W)
AlarmminoffEntry = Entry(IntervalAlarmFrame, textvariable=tkIntervalAlarmOffTime)
AlarmminoffEntry.grid(row = 13, column = 2, columnspan=1, rowspan=1, sticky=W)
AlarmminoffEntry.insert(0, "0")
AlarmminoffEntry.bind("<FocusIn>", (lambda event: AlarmminoffFocusIn(tkIntervalAlarmOffTime.get())))
AlarmminoffEntry.bind("<FocusOut>", (lambda event: AlarmminoffFocusOut(tkIntervalAlarmOffTime.get())))
#Joy-IT-Logo
Logo1 = ImageTk.PhotoImage(Image.open("logo.gif"))
Panel = Label(mainframe, image = Logo1, borderwidth=0, highlightthickness = 0)
Panel.grid(row = 0, column = 0, columnspan = 4, rowspan = 1, sticky=N, pady = 10, padx = 10)
#SetClockH
SetClockHlbl = Label(SetClockFrame1, text="Set the Hours:                         ", fg="snow", bg="#275c6b").grid(row = 0, column = 3, columnspan=1, rowspan=1, sticky=W)
SetClockHEntry = Entry(SetClockFrame1, textvariable=tkSetClockH)
SetClockHEntry.grid(row = 1, column = 3, columnspan=1, rowspan=1, sticky=W)
SetClockHEntry.insert(0, "0")
SetClockHEntry.bind("<FocusIn>", (lambda event: SetClockHFocusIn(tkSetClockH.get())))
SetClockHEntry.bind("<FocusOut>", (lambda event: SetClockHFocusOut(tkSetClockH.get())))
#SetClockM
SetClockMlbl = Label(SetClockFrame1, text="Set the Minutes:", fg="snow", bg="#275c6b").grid(row = 0, column = 4, columnspan=1, rowspan=1, sticky=W)
SetClockMEntry = Entry(SetClockFrame1, textvariable=tkSetClockM)
SetClockMEntry.grid(row = 1, column = 4, columnspan=1, rowspan=1, sticky=W)
SetClockMEntry.insert(0, "0")
SetClockMEntry.bind("<FocusIn>", (lambda event: SetClockMFocusIn(tkSetClockM.get())))
SetClockMEntry.bind("<FocusOut>", (lambda event: SetClockMFocusOut(tkSetClockM.get())))
#SetDateM
SetDateMpopupMenu = OptionMenu(SetClockFrame1, tkSetDateM, *Month_Choices)
SetDateMpopupMenu.configure(background="snow")
SetDateMlbl = Label(SetClockFrame1, text="Set the Month:", fg="snow", bg="#275c6b").grid(row = 4, column = 3, columnspan=1, rowspan=1, sticky=W)
SetDateMpopupMenu.grid(row = 5, column =3, columnspan=1, rowspan=1, sticky=W)
#SetDateWD
SetDateWDpopupMenu = OptionMenu(SetClockFrame1, tkSetDateWD, *Day_Choices)
SetDateWDpopupMenu.configure(background="snow")
SetDateWDlbl = Label(SetClockFrame1, text="Set The Weekday:", fg="snow", bg="#275c6b").grid(row = 4, column = 4, columnspan=1, rowspan=1, sticky=W)
SetDateWDpopupMenu.grid(row = 5, column =4, columnspan=1, rowspan=1, sticky=W)
#SetDateD
SetDateDlbl = Label(SetClockFrame1, text="Set the Days:", fg="snow", bg="#275c6b").grid(row = 2, column = 3, columnspan=1, rowspan=1, sticky=W)
SetDateDEntry = Entry(SetClockFrame1, textvariable=tkSetDateD)
SetDateDEntry.grid(row = 3, column = 3, columnspan=1, rowspan=1, sticky=W)
SetDateDEntry.insert(0, "0")
SetDateDEntry.bind("<FocusIn>", (lambda event: SetDateDFocusIn(tkSetDateD.get())))
SetDateDEntry.bind("<FocusOut>", (lambda event: SetDateDFocusOut(tkSetDateD.get())))
#SetDateD
SetDateYstr = 0 
SetDateYlbl = Label(SetClockFrame1, text="Set the Year:", fg="snow", bg="#275c6b").grid(row = 2, column = 4, columnspan=1, rowspan=1, sticky=W)
SetDateYEntry = Entry(SetClockFrame1, textvariable=tkSetDateY)
SetDateYEntry.grid(row = 3, column = 4, columnspan=1, rowspan=1, sticky=W)
SetDateYEntry.bind("<FocusIn>", (lambda event: SetDateYFocusIn(tkSetDateY.get())))
SetDateYEntry.bind("<FocusOut>", (lambda event: SetDateYFocusOut(tkSetDateY.get())))
SetDateYEntry.insert(0, "0")
#Checkbox
TimeSyncLabel =Label(SetClockFrame1, text="Settings for the Clock:                        ", fg="snow", bg="#275c6b").grid(row = 0, column = 0, columnspan=1, rowspan=1)
TimeSyncRB1 = IntVar(fenster)
RB1 = Radiobutton(SetClockFrame1, text="No Change",  variable=TimeSyncRB1, value=1, fg="black", bg="#275c6b")
RB1.grid(row=1, column=0, sticky=W)
RB1.select()
RB2 = Radiobutton(SetClockFrame1, text="Sync with RaspberryPi", variable=TimeSyncRB1, value=2, fg="black", bg="#275c6b")
RB2.grid(row=5, column=0, sticky=W)
RB2.deselect()
RB3 = Radiobutton(SetClockFrame1, text="Manual Setting", variable=TimeSyncRB1, value=3, fg="black", bg="#275c6b")
RB3.grid(row=3, column=0, sticky=W)
RB3.deselect()
#Info Label
Infolbl = Label(mainframe, text="Please read the Readme file", fg="snow", bg="#275c6b").grid(row=999, column = 0, columnspan = 1, rowspan = 1, padx=30, pady=20)
#Button GUI OBJECTS
Update_Button = Button(mainframe, text="UPDATE!", command=Upload_to_StromPi).grid(row = 999, column = 0, columnspan = 4, rowspan = 1, padx=30, pady=20)

Refresh_Status()


mainframe.mainloop()

