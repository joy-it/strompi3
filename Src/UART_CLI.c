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

/* Standard includes. */
#include "string.h"
#include <inttypes.h>


/*** STM32-HAL Includes ***/

#include "stm32f0xx_hal.h"

extern UART_HandleTypeDef huart1;
extern RTC_HandleTypeDef hrtc;

#include "cmsis_os.h"

/* FreeRTOS includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

#include "main.h"

uint8_t rx_ready = 0;
uint8_t console_start = 0;
uint8_t command_order = 0;

char firmwareVersion[5] = "v1.4";

/* FreeRTOS+IO includes. */

/* Example includes. */
#include "FreeRTOS_CLI.h"
#include <UART_CLI.h>

/* Dimensions the buffer into which input characters are placed. */
#define cmdMAX_INPUT_SIZE			50

/* Place holder for calls to ioctl that don't use the value parameter. */
#define cmdPARAMTER_NOT_USED		( ( void * ) 0 )

/* Block times of 50 and 500milliseconds, specified in ticks. */
#define cmd50ms						( ( void * ) ( 50UL / portTICK_RATE_MS ) )
#define cmd500ms					( ( void * ) ( 500UL / portTICK_RATE_MS ) )
/*-----------------------------------------------------------*/

/*
 * The task that implements the command console processing.
 */
static void prvUARTCommandConsoleTask(void const * pvParameters );
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);

/*-----------------------------------------------------------*/

/* Holds the handle of the task that implements the UART command console. */
static xTaskHandle xCommandConsoleTask = NULL;

static const int8_t * const pcNewLine = ( int8_t * ) "\r\n";
static const int8_t * const pcEndOfCommandOutputString = ( int8_t * ) "\r\n>";

/*-----------------------------------------------------------*/
osThreadId UARTCmdTaskHandle;

void vUARTCommandConsoleStart( void )
{


	/*** Creates the FreeRTOS Task for the Serial Console ***/

	xTaskCreate( 	prvUARTCommandConsoleTask,				/* The task that implements the command console. */
					( const int8_t * const ) "UARTCmd",		/* Text name assigned to the task.  This is just to assist debugging.  The kernel does not use this name itself. */
					configUART_COMMAND_CONSOLE_STACK_SIZE,	/* The size of the stack allocated to the task. */
					NULL,									/* The parameter is not used, so NULL is passed. */
					configUART_COMMAND_CONSOLE_TASK_PRIORITY,/* The priority allocated to the task. */
					&xCommandConsoleTask );					/* Used to store the handle to the created task. */


	/*** The available Commands are registered here.
	 * Please refer to the definition of the commands here at the bottom of this file (UART_CLI.c)
	 * and to the headerfile (UART_CLI.h)  ***/

	  FreeRTOS_CLIRegisterCommand( &xTimeOutput );
	  FreeRTOS_CLIRegisterCommand( &xADCOutput );
	  FreeRTOS_CLIRegisterCommand( &xMode );
	  FreeRTOS_CLIRegisterCommand( &xSetClock );
	  FreeRTOS_CLIRegisterCommand( &xSetDate );
	  FreeRTOS_CLIRegisterCommand( &xStartStromPiConsole );
	  FreeRTOS_CLIRegisterCommand( &xSetTimer );
	  FreeRTOS_CLIRegisterCommand( &xShutdownEnable );
	  FreeRTOS_CLIRegisterCommand( &xWarning );
	  FreeRTOS_CLIRegisterCommand( &xAlarmMode );
	  FreeRTOS_CLIRegisterCommand( &xAlarmEnable );
	  FreeRTOS_CLIRegisterCommand( &xAlarmTime );
	  FreeRTOS_CLIRegisterCommand( &xAlarmWeekday );
	  FreeRTOS_CLIRegisterCommand( &xAlarmDate );
	  FreeRTOS_CLIRegisterCommand( &xAlarmPowerOffTime );
	  FreeRTOS_CLIRegisterCommand( &xAlarmPowerOffEnable );
	  FreeRTOS_CLIRegisterCommand( &xShowStatus );
	  FreeRTOS_CLIRegisterCommand( &xPowerOff );
	  FreeRTOS_CLIRegisterCommand( &xTimeRPi );
	  FreeRTOS_CLIRegisterCommand( &xDateRPi );
	  FreeRTOS_CLIRegisterCommand( &xStatusRPi );
	  FreeRTOS_CLIRegisterCommand( &xSerialLessMode );
	  FreeRTOS_CLIRegisterCommand( &xBatLevelShutdown );
	  FreeRTOS_CLIRegisterCommand( &xQuitStromPiConsole );

}
/*-----------------------------------------------------------*/
/*** This defines the UART Console Task
 * Its main function is to check the serial interface for incoming Characters
 * which then are stored into an Receive-Buffer for processing.
 * If the console is enabled (through the flag "console_start==1"),
 * then the received character is echoed back through the serial interface,
 * so the user can see what have been typed into the console.
 * After the "Enter"-Key have been pressed (Character '\r')
 * the string which is stored in the ReceiveBuffer is sent
 * to the FreeRTOS+CLI subprocess, which compare it to the preregistered
 * command and process the command if it finds a match.
 * The output of the command is then sent out to the serial
 * interface, when the console is enabled - there a special
 * commands (like dateRpi) which can bypass a deactivated console
 * through the flag command_order=1. This is used to communicate
 * with the StromPi3 through scripts, where an input into the console
 * isn't needed ***/


static void prvUARTCommandConsoleTask(void const * pvParameters )
{
int8_t cRxedChar, cInputIndex = 0, *pcOutputString;
static int8_t cInputString[ cmdMAX_INPUT_SIZE ], cLastInputString[ cmdMAX_INPUT_SIZE ];
portBASE_TYPE xReturned;

	( void ) pvParameters;

	/* Obtain the address of the output buffer.  Note there is no mutual
	exclusion on this buffer as it is assumed only one command console
	interface will be used at any one time. */
	pcOutputString = FreeRTOS_CLIGetOutputBuffer();

	/* Send the welcome message. */
	volatile UBaseType_t uxHighWaterMark;

	uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL );


	for( ;; )
	{
		/* Only interested in reading one character at a time. */

		uxHighWaterMark = uxTaskGetStackHighWaterMark( NULL );


		/*** Process the Serial Interface Interrupt and copy a received Character
		 * into the predesignated buffer.
		 * The whole task waits here in the while-loop until an interrupt gives a
		 * signal for a processed character. ***/
		while(rx_ready != 1)
		{
			HAL_UART_Receive_IT(&huart1, (uint8_t *) &cRxedChar, 1 );
		}
		rx_ready = 0;

		/* Echo the character back. */
		if(UART_CheckIdleState(&huart1) == HAL_OK && console_start == 1)
		{
		  HAL_UART_Transmit(&huart1, (uint8_t *) &cRxedChar, sizeof( cRxedChar ), sizeof( cRxedChar ) );
		}

		/*** Return-Key have been pressed ***/
		if( cRxedChar == '\r' )
		{
			/* The input command string is complete.  Ensure the previous
			UART transmission has finished before sending any more data.
			This task will be held in the Blocked state while the Tx completes,
			if it has not already done so, so no CPU time will be wasted by
			polling. */
			  if(UART_CheckIdleState(&huart1) == HAL_OK && console_start == 1)
				  {
					HAL_UART_Transmit(&huart1, (uint8_t *) pcNewLine, strlen( ( char * ) pcNewLine ), strlen( ( char * ) pcNewLine ) );
				  }
			/* See if the command is empty, indicating that the last command is
			to be executed again. */
			if( cInputIndex == 0 )
			{
				strcpy( ( char * ) cInputString, ( char * ) cLastInputString );
			}

			/* Pass the received command to the command interpreter.  The
			command interpreter is called repeatedly until it returns
			pdFALSE as it might generate more than one string. */
			do
			{
				/* Once again, just check to ensure the UART has completed
				sending whatever it was sending last.  This task will be held
				in the Blocked state while the Tx completes, if it has not
				already done so, so no CPU time	is wasted polling. */
				if(UART_CheckIdleState(&huart1) == HAL_OK)
				  xReturned = pdPASS;
                                
				if( xReturned == pdPASS )
				{
					/* Get the string to write to the UART from the command
					interpreter. */
					xReturned = FreeRTOS_CLIProcessCommand( cInputString, pcOutputString, configCOMMAND_INT_MAX_OUTPUT_SIZE );

					/* Write the generated string to the UART. */
					if (console_start == 1 || command_order == 1)
					{
						HAL_UART_Transmit(&huart1, (uint8_t *) pcOutputString, strlen( ( char * ) pcOutputString ), strlen( ( char * ) pcOutputString ) );
						command_order = 0;
					}
				}

			} while( xReturned != pdFALSE );

			/* All the strings generated by the input command have been sent.
			Clear the input	string ready to receive the next command.  Remember
			the command that was just processed first in case it is to be
			processed again. */
			strcpy( ( char * ) cLastInputString, ( char * ) cInputString );
			cInputIndex = 0;
			memset( cInputString, 0x00, cmdMAX_INPUT_SIZE );

			/* Ensure the last string to be transmitted has completed. */
            if(UART_CheckIdleState(&huart1) == HAL_OK && console_start == 1)
            {
            	HAL_UART_Transmit(&huart1, (uint8_t *) pcEndOfCommandOutputString, strlen( ( char * ) pcEndOfCommandOutputString ), strlen( ( char * ) pcEndOfCommandOutputString ) );

            }
		}
		else
		{
			if( cRxedChar == '\r' )
			{
				/* Ignore the character. */
			}
			else if( cRxedChar == '\b' )
			{
				/* Backspace was pressed.  Erase the last character in the
				string - if any. */
				if( cInputIndex > 0 )
				{
					cInputIndex--;
					cInputString[ cInputIndex ] = '\0';
				}
			}
			else
			{
				/* A character was entered.  Add it to the string
				entered so far.  When a \n is entered the complete
				string will be passed to the command interpreter. */
				if( ( cRxedChar >= ' ' ) && ( cRxedChar <= '~' ) )
				{
					if( cInputIndex < cmdMAX_INPUT_SIZE )
					{
						cInputString[ cInputIndex ] = cRxedChar;
						cInputIndex++;
					}
				}
			}
		}
	}
}

/*-----------------------------------------------------------*/

/*** In the following section you'll find the definition of the preregistered Commands
 * Please refer also to the UART_CLI.h file***/

/*** prvADCOutput
 * This command outputs the measured Voltages which are connected to the StromPi3 ***/

static portBASE_TYPE prvADCOutput( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;


	if (rawValue[0] > minWide)
	{
		sprintf(( char * ) pcWriteBuffer, "****************************\r\nWide-Range-Inputvoltage: %d.%03d V",  measuredValue[0]/1000, measuredValue[0]%1000);
	}
	else
	{
		sprintf(( char * ) pcWriteBuffer, "****************************\r\nWide-Range-Inputvoltage: not connected");
	}
	if (rawValue[1] > minBatConnect)
	{
		sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\nLifePo4-Batteryvoltage: %d.%03d V", measuredValue[1]/1000, measuredValue[1]%1000);

		switch (batLevel)
			    {
			    	case 1:
			    				sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer)," [10%%]");
								break;

			    	case 2:
			    				sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer)," [25%%]");
			    	    		break;

			    	case 3:
			    				sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer)," [50%%]");
			    	    		break;

			    	case 4:
			    				sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer)," [100%%]");
			    	    		break;

			    }

		if (charging == 1)
		{
			sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer)," [charging]");
		}
	}
	else
	{
		sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\nLifePo4-Batteryvoltage: not connected");
	}
	if (rawValue[2] > minUSB)
	{
		sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\nmicroUSB-Inputvoltage: %d.%03d V", measuredValue[2]/1000, measuredValue[2]%1000);
	}
	else
	{
		sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\nmicroUSB-Inputvoltage: not connected");
	}
	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\nOutput-Voltage: %d.%03d V\r\n****************************\r\n", measuredValue[3]/1000, measuredValue[3]%1000);

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}
/*-----------------------------------------------------------*/

/*** prvMode
 * This command changes the mode of the StromPi3, which defines the primary and the secondary backup voltage input
 *
 *  1: mUSB (primary) -> Wide (secondary)
 *  2: Wide (primary) -> mUSB (secondary)
 *  3: mUSB (primary) -> Battery (secondary)
 *  4: Wide (primary) -> Battery (secondary)
 *
 * ***/

static portBASE_TYPE prvMode( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
const int8_t *const pcMessage = ( int8_t * ) "****************************\r\nMode has been changed\r\n\n****************************\n";
int8_t *pcParameter1;
BaseType_t xParameter1StringLength;

pcParameter1 = FreeRTOS_CLIGetParameter
                    (
                      /* The command string itself. */
                      pcCommandString,
                      /* Return the first parameter. */
                      1,
                      /* Store the parameter string length. */
                      &xParameter1StringLength
                    );

   /*** The parameter which have been included into the entered
    * command is saved into the "modus" variable  ***/

	modus = ascii2int(pcParameter1);

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	strcpy( ( char * ) pcWriteBuffer, ( char * ) pcMessage );

    /*** The updated "modus"-variable is written into the flash ***/
	flashConfig();

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}
/*-----------------------------------------------------------*/

/*** prvTimeOutput
 * This command shows the actual time of the STM32 RTC-Module
 * ***/

static portBASE_TYPE prvTimeOutput( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	RTC_TimeTypeDef stimestructureget;
	RTC_DateTypeDef sdatestructureget;

	HAL_RTC_GetTime(&hrtc, &stimestructureget, RTC_FORMAT_BIN);
	HAL_RTC_GetDate(&hrtc, &sdatestructureget, RTC_FORMAT_BIN);

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	sprintf(( char * ) pcWriteBuffer,"%02d:%02d:%02d",stimestructureget.Hours, stimestructureget.Minutes, stimestructureget.Seconds);


	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}
/*-----------------------------------------------------------*/

/*** prvSetClock
 * This command changes the time which is currently used in the STM32 RTC-Module
 *
 * ***/

static portBASE_TYPE prvSetClock( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t hour;
	uint8_t min;
	uint8_t sec;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );
	int8_t *pcParameter2;
	BaseType_t xParameter2StringLength;

	pcParameter2 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      2,
	                      /* Store the parameter string length. */
	                      &xParameter2StringLength
	                    );

	int8_t *pcParameter3;
	BaseType_t xParameter3StringLength;

	pcParameter3 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      3,
	                      /* Store the parameter string length. */
	                      &xParameter3StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;
    pcParameter2[ xParameter2StringLength ] = 0x00;
    pcParameter3[ xParameter3StringLength ] = 0x00;

	hour = ascii2int(pcParameter1);
	min = ascii2int(pcParameter2);
	sec = ascii2int(pcParameter3);

	RTC_TimeTypeDef  stimestructure;

	stimestructure.Hours = hour;
	stimestructure.Minutes = min;
	stimestructure.Seconds = sec;
	stimestructure.DayLightSaving = RTC_DAYLIGHTSAVING_NONE ;
	stimestructure.StoreOperation = RTC_STOREOPERATION_RESET;

	if(HAL_RTC_SetTime(&hrtc,&stimestructure,RTC_FORMAT_BIN) != HAL_OK)
	{
	/* Initialization Error */
		Error_Handler();
	}

	sprintf(( char * ) pcWriteBuffer,"The clock has been set to %02d:%02d:%02d",stimestructure.Hours, stimestructure.Minutes, stimestructure.Seconds);


	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvSetDate
 * This command changes the date which is currently used in the STM32 RTC-Module
 *
 * ***/


static portBASE_TYPE prvSetDate( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t day;
	uint8_t month;
	uint8_t year;
	uint8_t weekday;
	char weekday_message[20];

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );
	int8_t *pcParameter2;
	BaseType_t xParameter2StringLength;

	pcParameter2 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      2,
	                      /* Store the parameter string length. */
	                      &xParameter2StringLength
	                    );

	int8_t *pcParameter3;
	BaseType_t xParameter3StringLength;

	pcParameter3 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      3,
	                      /* Store the parameter string length. */
	                      &xParameter3StringLength
	                    );

	int8_t *pcParameter4;
		BaseType_t xParameter4StringLength;

		pcParameter4 = FreeRTOS_CLIGetParameter
		                    (
		                      /* The command string itself. */
		                      pcCommandString,
		                      /* Return the first parameter. */
		                      4,
		                      /* Store the parameter string length. */
		                      &xParameter4StringLength
		                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;
    pcParameter2[ xParameter2StringLength ] = 0x00;
    pcParameter3[ xParameter3StringLength ] = 0x00;
    pcParameter4[ xParameter4StringLength ] = 0x00;

	day = ascii2int(pcParameter1);
	month = ascii2int(pcParameter2);
	year = ascii2int(pcParameter3);
	weekday = ascii2int(pcParameter4);

	RTC_DateTypeDef  sdatestructure;

	sdatestructure.Year = year;
	sdatestructure.Month = month;
	sdatestructure.Date = day;
	sdatestructure.WeekDay = weekday;

	if(HAL_RTC_SetDate(&hrtc,&sdatestructure,RTC_FORMAT_BIN) != HAL_OK)
	{
	/* Initialization Error */
		Error_Handler();
	}

	switch (weekday)
	{
		case 1: strcpy(weekday_message, "Monday"); break;
		case 2: strcpy(weekday_message, "Tuesday"); break;
		case 3: strcpy(weekday_message, "Wednesday"); break;
		case 4: strcpy(weekday_message, "Thursday"); break;
		case 5: strcpy(weekday_message, "Friday"); break;
		case 6: strcpy(weekday_message, "Saturday"); break;
		case 7: strcpy(weekday_message, "Sunday"); break;
	}

	sprintf(( char * ) pcWriteBuffer,"The date has been set to %s %02d.%02d.20%02d", weekday_message, sdatestructure.Date, sdatestructure.Month, sdatestructure.Year);


	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}
/*-----------------------------------------------------------*/

/*** prvSetTimer
 * This command sets the seconds for the Shutdown-Timer
 *
 * ***/

static portBASE_TYPE prvSetTimer( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint16_t timer_sec;

	int16_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

    timer_sec = ascii2int(pcParameter1);

    shutdown_time = timer_sec;

    flashConfig();

	sprintf(( char * ) pcWriteBuffer,"The Shutdown-Timer has been set to %02d seconds", timer_sec);


	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}
/*-----------------------------------------------------------*/

/*** prvStartStromPiConsole
 *
 * This command enables the console output for the user.
 * The StromPi3 have two possibilities to send out the command-output to the Raspberry Pi
 *
 * - When the console_start flag is set to 1: This means that the user wants to configure the StromPi3 through the serial interface
 * - When the command_order flag is set to 1: This means that the output of the command can bypass a deactivated output - this is used to communicate with the StromPi3 through Scripts
 *
 * prvStartStromPiConsole sets the "console_start" flag to 1
 *
 * ***/

static portBASE_TYPE prvStartStromPiConsole( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
const int8_t *const pcMessage = ( int8_t * ) "\r\n------------------------------\r\nWelcome to the StromPi 3 Console\r\n------------------------------\r\nType ""help"" to view a list of available commands.\r\n\r\n[When you press ENTER the previous command would be executed again]\r\n";

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	console_start = 1;

	strcpy( ( char * ) pcWriteBuffer, ( char * ) pcMessage );

	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvQuitStromPiConsole
 *
 * This command disables the console output for the user.
 *
 * prvQuitStromPiConsole sets the "console_start" flag to 0
 *
 * ***/

static portBASE_TYPE prvQuitStromPiConsole( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
const int8_t *const pcMessage = ( int8_t * ) "";

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	console_start = 0;

	strcpy( ( char * ) pcWriteBuffer, ( char * ) pcMessage );

	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvPowerOff
 *
 * With this command it is possible to manual shut down the Raspberry Pi (through the "shutdown"-message)
 * and change the StromPi3 into its PowerOff-state - this would be needed for the Scheduler-System (main.c -> Alarmhandler())
 *
 * ***/

static portBASE_TYPE prvPowerOff( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
const int8_t *const pcMessage = ( int8_t * ) "\r\n Raspberry Pi Shutdown\r\n";

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	poweroff_flag = 1;
	ShutdownRPi();

	strcpy( ( char * ) pcWriteBuffer, ( char * ) pcMessage );

	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvTimeRPi
 *
 * This command is for programming the RTC Time through a script. (Like the RTCSerial.py script)
 *
 * It uses the command_order=1 flag to bypass a deactivated console_output to communicate directly to the Script executed by the Raspberry Pi
 *
 * ***/

static portBASE_TYPE prvTimeRPi( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	uint32_t time;

	RTC_TimeTypeDef stimestructureget;
	RTC_DateTypeDef sdatestructureget;

	HAL_RTC_GetTime(&hrtc, &stimestructureget, RTC_FORMAT_BIN);
	HAL_RTC_GetDate(&hrtc, &sdatestructureget, RTC_FORMAT_BIN);

	time = stimestructureget.Hours * 10000 + stimestructureget.Minutes * 100 + stimestructureget.Seconds;

	command_order = 1;

	sprintf(( char * ) pcWriteBuffer, "%lu" , time);

	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvDateRPi
 *
 * This command is for programming the RTC Date through a script. (Like the RTCSerial.py script)
 *
 * It uses the command_order=1 flag to bypass a deactivated console_output to communicate directly to the Script executed by the Raspberry Pi
 *
 * ***/

static portBASE_TYPE prvDateRPi( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	uint32_t date;

	RTC_TimeTypeDef stimestructureget;
	RTC_DateTypeDef sdatestructureget;

	HAL_RTC_GetTime(&hrtc, &stimestructureget, RTC_FORMAT_BIN);
	HAL_RTC_GetDate(&hrtc, &sdatestructureget, RTC_FORMAT_BIN);

	date = sdatestructureget.Year * 10000 + sdatestructureget.Month * 100 + sdatestructureget.Date;

	command_order = 1;

	sprintf(( char * ) pcWriteBuffer, "%lu" ,date);

	return pdFALSE;
}


/*-----------------------------------------------------------*/

/*** prvStatusRPi
 *
 * This command is needed for the StromPi3_Status.py script.
 * It is gathering all of the variables currently active and prepares them for transfer
 * through the serial interface.
 *
 * ***/

static portBASE_TYPE prvStatusRPi( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	uint16_t time;
	uint32_t date;
	uint8_t alarm_mode_tmp;
	uint8_t alarm_time_tmp;
	uint8_t alarm_date_tmp;
	uint8_t alarm_weekday_tmp;
	uint8_t alarm__tmp;


	RTC_TimeTypeDef stimestructureget;
	RTC_DateTypeDef sdatestructureget;

	HAL_RTC_GetTime(&hrtc, &stimestructureget, RTC_FORMAT_BIN);
	HAL_RTC_GetDate(&hrtc, &sdatestructureget, RTC_FORMAT_BIN);

	date = sdatestructureget.Year * 10000 + sdatestructureget.Month * 100 + sdatestructureget.Date;
	time = stimestructureget.Hours * 10000 + stimestructureget.Minutes * 100 + stimestructureget.Seconds;

	command_order = 1;

	sprintf(( char * ) pcWriteBuffer, "%lu\n" , time);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", date);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", sdatestructureget.WeekDay);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", modus);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_enable);

	if(alarmTime == 1)
		alarm_mode_tmp=1;
	else if(alarmDate == 1)
		alarm_mode_tmp=2;
	else if(alarmWeekDay == 1)
		alarm_mode_tmp=3;


	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_mode_tmp);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_hour);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_min);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_day);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_month);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_weekday);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarmPoweroff);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_hour_off);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", alarm_min_off);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", shutdown_enable);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", shutdown_time);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", warning_enable);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", serialLessMode);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", batLevel_shutdown);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", batLevel);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", charging);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", measuredValue[0]);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", measuredValue[1]);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", measuredValue[2]);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "%lu\n", measuredValue[3]);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), firmwareVersion);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\n");

	return pdFALSE;


}


/*-----------------------------------------------------------*/

/*** prvAlarmMode
 * This command changes the Alarmmode of the StromPi3 Scheduling System.
 * When the StromPi 3 have shutted down the Raspberry Pi and changed to its PowerOff-state
 * it s possible to wake the system up through one of the following Alarms
 *
 * - alarmTime: this alarm triggers every time the preprogrammed clock time have been reached
 * - alarmWeekDay: this alarm triggers every time the preprogrammed weekday have been reached (for example every monday)
 * - alarmDate: this alarm triggers every time the preprogrammed date have been reached (for example every first march of the year)
 *
 * ***/

static portBASE_TYPE prvAlarmMode( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t alarm_modus;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

    alarm_modus = ascii2int(pcParameter1);

    switch (alarm_modus)
    {
    	case 1:
					alarmTime = 1;
					alarmDate = 0;
					alarmWeekDay = 0;

					flashConfig();
					sprintf(( char * ) pcWriteBuffer,"The WakeUp-Alarm has been set to ""Time-Alarm""");
					break;

    	case 2:
    	    		alarmTime = 0;
    	    		alarmDate = 1;
    	    		alarmWeekDay = 0;

    	    		flashConfig();
    	    		sprintf(( char * ) pcWriteBuffer,"The WakeUp-Alarm has been set to ""Date-Alarm""");
    	    		break;

    	case 3:
    	    		alarmTime = 0;
    	    		alarmDate = 0;
    	    		alarmWeekDay = 1;

    	    		flashConfig();
    	    		sprintf(( char * ) pcWriteBuffer,"The WakeUp-Alarm has been set to ""Weekday-Alarm""");
    	    		break;

    }

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvAlarmEnable
 * This command enables or disables the StromPi3 Wakeup Scheduling System
 *
 * ***/

static portBASE_TYPE prvAlarmEnable( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t alarm_enable_temp;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

    alarm_enable_temp = ascii2int(pcParameter1);

    alarm_enable = alarm_enable_temp;

    flashConfig();

    switch (alarm_enable)
        {
        	case 0:
    					sprintf(( char * ) pcWriteBuffer,"The WakeUp-Alarm has been disabled");
    					break;

        	case 1:
        	    		sprintf(( char * ) pcWriteBuffer,"The WakeUp-Alarm has been enabled");
        	    		break;

        }

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvAlarmTime
 * This command sets the Time for the StromPi3 Wakeup Scheduling System
 *
 * ***/

static portBASE_TYPE prvAlarmTime( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t hour;
	uint8_t min;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );
	int8_t *pcParameter2;
	BaseType_t xParameter2StringLength;

	pcParameter2 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      2,
	                      /* Store the parameter string length. */
	                      &xParameter2StringLength
	                    );


	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;
    pcParameter2[ xParameter2StringLength ] = 0x00;

	hour = ascii2int(pcParameter1);
	min = ascii2int(pcParameter2);

	alarm_hour = hour;
	alarm_min = min;

	flashConfig();



	sprintf(( char * ) pcWriteBuffer,"The WakeUp-Alarm has been set to %02d:%02d", hour , min);


	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvAlarmWeekday
 * This command sets the WeekDay for the StromPi3 Wakeup Scheduling System
 *
 *  1 -> Monday
 *  2 -> Tuesday
 *  3 -> Wednesday
 *  4 -> Thursday
 *  5 -> Friday
 *  6 -> Saturday
 *  7 -> Sunday
 *
 * ***/


static portBASE_TYPE prvAlarmWeekday( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t weekday;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );


	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

	weekday = ascii2int(pcParameter1);

	alarm_weekday = weekday;

	flashConfig();

	char weekday_message[20];

	switch(weekday)
	{
		case 1: strcpy(weekday_message, "Monday"); break;
		case 2: strcpy(weekday_message, "Tuesday"); break;
		case 3: strcpy(weekday_message, "Wednesday"); break;
		case 4: strcpy(weekday_message, "Thursday"); break;
		case 5: strcpy(weekday_message, "Friday"); break;
		case 6: strcpy(weekday_message, "Saturday"); break;
		case 7: strcpy(weekday_message, "Sunday"); break;
	}

	sprintf(( char * ) pcWriteBuffer,"The Weekday-Alarm has been set to %s", weekday_message);


	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvAlarmDate
 * This command sets the Date for the StromPi3 Wakeup Scheduling System
 *
 * ***/

static portBASE_TYPE prvAlarmDate( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t day;
	uint8_t month;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );
	int8_t *pcParameter2;
	BaseType_t xParameter2StringLength;

	pcParameter2 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      2,
	                      /* Store the parameter string length. */
	                      &xParameter2StringLength
	                    );



	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;
    pcParameter2[ xParameter2StringLength ] = 0x00;


	day = ascii2int(pcParameter1);
	month = ascii2int(pcParameter2);

	alarm_day = day;
	alarm_month = month;

	flashConfig();

	sprintf(( char * ) pcWriteBuffer,"The date of the Date-Alarm has been set to %02d.%02d", alarm_day, alarm_month);

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvAlarmPowerOffTime
 * This command sets the Time for the StromPi3 Shutdown Scheduling System.
 *
 * With this it is possible to shutdown the Raspberry Pi to a preconfigured time and
 * put the StromPi 3 into its Shutdown-state
 *
 * ***/

static portBASE_TYPE prvAlarmPowerOffTime( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t hour;
	uint8_t min;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );
	int8_t *pcParameter2;
	BaseType_t xParameter2StringLength;

	pcParameter2 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      2,
	                      /* Store the parameter string length. */
	                      &xParameter2StringLength
	                    );


	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;
    pcParameter2[ xParameter2StringLength ] = 0x00;

	hour = ascii2int(pcParameter1);
	min = ascii2int(pcParameter2);

	alarm_hour_off = hour;
	alarm_min_off = min;

	flashConfig();

	sprintf(( char * ) pcWriteBuffer,"The time of the Time-Alarm has been set to %02d:%02d",alarm_hour_off, alarm_min_off);

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvAlarmPowerOffEnable
 * This command enable or disables the StromPi3 Shutdown Scheduling System.
 *
 * With this it is possible to shutdown the Raspberry Pi to a preconfigured time and
 * put the StromPi 3 into its Shutdown-state
 *
 * ***/

static portBASE_TYPE prvAlarmPowerOffEnable( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t poweroff_enable_temp;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

    poweroff_enable_temp = ascii2int(pcParameter1);

    alarmPoweroff = poweroff_enable_temp;

    flashConfig();

    switch (alarmPoweroff)
        {
        	case 0:
    					sprintf(( char * ) pcWriteBuffer,"The PowerOff-Alarm has been disabled");
    					break;

        	case 1:
        	    		sprintf(( char * ) pcWriteBuffer,"The PowerOff-Alarm has been enabled");
        	    		break;

        }

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvWarning
 * This command enable or disables the powerfail Warning, if the primary voltage source have failed
 *
 * ***/

static portBASE_TYPE prvWarning( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t warning_enable_temp;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

    warning_enable_temp = ascii2int(pcParameter1);

    warning_enable = warning_enable_temp;

    flashConfig();

    switch (warning_enable)
        {
        	case 0:
    					sprintf(( char * ) pcWriteBuffer,"The Powerfail Warning has been deactivated");
    					break;

        	case 1:
        	    		sprintf(( char * ) pcWriteBuffer,"The Powerfail Warning has been enabled");
        	    		break;

        }

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}


/*-----------------------------------------------------------*/

/*** prvShutdownEnable
 * This command enable or disables the shutdown-timer.
 * It is one of the main functions of the StromPi 3: In the case of a powerfailure at the configured primary voltage source
 * the StromPi3 sends a warning to the Raspberry Pi, so it can safely shutdown its OS; after that the StromPi3
 * starts its shutdown-timer and cut off the RPi from the backup source.
 *
 * ***/

static portBASE_TYPE prvShutdownEnable( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t shutdown_enable_temp;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

    shutdown_enable_temp = ascii2int(pcParameter1);

    shutdown_enable = shutdown_enable_temp;

    flashConfig();

    switch (shutdown_enable)
        {
        	case 0:
    					sprintf(( char * ) pcWriteBuffer,"The Raspberry-Pi Shutdown has been deactivated");
    					break;

        	case 1:
        	    		sprintf(( char * ) pcWriteBuffer,"The Raspberry-Pi Shutdown has been enabled");
        	    		break;

        }

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvBatLevelShutdown
 *  This command configures the Batterylevel-Shutdown function.
 *  The Battery-Voltage is measured and then mapped on 4 available voltage levels (1:10%, 2:25%, 3:50%, 4:100%)
 *  at the end of the main-Task. In the case the Batterylevel-Shutdown is configured,
 *  the StromPi3 give a shutdown-signal to the Raspberry Pi and cuts of the PowerPath in a fixed 10 seconds timer,
 *  when the Battery has been discharged to the configured level. *
 *
 * ***/

static portBASE_TYPE prvBatLevelShutdown( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t batLevel_shutdown_temp;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

    batLevel_shutdown_temp = ascii2int(pcParameter1);

    batLevel_shutdown = batLevel_shutdown_temp;

    flashConfig();

    switch (batLevel_shutdown)
        {

			case 0:
						sprintf(( char * ) pcWriteBuffer,"The Battery-Level Shutdown has been disabled");
						break;
        	case 1:
    					sprintf(( char * ) pcWriteBuffer,"The Battery-Level Shutdown has been configured to 10%%");
    					break;
        	case 2:
        	    		sprintf(( char * ) pcWriteBuffer,"The Battery-Level Shutdown has been configured to 25%%");
        	    		break;
        	case 3:
    					sprintf(( char * ) pcWriteBuffer,"The Battery-Level Shutdown has been configured to 50%%");
    					break;

        }

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** prvSerialLessMode
 *
 * If the Serial-Interface is blocked by another HAT or an other module,
 * it is possible to use the StromPi3 in a Serial-Less Mode.
 * In this case the Shutdown-Signal is not sent out through the serial Interface as a message,
 * but is indicated through a connected GPIO-LINE (Like in the previous versions of the StromPi family)
 * As for this needed extra connection, please refer to the manuals located in the "SerialLess" Folder
 *
 * ***/

static portBASE_TYPE prvSerialLessMode( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{

	uint8_t serialLessMode_temp;

	int8_t *pcParameter1;
	BaseType_t xParameter1StringLength;

	pcParameter1 = FreeRTOS_CLIGetParameter
	                    (
	                      /* The command string itself. */
	                      pcCommandString,
	                      /* Return the first parameter. */
	                      1,
	                      /* Store the parameter string length. */
	                      &xParameter1StringLength
	                    );

	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

    pcParameter1[ xParameter1StringLength ] = 0x00;

    serialLessMode_temp = ascii2int(pcParameter1);

    serialLessMode = serialLessMode_temp;

    flashConfig();

    switch (serialLessMode_temp)
        {
        	case 0:
    					sprintf(( char * ) pcWriteBuffer,"The StromPi3 Serial-Less Mode has been deactivated");
    					break;

        	case 1:
        	    		sprintf(( char * ) pcWriteBuffer,"The StromPi3 Serial-Less Mode has been enabled");
        	    		break;

        }

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}


/*-----------------------------------------------------------*/

/*** prvShowStatus
 * This command sums up all of the configuration data in the StromPi 3
 * and outputs it into the serial console.
 *
 * ***/

static portBASE_TYPE prvShowStatus ( int8_t *pcWriteBuffer, size_t xWriteBufferLen, const int8_t *pcCommandString )
{
	( void ) pcCommandString;
	configASSERT( pcWriteBuffer );

	/* This function assumes the buffer length is adequate. */
	( void ) xWriteBufferLen;

	RTC_TimeTypeDef stimestructureget;
	RTC_DateTypeDef sdatestructureget;

	HAL_RTC_GetTime(&hrtc, &stimestructureget, RTC_FORMAT_BIN);
	HAL_RTC_GetDate(&hrtc, &sdatestructureget, RTC_FORMAT_BIN);

	sprintf(( char * ) pcWriteBuffer, "\r\n Time: %02d:%02d:%02d", stimestructureget.Hours, stimestructureget.Minutes, stimestructureget.Seconds);

	char temp_message[20];

	switch (sdatestructureget.WeekDay)
		{
			case 1: strcpy(temp_message, "Monday"); break;
			case 2: strcpy(temp_message, "Tuesday"); break;
			case 3: strcpy(temp_message, "Wednesday"); break;
			case 4: strcpy(temp_message, "Thursday"); break;
			case 5: strcpy(temp_message, "Friday"); break;
			case 6: strcpy(temp_message, "Saturday"); break;
			case 7: strcpy(temp_message, "Sunday"); break;
		}

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n Date: %s %02d.%02d.20%02d\r\n", temp_message, sdatestructureget.Date, sdatestructureget.Month, sdatestructureget.Year);

	switch(modus)
	{
	case 1:	strcpy(temp_message, "mUSB -> Wide"); break;
	case 2: strcpy(temp_message, "Wide -> mUSB"); break;
	case 3:	strcpy(temp_message, "mUSB -> Battery"); break;
	case 4: strcpy(temp_message,"Wide -> Battery"); break;
	}
	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n StromPi-Mode: %s \r\n", temp_message);


	switch(alarm_enable)
	{
	case 0:	strcpy(temp_message, "Disabled"); break;
	case 1: strcpy(temp_message, "Enabled"); break;
	}
	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n WakeUp-Alarm: %s ", temp_message);


	if(alarmTime == 1)
		strcpy(temp_message, "Time-Alarm");
	else if(alarmDate == 1)
		strcpy(temp_message, "Date-Alarm");
	else if(alarmWeekDay == 1)
		strcpy(temp_message, "Weekday-Alarm");

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n  Alarm-Mode: %s ", temp_message);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n  Alarm-Time: %02d:%02d", alarm_hour, alarm_min);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n  Alarm-Date: %02d.%02d", alarm_day, alarm_month);

	switch (alarm_weekday)
		{
			case 1: strcpy(temp_message, "Monday"); break;
			case 2: strcpy(temp_message, "Tuesday"); break;
			case 3: strcpy(temp_message, "Wednesday"); break;
			case 4: strcpy(temp_message, "Thursday"); break;
			case 5: strcpy(temp_message, "Friday"); break;
			case 6: strcpy(temp_message, "Saturday"); break;
			case 7: strcpy(temp_message, "Sunday"); break;
		}

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n  Alarm-Weekday: %s \r\n", temp_message);

	switch(alarmPoweroff)
		{
		case 0:	strcpy(temp_message, "Disabled"); break;
		case 1: strcpy(temp_message, "Enabled"); break;
		}
	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n PowerOff-Alarm: %s ", temp_message);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n  PowerOff-Alarm-Time: %02d:%02d\r\n", alarm_hour_off, alarm_min_off);

	switch(shutdown_enable)
			{
			case 0:	strcpy(temp_message, "Disabled"); break;
			case 1: strcpy(temp_message, "Enabled"); break;
			}
	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n Raspberry Pi Shutdown: %s ", temp_message);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n  Shutdown-Timer: %d seconds", shutdown_time);

	switch(warning_enable)
				{
				case 0:	strcpy(temp_message, "Disabled"); break;
				case 1: strcpy(temp_message, "Enabled"); break;
				}
		sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n\r\n Powerfail Warning: %s ", temp_message);

	switch(serialLessMode)
					{
					case 0:	strcpy(temp_message, "Disabled"); break;
					case 1: strcpy(temp_message, "Enabled"); break;
					}
			sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n\r\n Serial-Less Mode: %s ", temp_message);

	switch(batLevel_shutdown)
						{
							case 0:
								sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n\r\n Battery-Level Shutdown: Disabled");
										break;
							case 1:
								sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n\r\n Battery-Level Shutdown: 10%%");
										break;
							case 2:
								sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n\r\n Battery-Level Shutdown: 25%%");
										break;
							case 3:
								sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n\r\n Battery-Level Shutdown: 50%%");
										break;
						}

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), "\r\n\r\n FirmwareVersion: ", temp_message);

	sprintf(( char * ) pcWriteBuffer + strlen(( char * ) pcWriteBuffer), firmwareVersion, temp_message);

	/* There is no more data to return after this single string, so return
	pdFALSE. */
	return pdFALSE;
}

/*-----------------------------------------------------------*/

/*** ascii2int
 * This is a help function to convert the input of the user into the correct format for storing into the associated variables
 *
 * ***/

int ascii2int(const char* s)
{
	int i = 0;
	while (*s != 0)
	{
		if (*s >= '0' && *s <= '9')
		{
			i = i * 10 + (*s - '0');
			s++;
		}
		else return 0;
	}
	return i;

}

/*-----------------------------------------------------------*/

/*** HAL_UART_RxCpltCallback
 * This is the STM32 Hal UART Interrupt Callback
 *
 * ***/

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{

	rx_ready = 1;
}

