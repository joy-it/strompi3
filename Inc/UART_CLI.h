/*
    FreeRTOS V7.3.0 - Copyright (C) 2012 Real Time Engineers Ltd.


    ***************************************************************************
     *                                                                       *
     *    FreeRTOS tutorial books are available in pdf and paperback.        *
     *    Complete, revised, and edited pdf reference manuals are also       *
     *    available.                                                         *
     *                                                                       *
     *    Purchasing FreeRTOS documentation will not only help you, by       *
     *    ensuring you get running as quickly as possible and with an        *
     *    in-depth knowledge of how to use FreeRTOS, it will also help       *
     *    the FreeRTOS project to continue with its mission of providing     *
     *    professional grade, cross platform, de facto standard solutions    *
     *    for microcontrollers - completely free of charge!                  *
     *                                                                       *
     *    >>> See http://www.FreeRTOS.org/Documentation for details. <<<     *
     *                                                                       *
     *    Thank you for using FreeRTOS, and thank you for your support!      *
     *                                                                       *
    ***************************************************************************


    This file is part of the FreeRTOS distribution.

    FreeRTOS is free software; you can redistribute it and/or modify it under
    the terms of the GNU General Public License (version 2) as published by the
    Free Software Foundation AND MODIFIED BY the FreeRTOS exception.
    >>>NOTE<<< The modification to the GPL is included to allow you to
    distribute a combined work that includes FreeRTOS without being obliged to
    provide the source code for proprietary components outside of the FreeRTOS
    kernel.  FreeRTOS is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
    more details. You should have received a copy of the GNU General Public
    License and the FreeRTOS license exception along with FreeRTOS; if not it
    can be viewed here: http://www.freertos.org/a00114.html and also obtained
    by writing to Richard Barry, contact details for whom are available on the
    FreeRTOS WEB site.

    1 tab == 4 spaces!

    http://www.FreeRTOS.org - Documentation, latest information, license and
    contact details.

    http://www.SafeRTOS.com - A version that is certified for use in safety
    critical systems.

    http://www.OpenRTOS.com - Commercial support, development, porting,
    licensing and training services.
*/

#ifndef UART_COMMAND_CONSOLE_H
#define UART_COMMAND_CONSOLE_H

void vUARTCommandConsoleStart( void );

/*-----------------------------------------------------------*/

/*** Here are the commands registered which can be used in the serial console ***/

static portBASE_TYPE prvTimeOutput( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvADCOutput( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvMode( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvSetClock( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvSetTimer( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvStartStromPiConsole( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvStartStromPiConsoleQuick( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvQuitStromPiConsole( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvSetDate( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmMode( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmEnable( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmTime( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmWeekday( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmDate( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmPowerOffTime( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmPowerOffEnable( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmIntervalEnable( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmIntervalOnTime( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvAlarmIntervalOffTime( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvShutdownEnable( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvSerialLessMode( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvWarning( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvShowStatus( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvPowerOff( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvTimeRPi( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvDateRPi( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvStatusRPi( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );
static portBASE_TYPE prvBatLevelShutdown( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString );

/*** Here you can find  how FreeRTOS needs the command registered
 *
 * For example of xSetClock:
 *
 * 	( const int8_t * const ) "set-clock",          -> This is the command which can be typed by the user
 *  ( const int8_t * const ) "set-clock <hour> <minutes> <seconds>:\r\n Set the Clock of the StromPi RTC \r\n\r\n",  -> This is the Help-text which is displayed in the help section of the serial console
 * 	prvSetClock, -> This is the function which is linked in the UART_CLI.c to the command
 *  3 -> This is the amount of paramters the user have to type with the command
 *
 * ***/

static const CLI_Command_Definition_t xSetClock =
{
	( const int8_t * const ) "set-clock",
	( const int8_t * const ) "set-clock <hour> <minutes> <seconds>:\r\n Set the Clock of the StromPi RTC \r\n\r\n",
	prvSetClock,
	3
};

static const CLI_Command_Definition_t xSetDate =
{
	( const int8_t * const ) "set-date",
	( const int8_t * const ) "set-date <date> <month> <year> <weekday>:\r\n Set the Date of the StromPi RTC-Clock \r\n\r\n",
	prvSetDate,
	4
};

static const CLI_Command_Definition_t xSetTimer =
{
	( const int8_t * const ) "set-timer",
	( const int8_t * const ) "set-timer <shutdown-seconds>:\r\n Sets the Shutdown Timer to <shutdown-seconds>\r\n\r\n",
	prvSetTimer,
	1
};

static const CLI_Command_Definition_t xStartStromPiConsole =
{
	( const int8_t * const ) "startstrompiconsole",
	( const int8_t * const ) "",
	prvStartStromPiConsole,
	0
	//startstrompiconsole:\r\n Terminal-Console wird auf dem StromPi gestartet\r\n\r\n
};

static const CLI_Command_Definition_t xStartStromPiConsoleQuick =
{
	( const int8_t * const ) "sspc",
	( const int8_t * const ) "",
	prvStartStromPiConsoleQuick,
	0
	//startstrompiconsole:\r\n Terminal-Console wird auf dem StromPi gestartet\r\n\r\n
};

static const CLI_Command_Definition_t xQuitStromPiConsole =
{
	( const int8_t * const ) "quit",
	( const int8_t * const ) "quit:\r\n Closes the StromPi-Console\r\n\r\n",
	prvQuitStromPiConsole,
	0
	//startstrompiconsole:\r\n Terminal-Console wird auf dem StromPi gestartet\r\n\r\n
};

static const CLI_Command_Definition_t xADCOutput =
{
	( const int8_t * const ) "adc-output",
	( const int8_t * const ) "adc-output:\r\n Outputs the measured Voltages\r\n\r\n",
	prvADCOutput,
	0
};

static const CLI_Command_Definition_t xMode =
{
	( const int8_t * const ) "strompi-mode",
	( const int8_t * const ) "strompi-mode <mode-number>:\r\n Configures the mode of the StromPi 3:\r\n  Mode 1: mUSB -> Wide\r\n  Mode 2: Wide -> mUSB\r\n  Mode 3: mUSB -> Battery\r\n  Mode 4: Wide -> Battery\r\n\r\n",
	prvMode,
	1
};

static const CLI_Command_Definition_t xTimeOutput =
{
	( const int8_t * const ) "time-output",
	( const int8_t * const ) "time-output:\r\n Displays the actual time of the StromPi RTC-Clock\r\n\r\n",
	prvTimeOutput,
	0
};

static const CLI_Command_Definition_t xAlarmMode =
{
	( const int8_t * const ) "alarm-mode",
	( const int8_t * const ) "alarm-mode <mode-number>:\r\n Set the Wakeup-Alarm to one of the following modes:\r\n  Mode 1: Time-Alarm\r\n  Mode 2: Date-Alarm\r\n  Mode 3: Weekday-Alarm\r\n\r\n",
	prvAlarmMode,
	1
};

static const CLI_Command_Definition_t xAlarmEnable =
{
	( const int8_t * const ) "alarm-enable",
	( const int8_t * const ) "alarm-enable <option>:\r\n The configured Alarm-Mode will be enabled <1> or disabled <0>. \r\n\r\n",
	prvAlarmEnable,
	1
};

static const CLI_Command_Definition_t xAlarmTime =
{
	( const int8_t * const ) "alarm-set-time",
	( const int8_t * const ) "alarm-set-time <hour> <minutes>:\r\n Sets the time of the Wakeup-Alarm\r\n\r\n",
	prvAlarmTime,
	2
};

static const CLI_Command_Definition_t xAlarmWeekday =
{
	( const int8_t * const ) "alarm-set-weekday",
	( const int8_t * const ) "alarm-set-weekday <weekday>:\r\n Configures the weekday of the Wakeup-Alarm (Monday...Sunday -> 1...7)\r\n\r\n",
	prvAlarmWeekday,
	1
};

static const CLI_Command_Definition_t xAlarmDate =
{
	( const int8_t * const ) "alarm-set-date",
	( const int8_t * const ) "alarm-set-date <date> <month>:\r\n Sets the date of the Wakeup-Alarm\r\n\r\n",
	prvAlarmDate,
	2
};

static const CLI_Command_Definition_t xAlarmPowerOffTime =
{
	( const int8_t * const ) "poweroff-set-time",
	( const int8_t * const ) "poweroff-set-time <hour> <minutes>:\r\n Sets the time of the PowerOff-Alarm\r\n\r\n",
	prvAlarmPowerOffTime,
	2
};

static const CLI_Command_Definition_t xAlarmPowerOffEnable =
{
	( const int8_t * const ) "poweroff-enable",
	( const int8_t * const ) "poweroff-enable <option>:\r\n Enables <1> or disables <0> the PowerOff-Alarm\r\n\r\n",
	prvAlarmPowerOffEnable,
	1
};

static const CLI_Command_Definition_t xAlarmIntervalEnable =
{
	( const int8_t * const ) "interval-enable",
	( const int8_t * const ) "interval-enable <option>:\r\n Enables <1> or disables <0> the PowerOff-Interval-Alarm\r\n\r\n",
	prvAlarmIntervalEnable,
	1
};

static const CLI_Command_Definition_t xAlarmIntervalOnTime =
{
	( const int8_t * const ) "interval-ontime",
	( const int8_t * const ) "interval-ontime <min>:\r\n Defines the OnTime of the PowerOff-Interval-Alarm in Minutes\r\n\r\n",
	prvAlarmIntervalOnTime,
	1
};

static const CLI_Command_Definition_t xAlarmIntervalOffTime =
{
	( const int8_t * const ) "interval-offtime",
	( const int8_t * const ) "interval-offtime <min>:\r\n Defines the OffTime of the PowerOff-Interval-Alarm in Minutes\r\n\r\n",
	prvAlarmIntervalOffTime,
	1
};


static const CLI_Command_Definition_t xWarning =
{
	( const int8_t * const ) "warning-enable",
	( const int8_t * const ) "warning-enable <option>:\r\n Enables <1> or disables <0> the Warning through the serial interface, when the primary voltage input fails\r\n\r\n",
	prvWarning,
	1
};

static const CLI_Command_Definition_t xShutdownEnable =
{
	( const int8_t * const ) "shutdown-enable",
	( const int8_t * const ) "shutdown-enable <option>:\r\n Enables <1> or disables <0> the Raspberry Pi Shutdown\r\n\r\n",
	prvShutdownEnable,
	1
};

static const CLI_Command_Definition_t xShowStatus =
{
	( const int8_t * const ) "show-status",
	( const int8_t * const ) "show-status:\r\n Outputs the actual Configuration\r\n\r\n",
	prvShowStatus,
	0
};

static const CLI_Command_Definition_t xPowerOff =
{
	( const int8_t * const ) "poweroff",
	( const int8_t * const ) "poweroff:\r\n Shutdown the Raspberry Pi with the StromPi \r\n\r\n",
	prvPowerOff,
	0
};

static const CLI_Command_Definition_t xTimeRPi =
{
	( const int8_t * const ) "time-rpi",
	( const int8_t * const ) "",
	prvTimeRPi,
	0
};

static const CLI_Command_Definition_t xDateRPi =
{
	( const int8_t * const ) "date-rpi",
	( const int8_t * const ) "",
	prvDateRPi,
	0
};

static const CLI_Command_Definition_t xStatusRPi =
{
	( const int8_t * const ) "status-rpi",
	( const int8_t * const ) "",
	prvStatusRPi,
	0
};

static const CLI_Command_Definition_t xSerialLessMode =
{
	( const int8_t * const ) "serialless-mode",
	( const int8_t * const ) "serialless-mode:\r\n Enables <1> or disables <0> the Serial-Less Mode of the StromPi3\r\n\r\n",
	prvSerialLessMode,
	1
};

static const CLI_Command_Definition_t xBatLevelShutdown =
{
	( const int8_t * const ) "batlevel-shutdown",
	( const int8_t * const ) "batlevel-shutdown <level-number>:\r\n Configures the StromPi 3 to shutdown the Raspberry Pi when the Battery Level\r\n falls below the configured Battery-Voltagelevel:\r\n  Mode 0: Disabled\r\n  Mode 1: Below 10%\r\n  Mode 2: Below 25%\r\n  Mode 3: Below 50%\r\n\r\n",
	prvBatLevelShutdown,
	1
};

int ascii2int(const char* s);


#endif /* UART_COMMAND_CONSOLE_H */



