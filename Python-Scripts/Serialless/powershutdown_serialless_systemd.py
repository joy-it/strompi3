#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
"""
Shut down the Raspberry Pi gracefully when the power supply fails.

Hardware
========

Raspberry Pi 1 B+ or higher (because of the different GPIO header layout)
StromPi3 Rev1.1
StromPi3 BatteryHAT


StromPi3 setup
==============

[If the StromPi3 is in serialless mode, execute the skript:
    StromPi3_Scriptverzeichnis_20200108/Serialless/Stop_Serialless.py
and set the jumper "Serialless" to OFF.]

Set up the StromPi 3 as follows (Firmware version 1.72c) using either
    StromPi3_Scriptverzeichnis_20200108/Config\ Scripte\ nur\ main\ Version/V1.72/Config\ Script\ ohne\ GUI/strompi_config.py
or
    StromPi3_Scriptverzeichnis_20200108/Config\ Scripte\ nur\ main\ Version/V1.72/Config\ Script\ mit\ GUI/strompi_config_gui.py
to the following values:
    Config
    ———————————
    StromPi-Status:
    ———————————
    StromPi-Output: mUSB
    StromPi-Mode: mUSB -> Battery
    Raspberry Pi Shutdown: Enabled
    Shutdown-Timer: 30 seconds
    Powerfail Warning: Enabled
    Serial-Less Mode: Enabled
    PowerOn-Button: Disabled
    PowerOn-Button-Timer: 30 seconds
    Battery-Level Shutdown: Disabled
    PowerOff Mode: Disabled

Double check the settings with the following program:
    StromPi3_Scriptverzeichnis_20200108/StromPi\ Status/V1.72/StromPi3_Status.py

Shut down Raspberry Pi and set the jumper as follow:
    Serialless  ON

Power on the Raspberry Pi.

Execute the script:
    StromPi3_Scriptverzeichnis_20200108/Serialless/Start_Serialless.py


Software installation
=====================

Systemd unit file:
--8<---
[Unit]
Description=StromPi3 system shutdown on power failure

[Service]
Type=simple
ExecStart=/usr/local/bin/strompi3_shutdown_serialless.py

[Install]
WantedBy=default.target
--8<---

Copy this file to /usr/local/bin/strompi3_shutdown_serialless.py
$ sudo chmod +x /usr/local/bin/strompi3_shutdown_serialless.py
Copy the above content into /etc/systemd/system/strompi3_shutdown_serialless.service
$ sudo chmod 664 /etc/systemd/system/strompi3_shutdown_serialless.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable strompi3_shutdown_serialless.service
$ sudo systemctl start strompi3_shutdown_serialless.service
$ systemctl status strompi3_shutdown_serialless.service

"""

import RPi.GPIO as GPIO
from threading import Timer
import signal
import os

# Here you can choose the connected GPIO-Pin (in BCM mode)
# Pin 21 is the default pin when using the jumper on StromPi3 Rev1.1
GPIO_PIN = 21

# How long (in seconds) can the power failure last before we shut down?
SHUTDOWN_TIMER = 10

__NAME__ = 'StromPi3'

class ShutdownSerialless:
    """Watch the pin used by StromPi 3 to signal power failure.

    If a power failure is detected, a 'Timer' is started. When this timer
    elapses, the system will be shut down, but if the power supply comes
    back, the timer will be cancelled and nothing happens.
    """

    def __init__(self, pin, timeout, mode=GPIO.BCM, bounce=300):
        """Initialize.

        Parameters:
            pin: The pin where the StromPi 3 announces the power failure.
            timeout: How long to wait before initiating a system shutdown.
            mode: The GPIO mode how the pins are named.
            bounce: The bounce time (in ms).
        """
        self.pin = pin
        self.timeout = timeout
        self.mode = mode
        self.bounce = bounce
        self.timers = []

    def __del__(self):
        """Clean up behind us."""
        self.stop()
 
    def start(self):
        """Start watching the StromPi 3."""
        # Initialization
        GPIO.setmode(self.mode)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Add interrupt handling routine
        GPIO.add_event_detect(
            self.pin, GPIO.BOTH,
            callback=self.power_change, bouncetime=self.bounce)
        print(f'{__NAME__}: Safe shutdown in the case of power failure enabled')

    def stop(self):
        """Stop watching the StromPi 3."""
        if GPIO.getmode() is not None:
            # Remove interrupt handling routine and clean up behind us
            GPIO.remove_event_detect(self.pin)
            GPIO.cleanup()

    def signal(self, sig, frame):
        """Handle the signal 'sig'."""
        self.stop()
        if sig == signal.SIGINT:
            # We got a keyboard interrupt, print a new line
            print()
        print(f'{__NAME__}: Safe shutdown in the case of power failure disabled')

    def power_change(self, pin):
        """Callback function when the power supply changed."""
        if GPIO.input(self.pin):
            # If pin is high, we are back on the power supply
            print(f'{__NAME__}: Power back detected')
            for t in self.timers:
                t.cancel()
        else:
            # If pin is low, we lost the power supply
            print(f'{__NAME__}: Power failure detected')
            t = Timer(self.timeout, self.shutdown)
            t.start()
            self.timers.append(t)

    def shutdown(self):
        """Safely shut down the system."""
        print(f'{__NAME__}: Shutdown system')
        os.system('sudo shutdown -h now')


if __name__ == '__main__':

    s = ShutdownSerialless(GPIO_PIN, SHUTDOWN_TIMER)
    signal.signal(signal.SIGTERM, s.signal)     # 'kill'
    signal.signal(signal.SIGINT, s.signal)      # CTRL-C
    s.start()
    print('(CTRL-C for exit)')
    signal.pause()

