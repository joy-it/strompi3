# Open-Source Firmware for the Joy-IT StromPi 3
******************************************************************************************************************

StromPi v3 - by Joy-IT
OpenSource-Firmware published under MIT-License

******************************************************************************************************************

	This following pieces of Code defines the Firmware of the StromPi3 Raspberry Pi expansion.
	Its main functions are included into the integrated OpenSource FreeRTOS
	The Basis I/O HAL Drivers of the STM32F031 are generated with STM32CubeMX and can be modified here in Source
	or with the "StromPi3.ioc" - File.

	The main functionality of the StromPi3 is realized with the STM32 ADC Watchdog - which is configured to monitor
	the voltage of the configured primary voltage source. If the voltage source fails and the measured voltage
	falls under the threshold, then the STM32 switch to the voltage/powerpath of the configured backup source.
	The STM32 switches the powerpath through Mosfets connected to its GPIO-Ports.
	The voltage-sources which can be configured are the following:

		- mUSB
		- Wide-Range (StepDown Regulator Output)
		- Battery

	If the Battery-PowerPath isn't selected as the voltage-source, the Battery-Hat Expansion would be configured
	into its charging mode.
	For further reference of the topology of the StromPi3, please refer to the schematic-files which are also
	included into the OpenSource-Files

	The FreeRTOS Operating System is generated with two Tasks:

		- Main Operating Task with the AlarmHandler (for Time based Operations like timed WakeUp or Shutdown),
		  the function to repower the Raspberry Pi in case that the main voltage source comes back
		  and the functions to read out the ADC-Values for Voltage Output.
		  This Task is timed to operate in a period of 1 second

		  The Sourcecode of this Task is defined in this "main.c" File

		- Serial Console Task which is processing the the in- and output of the serial interface.

		  The Sourecode of this Task is defined in the "UART_CLI.c" File

 	The ADC-Watchdog is processed in its own HAL-Based Interrupt-Routine through flags, which then are
 	processed in the main Task.
	
	Further Informations about the Schematic and the PCB Layout of the StromPi3, 
	you can find in the "Schematic+Hardware-Layout"-Folder.

 	The Files are created in the Atollic TrueSTUDIO for STM32, which can be used for STM32 for free.
 	You can include the .cproject file in the IDE and start to code your own modifications
 	and debug them with a ST-Linkv2 connected to the StromPi3 or make your own binary which can be flashed
 	with the stm32flasher in flashmode of the StromPi 3
 	(Please refer to the manual provided in our firmware updates in the download section of strompi.joy-it.net)

 	(connections have to be soldered for InCircuit debugging- please refer to the Hardware-Layout provided in 
	the "Schematic Files+Hardware-Layout" Folder)

 	Please refer to the additional comments in the corresponding sections for further explanations.

	If there are questions or something is unclear, please feel free
	to contact us via E-Mail: service@joy-it.net
	
******************************************************************************************************************
	
Firmware Changelog	

******************************************************************************************************************

Firmware 1.0 – original Firmware Files

Firmware 1.1 – Power Fail Warning
- In the configuration terminal a new option has been included „warning-enable <option>“
- If this option is enabled, a warning is sent through the serial interface, when the primary voltage source fails – this option is similar to the function „shutdown-enable“ where a warning is sent out to shutdown the Raspbery Pi
		
Firmware 1.2 – PowerBack Detection
- After a power failure of the primary voltage source the shutdown-time can now be canceled if in the configured shutdown-time the voltage-source turns back on.
In this case there would be an additional message sent out the serial interface which can be processed in a python script for example – a modified serialShutdown.py script is added with this firmware update.

Firmware 1.21 – Fix Shutdown Timer
- Bug-Fix: Shutdown Timer can now be set > 255 seconds
		
Firmware 1.3 Beta
- Bug-Fix: PowerOff-Alarm Fixed
- StromPi3_Status.py Support: Now it is possible to read out the Configuration of the StromPi3 through a python Script.
		  It is also possible to read out the current ADC Voltage Values (like the current battery volatge) and process them in own python functions
- Firmware Version Output in "show-status" function

Firmware 1.4
- Serial-Less Mode:
 If the Serial-Interface is blocked by another HAT or an other module,
 it is possible to use the StromPi3 in a Serial-Less Mode.
 In this case the Shutdown-Signal is not sent out through the serial Interface as a message,
 but is indicated through a connected GPIO-LINE (Like in the previous versions of the StromPi family)
 As for this needed extra connection, please refer to the manuals located in the "SerialLess" Folder
- Battery-Voltagelevel percentage output in "adc-output"
- Charging State Output
- Batterylevel-Shutdown:
 The Battery-Voltage is measured and then mapped on 4 available voltage levels (1:10%, 2:25%, 3:50%, 4:100%)
 at the end of the main-Task. In the case the Batterylevel-Shutdown is configured,
 the StromPi3 give a shutdown-signal to the Raspberry Pi and cuts of the PowerPath in a fixed 10 seconds timer,
 when the Battery has been discharged to the configured level.
 
Firmware 1.5
- Interval Function: 
 Through this mode the StromPi3 can start the Powerpath for X Minutes, then it shuts down the Raspberry Pi with a serial command (Python Script have to be active in the background) and then it poweroff the main Powerpath.
 After the configured X "Off-Time" the StromPi3 turns the PowerPath on for another X Minutes "On-Time"
- sspc Command:
 The Terminal Console can be also started through this new command ["sspc"] additionally to the ["startstrompiconsole"]
- PowerOn Button:
 Now after the StromPi3 have powered off the PowerPath, the main PowerPathcan be started manually through shorting of the ResetPin of the StromPi3 - for this there have to be made an additional connection on the SP3 PCB; for this please refer to the manual in the PowerOnButton Folder
- poweroff Command:
 There was a bugfix included in this command
 
Firmware 1.6
- New Configuration Method: Because of the limited space in the Flash-Memory of the STM32F031 MCU, the configuration method for the StromPi Features has changed to a python script - this script features an assistant which shows you the current configuration parameters and helps you to change them to your desired setup.
You can find this script following this link: https://github.com/joy-it/strompi3/blob/master/StromPi3-Config/strompi_config.py
In the CLI (Command Line Interface), which was the previous configuration method, there are only basic features left - when you still want to use the configuration method through the CLI, then you can change to the CLI-Version of the firware (you can find it following this link: https://github.com/joy-it/strompi3-cliconfig or https://strompi.joy-it.net/wp-content/uploads/2019/04/StromPi3_v1.6_CLI.zip), but this version will have a lesser featureset, than the main version.
- Feature to show the current Voltage-Source:
 You can find a new entry at the "show-status" command, which shows the current active Voltage-Source
- PowerBackDetection in Serial-Less-Mode:
 Rather than a generated impulse, the GPIO-Pin for the Serial-Less Feature is pulled to GND as long as the Backup-Voltage Source is active. With the new Python-Scripts (please check the associated Script folders @ https://github.com/joy-it/strompi3-cliconfig/tree/master/SerialLess-Mode/SerialLess-Scripts) it is now possible to detect a PowerBack Event to stop a dedicated shutdown Counter.
- BugFix for the Serial-Less-Mode:
 In some configuration the Raspberry Pi wouldn't boot after shutdown in the Serial-Less-Mode. Now this should be fixed.
- Powerfailure-Counter:
 You can find a new entry at the "show-status" command, where you can check how many times the StromPi3 had to change to the Backup-Voltagesource
- PowerOn Button Timer and PowerOnButton Enable:
 If you want to use the PowerOn-Button Feature (https://github.com/joy-it/strompi3-cliconfig/blob/master/PowerOn-Button/RB-StromPi3-poweroff-Manual.pdf) you now can enable/disable this function - also now you can configure the timer for the shutdown after poweroff, which is needed for the PowerOffButton to initialize.
- PowerOff BugFix
- BatteryLevelShutdown:
 The Threshold Values were changed to more lower values (< 2800mV -> 10% | < 3100mV -> 25% | < 3220mV -> 50%) to extend battery operation with the an active BatteryLevelShutdown.

Firmware 1.7
- Power-Save-Mode: If you connect a Voltage-Source to the Wide-Input which is limited in it's energy (like a 12V Battery) you can now activate the Power-Save-Mode of the StromPi3 which is decreasing the standby current of this voltage source to a mere fraction. Please be aware that in high-power configurations, where the StromPi3 has to deliver about 2,5A and up, in the activated Power-Save-Mode there can occure some instabilities which results in a reboot of the Raspberry Pi.
- Revised Serial-Less Mode: There is now a second stage of the Serial-Less Mode which disconnects the UART Pins of the StromPi3 STM32 Controller completely from the TX/RX-Lines of the Raspberry Pi. As for this the compatibility of HATs/Expansions, which are also using the UART interface, is increased. Please refer to the Manuals and Scripts for activating and deactivating this mode.

Firmware 1.71
- (Emergency) PowerOff-Mode: This Feature shuts down the Raspberry Pi through the normal Shutdown procedure after a powerfailure and will procede into and maintain a poweroffstate even if the main Powersource would come back. Only a WakeUP Timer Event or a PowerOn Button will then be able to bring back the StromPi3 to  normal Operation. As for this please refer to the manual of the StromPi3. 
      
Firmware 1.72
- Weekend-Wakeup-Alarm: This mode allows you to choose if the WakeUp-Alarm will operate on weekends (saturday and sunday).
- Minute Wakeup Alarm: The Minute-WakeUp-Alarm allows you to set a timer, that will start the RaspberryPi after a set time, when it was shutdown through the poweroff command or the poweroff timer.

Firmware 1.72b
- Small Bugfix (shutdown_time_counter)
- Preparation for Hardware Rev 1.1 

Firmware 1.72c
- Bugfix on Interval Feature - Thanks @ctc

******************************************************************************************************************
	
Request Firmware Updates:

******************************************************************************************************************

If you would need a function which isn't currently included in the StromPi3, please feel free to contact us via Mail (service@joy-it.net), so we can include it in our next Firmware-Updates


******************************************************************************************************************
	
Support

******************************************************************************************************************

As for Support for our Firmware, please contact us via E-Mail: service@joy-it.net
or use our FAQ-Board at: https://strompi.joy-it.net/questions/

