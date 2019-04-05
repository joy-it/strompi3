import serial
from time import sleep


wide_range_volt_min = 4.8
battery_volt_min = 0.5
mUSB_volt_min = 4.1


breakS = 0.1
breakL = 0.5


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




print("\n\n\nStromPi V3 Serial Config Script (PYTHON3)\n\n")


#strompi-mode
print("\n\nSetting the StromPi mode (1 = mUSB -> Wide, 2 = Wide -> mUSB, 3 = mUSB -> Battery, 4 = Wide -> Battery)\n")

strompiMode = input("Mode (1-4): ")
while int(strompiMode) < 1 or int(strompiMode) > 4:
    strompiMode = input("Failed! Mode (1-4): ")


#Shutdown-enable & set-timer
print("\n\nEnabling or disabling shutdown (0 = disable, 1 = enable)\n")

shutdownEnable = input("Shutdown status (0 - 1): ")
while int(shutdownEnable) < 0 or int(shutdownEnable) > 1:
    shutdownEnable = input("Failed! Shutdown status (0 - 1): ")

if int(shutdownEnable) == 1:
    print("\nSetting shutdown timer (seconds)\n")

    setTimer = input("Seconds (0 - 65535): ")
    while int(setTimer) < 0 or int(setTimer) > 65535:
        setTimer = input("Failed! Seconds (0 - 65535): ")


#alarm-enable & alarm-mode
print("\n\nEnabling or disabling wake up alarm (0 = disable, 1 = enable)\n")

alarmEnable = input("Wake up alarm status (0 - 1): ")
while int(alarmEnable) < 0 or int(alarmEnable) > 1:
    alarmEnable = input("Failed! Wake up alarm status (0 - 1): ")

if int(alarmEnable) == 1:
    print("\nSetting the wake up alarm mode (1 = Time-Alarm , 2 = Date-Alarm, 3 = Weekday-Alarm)\n")

    alarmMode = input("Wake up alarm mode (1 - 3): ")
    while int(alarmMode) < 1 or int(alarmMode) > 3:
        alarmMode = input("Failed! Wake up alarm mode (1 - 3): ")

    #Wake up alarm time
    if int(alarmMode) == 1:
        print("\nSetting the wake up alarm time (hours, minutes)\n")

        alarmSetTimeH = input("Hours (0-23): ")
        while int(alarmSetTimeH) < 0 or int(alarmSetTimeH) > 23:
            alarmSetTimeH = input("Failed! Hours (0-23): ")

        alarmSetTimeM = input("Minutes (0-59): ")
        while int(alarmSetTimeM) < 0 or int(alarmSetTimeM) > 59:
            alarmSetTimeM = input("Failed! Hours (0-59): ")

    #Wake up alarm date
    elif int(alarmMode) == 2:
        print("\nSetting the wake up alarm date (day, month)\n")

        alarmSetDateD = input("Day (1-31): ")
        while int(alarmSetDateD) < 1 or int(alarmSetDateD) > 31:
            alarmSetDateD = input("Failed! Day (1-31): ")

        alarmSetDateM = input("Month (1-12): ")
        while int(alarmSetDateM) < 1 or int(alarmSetDateM) > 12:
                alarmSetDateM = input("Failed! Month (1-12): ")

    else:
        print("\nSetting the wake up alarm date (1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday)\n")

        alarmSetWeekday = input("Weekday (1 - 7): ")
        while int(alarmSetWeekday) < 1 or int(alarmSetWeekday) > 7:
            alarmSetWeekday = input("Failed! Weekday (1 - 7): ")


#poweroff-enable & poweroff-set-time
print("\n\nEnabling or disabling poweroff (0 = disable, 1 = enable)\n")

poweroffEnable = input("Poweroff status (0 - 1): ")
while int(poweroffEnable) < 0 or int(poweroffEnable) > 1:
    poweroffEnable = input("Failed! Poweroff status (0 - 1): ")

if int(poweroffEnable) == 1:
    print("\nSetting poweroff time (hour, minute)\n")

    poweroffSetTimeH = input("Hour (0 - 23): ")
    while int(poweroffSetTimeH) < 0 or int(poweroffSetTimeH) > 23:
        poweroffSetTimeH = input("Failed! Hour (0 - 23): ")

    poweroffSetTimeM = input("Minute (0 - 59): ")
    while int(poweroffSetTimeM) < 0 or int(poweroffSetTimeM) > 59:
        poweroffSetTimeM = input("Failed! Minute (0 - 59): ")


#batlevel-shutdown
print("\n\nSetting battery level shutdown (0 = disable, 1 = below 10%, 2 = below 25%, 3 = below 50%)\n")

batlevelShutdown = input("Battery level shutdown (0 - 3): ")
while int(batlevelShutdown) < 0 or int(batlevelShutdown) > 3:
    batlevelShutdown = input("Failed! Battery level shutdown (0 - 3): ")


#serialless-mode
print("\n\nEnabling or disabling serialless-mode (0 = disable, 1 = enable)\n")

seriallessMode = input("Serialless mode (0 - 1): ")
while int(seriallessMode) < 0 or int(seriallessMode) > 1:
    seriallessMode = input("Failed! Serialless mode (0 - 1): ")


#warning-enable
print("\n\nEnabling or disabling warning through serial interface (0 = disable, 1 = enable)\n")

warningEnable = input("Warning status (0 - 1): ")
while int(warningEnable) < 0 or int(warningEnable) > 1:
    warningEnable = input("Failed! Warning status (0 - 1): ")


#set-date
print("\n\nSetting the date (day, month, year, weekday)\n")

setDateD = input("Day (1-31): ")
while int(setDateD) < 1 or int(setDateD) > 31:
    setDateD = input("Failed! Day (1-31): ")

setDateM = input("Month (1-12): ")
while int(setDateM) < 1 or int(setDateM) > 12:
    setDateM = input("Failed! Month (1-12): ")

setDateY = input("Year (0-99): ")
while int(setDateY) < 0 or int(setDateY) > 99:
    setDateY = input("Failed! Year (0-99): ")

setDateWD = input("Weekday (1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday): ")
while int(setDateWD) < 1 or int(setDateWD) > 7:
    setDateWD = input("Failed! Weekday (1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday): ")


#set-clock
print("\n\nSetting the clock (hour, minute)\n")

setClockH = input("Hour (0-23): ")
while int(setClockH) < 0 or int(setClockH) > 23:
    setClockH = input("Failed! Hour (0-23): ")

setClockM = input("Minute (0-59): ")
while int(setClockM) < 0 or int(setClockM) > 59:
    setClockM = input("Failed! Minute (0-59): ")

setClockS = "00"




serial_port = serial.Serial()

serial_port.baudrate = 38400
serial_port.port = "/dev/serial0"
serial_port.timeout = 1
serial_port.bytesize = 8
serial_port.stopbits = 1
serial_port.parity = serial.PARITY_NONE

if serial_port.isOpen(): serial_port.close()
serial_port.open()

try:
    serial_port.write(str.encode("quit"))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    sleep(breakL)

    serial_port.write(str.encode("set-date " + setDateD + " " + setDateM + " " + setDateY + " " + setDateWD))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("\n\nSetting set-date...")
    sleep(breakL)

    serial_port.write(str.encode("set-clock " + setClockH + " " + setClockM + " " + setClockS))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("Setting set-clock...")
    sleep(breakL)

    serial_port.write(str.encode("strompi-mode " + strompiMode))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("Setting strompi-mode...")
    sleep(breakL)

    serial_port.write(str.encode("shutdown-enable " + shutdownEnable))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("Setting shutdown-enable...")
    sleep(breakL)

    if int(shutdownEnable) == 1:
        serial_port.write(str.encode("set-timer " + setTimer))
        sleep(breakS)
        serial_port.write(str.encode("\x0D"))
        print("Setting set-timer...")
        sleep(breakL)

    serial_port.write(str.encode("alarm-enable " + alarmEnable))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("Setting alarm-enable...")
    sleep(breakL)

    if int(alarmEnable) == 1:
        serial_port.write(str.encode("alarm-mode " + alarmMode))
        sleep(breakS)
        serial_port.write(str.encode("\x0D"))
        print("Setting alarm-mode...")
        sleep(breakL)

        if int(alarmMode) == 1:
            serial_port.write(str.encode("alarm-set-time " + alarmSetTimeH + " " + alarmSetTimeM))
            sleep(breakS)
            serial_port.write(str.encode("\x0D"))
            print("Setting alarm-set-time...")
            sleep(breakL)

        elif int(alarmMode) == 2:
            serial_port.write(str.encode("alarm-set-date " + alarmSetDateD + " " + alarmSetDateM))
            sleep(breakS)
            serial_port.write(str.encode("\x0D"))
            print("Setting alarm-set-date...")
            sleep(breakL)

        else:
            serial_port.write(str.encode("alarm-set-weekday " + alarmSetWeekday))
            sleep(breakS)
            serial_port.write(str.encode("\x0D"))
            print("Setting alarm-set-weekday...")
            sleep(breakL)

    serial_port.write(str.encode("poweroff-enable " + poweroffEnable))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("Setting poweroff-enable...")
    sleep(breakL)

    if int(poweroffEnable) == 1:
        serial_port.write(str.encode("poweroff-set-time " + poweroffSetTimeH + " " + poweroffSetTimeM))
        sleep(breakS)
        serial_port.write(str.encode("\x0D"))
        print("Setting poweroff-set-time...")
        sleep(breakL)

    serial_port.write(str.encode("batlevel-shutdown " + batlevelShutdown))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("Setting batlevel-shutdown...")
    sleep(breakL)

    serial_port.write(str.encode("serialless-mode " + seriallessMode))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("Setting serialless-mode...")
    sleep(breakL)

    serial_port.write(str.encode("warning-enable " + warningEnable))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    print("Setting warning-enable...")
    sleep(breakL)

    print("\nDone.")

    serial_port.write(str.encode('status-rpi'))
    sleep(0.1)
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

    print(' ')
    print('---------------------------------')
    print('StromPi-Status:')
    print('---------------------------------')
    print('Time: ' + str(strompi_hour).zfill(2) + ':' + str(strompi_min).zfill(2) + ':' + str(strompi_sec).zfill(2))
    print('Date: ' + weekday_converter(int(sp3_weekday)) + ' ' + str(strompi_day).zfill(2) + '.' + str(
        strompi_month).zfill(2) + '.' + str(strompi_year).zfill(2))
    print(' ')
    print('StromPi-Mode: ' + strompi_mode_converter((int(sp3_modus))))
    print(' ')
    print('WakeUp-Alarm: ' + enabled_disabled_converter(int(sp3_alarm_enable)))
    print(' Alarm-Mode: ' + alarm_mode_converter(int(sp3_alarm_mode)))
    print(
        ' Alarm-Time: ' + str(sp3_alarm_hour.rstrip(b'\n').zfill(2) + b':' + sp3_alarm_min.rstrip(b'\n').zfill(2))[2:7])
    print(' Alarm-Date: ' + str(sp3_alarm_day.rstrip(b'\n').zfill(2) + b':' + sp3_alarm_month.rstrip(b'\n').zfill(2))[
                            2:7])
    print(' WakeUp-Alarm: ' + weekday_converter(int(sp3_alarm_weekday)))
    print(' ')
    print('PowerOff-Alarm: ' + enabled_disabled_converter(int(sp3_alarmPoweroff)))
    print(' PowerOff-Alarm-Time: ' + str(
        sp3_alarm_hour_off.rstrip(b'\n').zfill(2) + b':' + sp3_alarm_min_off.rstrip(b'\n').zfill(2))[2:7])
    print(' ')
    print('Raspberry Pi Shutdown: ' + enabled_disabled_converter(int(sp3_shutdown_enable)))
    print(' Shutdown-Timer: ' + str(sp3_shutdown_time.rstrip(b'\n') + b' seconds')[2:])
    print(' ')
    print('Powerfail Warning: ' + enabled_disabled_converter(int(sp3_warning_enable)))
    print(' ')
    print('Serial-Less Mode: ' + enabled_disabled_converter(int(sp3_serialLessMode)))
    print(' ')
    print('Battery-Level Shutdown: ' + batterylevel_shutdown_converter(int(sp3_batLevel_shutdown)))
    print(' ')
    print('Firmware Version: ' + str(sp3_firmwareVersion.rstrip(b'\n'))[2:])
    print(' ')
    print('---------------------------------')
    print('Voltage-Levels:')
    print('---------------------------------')
    print('Wide-Range-Inputvoltage: ' + wide_range_volt)
    print('LifePo4-Batteryvoltage: ' + battery_volt)
    print('microUSB-Inputvoltage: ' + microUSB_volt)
    print('Output-Voltage: ' + output_volt)
    print(' ')

except KeyboardInterrupt:
    print('interrupted!')

serial_port.close()