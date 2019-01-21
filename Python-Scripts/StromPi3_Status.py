import serial
from time import sleep

wide_range_volt_min = 4.8
battery_volt_min = 0.5
mUSB_volt_min = 4.1

def enabled_disabled_converter(argument):
    switcher = {
        0: "Disabled",
        1: "Enabled",
    }
    return switcher.get(argument, "nothing")

def weekday_converter(argument):
    switcher = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday",
    }
    return switcher.get(argument, "nothing")

def strompi_mode_converter(argument):
    switcher = {
        1: "mUSB -> Wide",
        2: "Wide -> mUSB",
        3: "mUSB -> Battery",
        4: "Wide -> Battery",
    }
    return switcher.get(argument, "nothing")

def alarm_mode_converter(argument):
    switcher = {
        1: "Time-Alarm",
        2: "Date-Alarm",
        3: "Weekday-Alarm",
    }
    return switcher.get(argument, "nothing")

def batterylevel_shutdown_converter(argument):
    switcher = {
        0: "Disabled",
        1: "10%",
        2: "25%",
        3: "50%",
    }
    return switcher.get(argument, "nothing")

def batterylevel_converter(batterylevel,charging):

    if charging:
        switcher = {
            1: " [10%] [charging]",
            2: " [25%] [charging]",
            3: " [50%] [charging]",
            4: " [100%] [charging]",
        }
        return switcher.get(batterylevel, "nothing")
    else:
        switcher = {
            1: " [10%]",
            2: " [25%]",
            3: " [50%]",
            4: " [100%]",
        }
        return switcher.get(batterylevel, "nothing")

serial_port = serial.Serial()

serial_port.baudrate = 38400
serial_port.port = '/dev/serial0'
serial_port.timeout = 1
serial_port.bytesize = 8
serial_port.stopbits = 1
serial_port.parity = serial.PARITY_NONE

if serial_port.isOpen(): serial_port.close()
serial_port.open()

try:
    serial_port.write('status-rpi')
    sleep(1)
    serial_port.write('\x0D')
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
    sp3_ADC_Wide = float(serial_port.readline(9999))/1000;
    sp3_ADC_BAT = float(serial_port.readline(9999))/1000;
    sp3_ADC_USB = float(serial_port.readline(9999))/1000;
    sp3_ADC_OUTPUT = float(serial_port.readline(9999))/1000;
    sp3_firmwareVersion = serial_port.readline(9999);


    date = int(sp3_date)

    strompi_year = int(sp3_date) // 10000
    strompi_month = int(sp3_date) % 10000 // 100
    strompi_day = int(sp3_date) % 100

    strompi_hour = int(sp3_time) // 10000
    strompi_min = int(sp3_time) % 10000 // 100
    strompi_sec = int(sp3_time) % 100

    if sp3_ADC_Wide > wide_range_volt_min:
        wide_range_volt = str(sp3_ADC_Wide) + 'V'
    else:
        wide_range_volt = ' not connected'

    if sp3_ADC_BAT > battery_volt_min:
        battery_volt = str(sp3_ADC_BAT) + 'V' + batterylevel_converter(int(sp3_batLevel),int(sp3_charging))
    else:
        battery_volt = ' not connected'

    if sp3_ADC_USB > mUSB_volt_min:
        microUSB_volt = str(sp3_ADC_USB) + 'V'
    else:
        microUSB_volt = ' not connected'

    output_volt = str(sp3_ADC_OUTPUT) + 'V'

    print ' '
    print '---------------------------------'
    print 'StromPi-Status:'
    print '---------------------------------'
    print 'Time: ' + str(strompi_hour).zfill(2) + ':' + str(strompi_min).zfill(2) + ':' + str(strompi_sec).zfill(2)
    print 'Date: ' + weekday_converter(int(sp3_weekday)) + ' ' + str(strompi_day).zfill(2) + '.' + str(strompi_month).zfill(2) + '.' + str(strompi_year).zfill(2)
    print ' '
    print 'StromPi-Mode: ' + strompi_mode_converter((int(sp3_modus)))
    print ' '
    print 'WakeUp-Alarm: ' + enabled_disabled_converter(int(sp3_alarm_enable))
    print ' Alarm-Mode: ' + alarm_mode_converter(int(sp3_alarm_mode))
    print ' Alarm-Time: ' + sp3_alarm_hour.rstrip('\n').zfill(2) + ':' + sp3_alarm_min.rstrip('\n').zfill(2)
    print ' Alarm-Date: ' + sp3_alarm_day.rstrip('\n').zfill(2) + ':' + sp3_alarm_month.rstrip('\n').zfill(2)
    print ' WakeUp-Alarm: ' + weekday_converter(int(sp3_alarm_weekday))
    print ' '
    print 'PowerOff-Alarm: ' + enabled_disabled_converter(int(sp3_alarmPoweroff))
    print ' PowerOff-Alarm-Time: ' + sp3_alarm_hour_off.rstrip('\n').zfill(2) + ':' + sp3_alarm_min_off.rstrip('\n').zfill(2)
    print ' '
    print 'Raspberry Pi Shutdown: ' + enabled_disabled_converter(int(sp3_shutdown_enable))
    print ' Shutdown-Timer: ' + sp3_shutdown_time.rstrip('\n').zfill(2) + ' seconds'
    print ' '
    print 'Powerfail Warning: ' + enabled_disabled_converter(int(sp3_warning_enable))
    print ' '
    print 'Serial-Less Mode: ' + enabled_disabled_converter(int(sp3_serialLessMode))
    print ' '
    print 'Interval-Alarm: ' + enabled_disabled_converter(int(sp3_intervalAlarm))
    print ' Interval-On-Time: ' + sp3_intervalAlarmOnTime.rstrip('\n').zfill(2) + ' minutes'
    print ' Interval-Off-Time: ' + sp3_intervalAlarmOffTime.rstrip('\n').zfill(2) + ' minutes'
    print ' '
    print 'Battery-Level Shutdown: ' + batterylevel_shutdown_converter(int(sp3_batLevel_shutdown))
    print ' '
    print 'Firmware Version: ' + sp3_firmwareVersion.rstrip('\n')
    print ' '
    print '---------------------------------'
    print 'Voltage-Levels:'
    print '---------------------------------'
    print 'Wide-Range-Inputvoltage: ' + wide_range_volt
    print 'LifePo4-Batteryvoltage: ' + battery_volt
    print 'microUSB-Inputvoltage: ' + microUSB_volt
    print 'Output-Voltage: ' + output_volt
    print ' '

except KeyboardInterrupt:
    print('interrupted!')

serial_port.close()