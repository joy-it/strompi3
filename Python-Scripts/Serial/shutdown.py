import serial
import os
from time import sleep


breakS = 0.1
breakL = 0.5

serial_port = serial.Serial()

serial_port.baudrate = 38400
serial_port.port = "/dev/serial0"
serial_port.timeout = 1
serial_port.bytesize = 8
serial_port.stopbits = 1
serial_port.parity = serial.PARITY_NONE

if serial_port.isOpen(): serial_port.close()
serial_port.open()

while True:
    serial_port.write(str.encode("quit"))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))
    sleep(breakL)

    serial_port.write(str.encode("poweroff"))
    sleep(breakS)
    serial_port.write(str.encode("\x0D"))

    print("sudo shutdown -h now")
    print("Shutting down...")

    sleep(2)
    os.system("sudo shutdown -h now")