
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * This notice applies to any and all portions of this file
  * that are not between comment pairs USER CODE BEGIN and
  * USER CODE END. Other portions of this file, whether 
  * inserted by the user or by software development tools
  * are owned by their respective copyright owners.
  *
  * Copyright (c) 2018 STMicroelectronics International N.V. 
  * All rights reserved.
  *
  * Redistribution and use in source and binary forms, with or without 
  * modification, are permitted, provided that the following conditions are met:
  *
  * 1. Redistribution of source code must retain the above copyright notice, 
  *    this list of conditions and the following disclaimer.
  * 2. Redistributions in binary form must reproduce the above copyright notice,
  *    this list of conditions and the following disclaimer in the documentation
  *    and/or other materials provided with the distribution.
  * 3. Neither the name of STMicroelectronics nor the names of other 
  *    contributors to this software may be used to endorse or promote products 
  *    derived from this software without specific written permission.
  * 4. This software, including modifications and/or derivative works of this 
  *    software, must execute solely and exclusively on microcontroller or
  *    microprocessor devices manufactured by or for STMicroelectronics.
  * 5. Redistribution and use of this software other than as permitted under 
  *    this license is void and will automatically terminate your rights under 
  *    this license. 
  *
  * THIS SOFTWARE IS PROVIDED BY STMICROELECTRONICS AND CONTRIBUTORS "AS IS" 
  * AND ANY EXPRESS, IMPLIED OR STATUTORY WARRANTIES, INCLUDING, BUT NOT 
  * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
  * PARTICULAR PURPOSE AND NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY
  * RIGHTS ARE DISCLAIMED TO THE FULLEST EXTENT PERMITTED BY LAW. IN NO EVENT 
  * SHALL STMICROELECTRONICS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
  * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
  * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
  * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
  * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
  * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */



/************************************************************************************************************************************************************

StromPi v3 - by Joy-IT
OpenSource-Firmware published under MIT-License

/************************************************************************************************************************************************************

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

 	The Files are created in the Atollic TrueSTUDIO for STM32, which can be used for STM32 for free.
 	You can include the .cproject file in the IDE and start to code your own modifications
 	and debug them with a ST-Linkv2 connected to the StromPi3 or make your own binary which can be flashed
 	with the stm32flasher in flashmode of the StromPi 3
 	(Please refer to the manual provided in our firmware updates in the download section of strompi.joy-it.net)

 	(connections have to be soldered for InCircuit debugging- please refer to the additional Files provided in the OpenSource Package for the right pinout)

 	Please refer to the additional comments in the corresponding sections for further explanations.

	If there are questions or something is unclear, please feel free
	to contact us via E-Mail: service@joy-it.net
*/


/***********************************************************************************************************************************************************/

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f0xx_hal.h"
#include "cmsis_os.h"

/* USER CODE BEGIN Includes */

/*** The following variables are needed for initialization of the STM32-HAL System ***/

/* USER CODE END Includes */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc;
DMA_HandleTypeDef hdma_adc;

RTC_HandleTypeDef hrtc;

UART_HandleTypeDef huart1;

osThreadId defaultTaskHandle;

/* USER CODE BEGIN PV */
/* Private variables ---------------------------------------------------------*/
PAGEError = 0;
uint8_t initstart = 0;  /*** only needed in factory production  ***/

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_ADC_Init(void);
static void MX_RTC_Init(void);
static void MX_USART1_UART_Init(void);
void StartDefaultTask(void const * argument);
static void MX_NVIC_Init(void);

/* USER CODE BEGIN PFP */
/* Private function prototypes -----------------------------------------------*/

extern void vUARTCommandConsoleStart( void );


/* USER CODE END PFP */

/* USER CODE BEGIN 0 */

/*** Initialization of the STM32-HAL RTC Driver ***/

RTC_DateTypeDef  sdatestructure;
RTC_TimeTypeDef  stimestructure;

/*** Here are defined the warning messages which are sent through the serial interface ***/

uint8_t shutdownMessage[] = "xxxShutdownRaspberryPixxx\n\r";

uint8_t powerfailMessage[] = "xxx--StromPiPowerfail--xxx\n\r";

uint8_t powerBackMessage[] = "xxx--StromPiPowerBack--xxx\n\r";


/*** FreeRTOS Hook for Debug-Purposes ***/

void vApplicationStackOverflowHook(xTaskHandle *pxTask, signed char *pcTaskName )
{
	for( ;; );
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  *
  * @retval None
  */
int main(void)
{
  /* USER CODE BEGIN 1 */


  /*** The configuration, which is made in the serial console,
   * are stored into the flash of the STM32F031 MCU with the flashconfig() function.
   * In the following section, the configuration is read out from the designated flash
   * and stored into variables in the memory ***/

  modus =  *(uint8_t *)modus_FlashAdress;
  alarmDate = *(uint8_t *)alarmDate_FlashAdress;
  alarmWeekDay = *(uint8_t *)alarmWeekDay_FlashAdress;
  alarmTime = *(uint8_t *)alarmTime_FlashAdress;
  alarmPoweroff = *(uint8_t *)alarmPoweroff_FlashAdress;
  alarm_min = *(uint8_t *)alarm_min_FlashAdress;
  alarm_hour = *(uint8_t *)alarm_hour_FlashAdress;
  alarm_min_off = *(uint8_t *)alarm_min_off_FlashAdress;
  alarm_hour_off = *(uint8_t *)alarm_hour_off_FlashAdress;
  alarm_day = *(uint8_t *)alarm_day_FlashAdress;
  alarm_month = *(uint8_t *)alarm_month_FlashAdress;
  alarm_weekday = *(uint8_t *)alarm_weekday_FlashAdress;
  alarm_enable = *(uint8_t *)alarm_enable_FlashAdress;
  shutdown_enable = *(uint8_t *)shutdown_enable_FlashAdress;
  shutdown_time = *(uint8_t *)shutdown_time_FlashAdress;
  warning_enable=  *(uint8_t *)warning_enable_FlashAdress;
  poweroff_flag = 0;


  /* USER CODE END 1 */

  /* MCU Configuration----------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_RTC_Init();

  /* Initialize interrupts */
  MX_NVIC_Init();
  /* USER CODE BEGIN 2 */

  /*** Only for manufacturing | Checks if the Flash Area of the STM32F031 is blank - in this case it preprogrmm it with a default configuration ***/
  initialCheck();



/*********************************************************************************/

  /*** STM32HAL RTC-Driver Initialization ***/
  sdatestructure.Year = 0x18;
  sdatestructure.Month = RTC_MONTH_MAY;
  sdatestructure.Date = 0x01;
  sdatestructure.WeekDay = RTC_WEEKDAY_TUESDAY;

  if(HAL_RTC_SetDate(&hrtc,&sdatestructure,RTC_FORMAT_BCD) != HAL_OK)
  {
    /* Initialization Error */
    Error_Handler();
  }

  stimestructure.Hours = 0x00;
  stimestructure.Minutes = 0x00;
  stimestructure.Seconds = 0x00;
  stimestructure.TimeFormat = RTC_HOURFORMAT12_AM;
  stimestructure.DayLightSaving = RTC_DAYLIGHTSAVING_NONE ;
  stimestructure.StoreOperation = RTC_STOREOPERATION_RESET;

  if(HAL_RTC_SetTime(&hrtc,&stimestructure,RTC_FORMAT_BCD) != HAL_OK)
  {
    /* Initialization Error */
    Error_Handler();
  }

/*********************************************************************************/

  /*** Activates Powerpath of the configured primary source ***/
  /*
   * The Mode number represents the following configurations
   *
   *  1: mUSB (primary) -> Wide (secondary)
   *  2: Wide (primary) -> mUSB (secondary)
   *  3: mUSB (primary) -> Battery (secondary)
   *  4: Wide (primary) -> Battery (secondary)
   *
   *  So for the initial boot process the primary source is selected
   */

  if (modus == 1 || modus == 3)
  {
	  Power_USB();
  }
  else if (modus == 2 || modus == 4)
  {
	  Power_Wide();
  }

/*********************************************************************************/
/*
 * In the next lines the FreeRTOS Main Task is created and the Scheduler starts
 */
/*********************************************************************************/

  /* USER CODE END 2 */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* Create the thread(s) */
  /* definition and creation of defaultTask */
  osThreadDef(defaultTask, StartDefaultTask, osPriorityNormal, 0, 64);
  defaultTaskHandle = osThreadCreate(osThread(defaultTask), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */

  /* USER CODE END RTOS_THREADS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */

  /* USER CODE END RTOS_QUEUES */
 

  /* Start scheduler */
  osKernelStart();
  
  /* We should never get here as control is now taken by the scheduler */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {

  /* USER CODE END WHILE */

  /* USER CODE BEGIN 3 */

  }
  /* USER CODE END 3 */

}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{

  RCC_OscInitTypeDef RCC_OscInitStruct;
  RCC_ClkInitTypeDef RCC_ClkInitStruct;
  RCC_PeriphCLKInitTypeDef PeriphClkInit;

    /**Initializes the CPU, AHB and APB busses clocks 
    */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI14|RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSI14State = RCC_HSI14_ON;
  RCC_OscInitStruct.HSI14CalibrationValue = 16;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL6;
  RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Initializes the CPU, AHB and APB busses clocks 
    */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART1|RCC_PERIPHCLK_RTC;
  PeriphClkInit.Usart1ClockSelection = RCC_USART1CLKSOURCE_PCLK1;
  PeriphClkInit.RTCClockSelection = RCC_RTCCLKSOURCE_HSE_DIV32;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure the Systick interrupt time 
    */
  HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);

    /**Configure the Systick 
    */
  HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);

  /* SysTick_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(SysTick_IRQn, 3, 0);
}

/**
  * @brief NVIC Configuration.
  * @retval None
  */
static void MX_NVIC_Init(void)
{
  /* ADC1_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(ADC1_IRQn, 3, 0);
  HAL_NVIC_EnableIRQ(ADC1_IRQn);
  /* USART1_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(USART1_IRQn, 3, 0);
  HAL_NVIC_EnableIRQ(USART1_IRQn);
  /* DMA1_Channel1_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Channel1_IRQn, 3, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel1_IRQn);
}

/* ADC init function */
static void MX_ADC_Init(void)
{

  ADC_ChannelConfTypeDef sConfig;
  ADC_AnalogWDGConfTypeDef AnalogWDGConfig;

    /**Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion) 
    */
  hadc.Instance = ADC1;
  hadc.Init.ClockPrescaler = ADC_CLOCK_ASYNC_DIV1;
  hadc.Init.Resolution = ADC_RESOLUTION_12B;
  hadc.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc.Init.ScanConvMode = ADC_SCAN_DIRECTION_FORWARD;
  hadc.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  hadc.Init.LowPowerAutoWait = DISABLE;
  hadc.Init.LowPowerAutoPowerOff = DISABLE;
  hadc.Init.ContinuousConvMode = ENABLE;
  hadc.Init.DiscontinuousConvMode = DISABLE;
  hadc.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc.Init.DMAContinuousRequests = ENABLE;
  hadc.Init.Overrun = ADC_OVR_DATA_OVERWRITTEN;
  if (HAL_ADC_Init(&hadc) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure for the selected ADC regular channel to be converted. 
    */
  sConfig.Channel = ADC_CHANNEL_5;
  sConfig.Rank = ADC_RANK_CHANNEL_NUMBER;
  sConfig.SamplingTime = ADC_SAMPLETIME_239CYCLES_5;
  if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure for the selected ADC regular channel to be converted. 
    */
  sConfig.Channel = ADC_CHANNEL_6;
  if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure for the selected ADC regular channel to be converted. 
    */
  sConfig.Channel = ADC_CHANNEL_7;
  if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure for the selected ADC regular channel to be converted. 
    */
  sConfig.Channel = ADC_CHANNEL_9;
  if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure for the selected ADC regular channel to be converted. 
    */
  sConfig.Channel = ADC_CHANNEL_VREFINT;
  if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure the analog watchdog 
    */
  AnalogWDGConfig.WatchdogMode = ADC_ANALOGWATCHDOG_SINGLE_REG;
  AnalogWDGConfig.Channel = ADC_CHANNEL_7;
  AnalogWDGConfig.ITMode = ENABLE;
  AnalogWDGConfig.HighThreshold = 4095;
  AnalogWDGConfig.LowThreshold = 1850;
  if (HAL_ADC_AnalogWDGConfig(&hadc, &AnalogWDGConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

/* RTC init function */
static void MX_RTC_Init(void)
{

    /**Initialize RTC Only 
    */
  hrtc.Instance = RTC;
  hrtc.Init.HourFormat = RTC_HOURFORMAT_24;
  hrtc.Init.AsynchPrediv = 124;
  hrtc.Init.SynchPrediv = 1999;
  hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;
  hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;
  hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;
  if (HAL_RTC_Init(&hrtc) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

/* USART1 init function */
static void MX_USART1_UART_Init(void)
{

  huart1.Instance = USART1;
  huart1.Init.BaudRate = 38400;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  huart1.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart1.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

/** 
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void) 
{
  /* DMA controller clock enable */
  __HAL_RCC_DMA1_CLK_ENABLE();

}

/** Configure pins as 
        * Analog 
        * Input 
        * Output
        * EVENT_OUT
        * EXTI
*/
static void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct;

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, CTRL_VUSB_Pin|RESET_Rasp_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, CTRL_VREG5_Pin|BOOST_EN_Pin|CTRL_L7987_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin : CTRL_VUSB_Pin */
  GPIO_InitStruct.Pin = CTRL_VUSB_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(CTRL_VUSB_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : CTRL_VREG5_Pin BOOST_EN_Pin CTRL_L7987_Pin */
  GPIO_InitStruct.Pin = CTRL_VREG5_Pin|BOOST_EN_Pin|CTRL_L7987_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : RESET_Rasp_Pin */
  GPIO_InitStruct.Pin = RESET_Rasp_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(RESET_Rasp_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */

/*********************************************************************************/
/*
 * Functions to change the PowerPath
 *
 *
 * 		- Power_Wide() activates the PowerPath of the WideRange StepDownConverter
 * 		- Power_USB() activates the PowerPath of the mUSB Input
 * 		- Power_Bat() deactivates the charging circuit and activates the PowerPath of the Battery
 * 		- Power_Off() deactivates all Powerpathes so the Raspberry Pi turns off completely
 */

void Power_Wide(void)
{
	HAL_GPIO_WritePin(CTRL_VREG5_GPIO_Port,CTRL_VREG5_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(BOOST_EN_GPIO_Port,BOOST_EN_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(CTRL_VUSB_GPIO_Port,CTRL_VUSB_Pin,GPIO_PIN_RESET);
}

void Power_USB(void)
{
	HAL_GPIO_WritePin(CTRL_VUSB_GPIO_Port,CTRL_VUSB_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(CTRL_VREG5_GPIO_Port,CTRL_VREG5_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(BOOST_EN_GPIO_Port,BOOST_EN_Pin,GPIO_PIN_SET);
}

void Power_Bat(void)
{
	HAL_GPIO_WritePin(BOOST_EN_GPIO_Port,BOOST_EN_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(CTRL_VREG5_GPIO_Port,CTRL_VREG5_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(CTRL_VUSB_GPIO_Port,CTRL_VUSB_Pin,GPIO_PIN_RESET);
}

void Power_Off(void)
{
	HAL_GPIO_WritePin(CTRL_VREG5_GPIO_Port,CTRL_VREG5_Pin,GPIO_PIN_RESET);
	HAL_GPIO_WritePin(BOOST_EN_GPIO_Port,BOOST_EN_Pin,GPIO_PIN_SET);
	HAL_GPIO_WritePin(CTRL_VUSB_GPIO_Port,CTRL_VUSB_Pin,GPIO_PIN_RESET);
}

/*********************************************************************************/

/*** Functions to output the warning message, when the state of the StromPi3 have changes
 *
 * 		- ShutdownRPi() sends the warning to shutdown the Raspberry Pi when the primary voltage source fails
 * 		- PowerBack() sends a message when the primary voltage source comes back
 * 		- PowerfailWarning() sends the warning when the primary voltage source fails but its message doesn't shutdown the RPi
 * 																							  ***/
void ShutdownRPi(void)
{
	HAL_UART_Transmit(&huart1, (uint8_t *)shutdownMessage, sizeof(shutdownMessage), sizeof(shutdownMessage));
}

void PowerBack(void)
{
	HAL_UART_Transmit(&huart1, (uint8_t *)powerBackMessage, sizeof(powerBackMessage), sizeof(powerBackMessage));
}

void PowerfailWarning(void)
{
	HAL_UART_Transmit(&huart1, (uint8_t *)powerfailMessage, sizeof(powerfailMessage), sizeof(powerfailMessage));
	vTaskDelay(1 * 1000);
}

/*********************************************************************************/

/*** Functions to configure the ADC-Watchdog.
 * The STM32 can monitor the configured ADC-Voltageinput and switches to the HAL_ADC_LevelOutOfWindowCallback
 * when the voltage drops under the configured "AnalogWDGConfig.LowThreshold"
 *
 * 		- configureAWD_USB() is used when mUSB (mode 1 or 3) is configured as the primary input
 * 		- configureAWD_Wide() is used when Wide (mode 2 or 4) is configured as the primary input
 * 																							  ***/

void configureAWD_USB(void)
{
	ADC_AnalogWDGConfTypeDef AnalogWDGConfig;

    /**Configure the analog watchdog
    */
  AnalogWDGConfig.WatchdogMode = ADC_ANALOGWATCHDOG_SINGLE_REG;
  AnalogWDGConfig.Channel = ADC_CHANNEL_7;
  AnalogWDGConfig.ITMode = ENABLE;
  AnalogWDGConfig.HighThreshold = 4095;
  AnalogWDGConfig.LowThreshold = minUSB;
  if (HAL_ADC_AnalogWDGConfig(&hadc, &AnalogWDGConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

void configureAWD_Wide(void)
{
	ADC_AnalogWDGConfTypeDef AnalogWDGConfig;

    /**Configure the analog watchdog
    */
  AnalogWDGConfig.WatchdogMode = ADC_ANALOGWATCHDOG_SINGLE_REG;
  AnalogWDGConfig.Channel = ADC_CHANNEL_5;
  AnalogWDGConfig.ITMode = ENABLE;
  AnalogWDGConfig.HighThreshold = 4095;
  AnalogWDGConfig.LowThreshold = minWide;
  if (HAL_ADC_AnalogWDGConfig(&hadc, &AnalogWDGConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

/*********************************************************************************/

/*********************************************************************************/

/*** ADC Watchdog Interrupt
 *
 * When the Voltage drops under the configured Low Threshold, then the STM32 start the following
 * Callback function. The main Purpose is to switch as fast as possible to the backup voltage source
 * and then turn on the adequate flags for warning message processing or for starting the shutdown timer.
 *
 * 																							  ***/



void HAL_ADC_LevelOutOfWindowCallback(ADC_HandleTypeDef* hadc)
{
	__disable_irq();


	/*** Here the StromPi3 switches the PowerPath depended which mode is configured
    *
    *  1: mUSB (primary) -> Wide (secondary)
    *  2: Wide (primary) -> mUSB (secondary)
    *  3: mUSB (primary) -> Battery (secondary)
    *  4: Wide (primary) -> Battery (secondary)
    *
    *  The "warning_enable" flag is for the feature to make a powerfail warning without turning on the shutdowntimer
    *  and without shuting down the Raspberry Pi with the warning message through the serial interface.
    *
	 *   ***/

	if (modus == 1)
	{
		Power_Wide();
		if(warning_enable == 1)
		{
			warning_flag = 1;
		}
	}
	else if (modus == 2)
	{
		Power_USB();
		if(warning_enable == 1)
		{
			warning_flag = 1;
		}
	}
	else if (modus == 3 || modus == 4)
	{
		Power_Bat();
		powerBat_flag = 1;
		if(warning_enable == 1)
		{
			warning_flag = 1;
		}
	}


	/*** If the Shutdown-Timer is configured, then the shutdown_flag is activated here
	 * so the shutdown-timer can be started and the shutdown message for the raspberry pi can be sent through the serial interface ***/
	if (shutdown_enable == 1)
	{
		shutdown_flag = 1;
	}

	/*** This line deactivates the ADC Watchdog
	 * Its main purpose is to make sure to register a powerfailure probably once
	 * and that the ADC Watchdog Callback wouldn't be retriggered before the powerfailure
	 * processing in the main task have finished ***/
	__HAL_ADC_DISABLE_IT(hadc, ADC_IT_AWD);
	__enable_irq();
}

/*********************************************************************************/

/*** ADC Watchdog Interrupt
 *
 * flashConfig() is used for storing all of the configuration values to the flash
 * of the STM32F031 MCU, so it can be retrieved after a shutdown.
 *
 * flashValue() is a help function which is using the STM32-HAL for this matter.
 *
 * 																			  ***/



void flashConfig(void)
{
	FLASH_EraseInitTypeDef EraseInitStruct;

	HAL_FLASH_Unlock();
	EraseInitStruct.TypeErase   = FLASH_TYPEERASE_PAGES;
	EraseInitStruct.PageAddress = 0x8007C00;
	EraseInitStruct.NbPages     = 1;


	 if (HAL_FLASHEx_Erase(&EraseInitStruct, &PAGEError) != HAL_OK)
	  {
	    /*
	      Error occurred while page erase.
	      User can add here some code to deal with this error.
	      PAGEError will contain the faulty page and then to know the code error on this page,
	      user can call function 'HAL_FLASH_GetError()'
	    */
	    /* Infinite loop */
	    while (1)
	    {
	    	_Error_Handler(__FILE__, __LINE__);
	    }
	  }

	  flashValue(modus_FlashAdress,modus);
	  flashValue(alarmDate_FlashAdress,alarmDate);
	  flashValue(alarmWeekDay_FlashAdress,alarmWeekDay);
	  flashValue(alarmTime_FlashAdress,alarmTime);
	  flashValue(alarmPoweroff_FlashAdress,alarmPoweroff);
	  flashValue(alarm_min_FlashAdress,alarm_min);
	  flashValue(alarm_hour_FlashAdress,alarm_hour);
	  flashValue(alarm_min_off_FlashAdress,alarm_min_off);
	  flashValue(alarm_hour_off_FlashAdress,alarm_hour_off);
	  flashValue(alarm_day_FlashAdress,alarm_day);
	  flashValue(alarm_month_FlashAdress,alarm_month);
	  flashValue(alarm_weekday_FlashAdress,alarm_weekday);
	  flashValue(alarm_enable_FlashAdress,alarm_enable);
	  flashValue(shutdown_enable_FlashAdress,shutdown_enable);
	  flashValue(shutdown_time_FlashAdress,shutdown_time);
	  flashValue(warning_enable_FlashAdress,warning_enable);

	HAL_FLASH_Lock();

}

void flashValue(uint32_t address, uint32_t data)
{
	 if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, address , data) != HAL_OK)
	  {
	    /*
	      Error occurred while page erase.
	      User can add here some code to deal with this error.
	      PAGEError will contain the faulty page and then to know the code error on this page,
	      user can call function 'HAL_FLASH_GetError()'
	    */
	    /* Infinite loop */
	    while (1)
	    {
	    	_Error_Handler(__FILE__, __LINE__);
	    }
	  }
}

/*********************************************************************************/

/*********************************************************************************/

/*** Alarm_Handler
 *
 * This function is the main part of the time based sheduling system of the StromPi3
 * It is called every minute in the main Task and is checking if one
 * of the preprogrammed events is triggered - in this case the StromPi3 restarts the
 * RPi through switch the poweroff_flag to 0.
 * As for this the StromPi3 have to be in hi "shutdown-state" (poweroff_flag=1), which can be
 * achieved through the preprogrammed alarmPoweroff
 * or through a manual shutdown through the serial console.
 *  *
 * An event can be
 *
 * - alarmTime: the event triggers every time the preprogrammed clock time have been reached
 * - alarmWeekDay: the event triggers every time the preprogrammed weekday have been reached (for example every monday)
 * - alarmDate: the event triggers every time the preprogrammed date have been reached (for example every first march of the year)
 *
 *
 * 																			  ***/

void Alarm_Handler(void)
{
	RTC_TimeTypeDef stimestructureget;
	RTC_DateTypeDef sdatestructureget;

	HAL_RTC_GetTime(&hrtc, &stimestructureget, RTC_FORMAT_BIN);
	HAL_RTC_GetDate(&hrtc, &sdatestructureget, RTC_FORMAT_BIN);

 /*** This part handles the preprogrammed shutdown function  ***/
	if(alarmPoweroff == 1)
	{
		if (alarm_min_off == stimestructureget.Minutes
				&& alarm_hour_off == stimestructureget.Hours) {
			    poweroff_flag = 1;
				ShutdownRPi();
		}
	}


	if(alarm_enable == 1)
	{
		if(alarmTime == 1)
		{
			if (alarm_min == stimestructureget.Minutes && alarm_hour == stimestructureget.Hours)
				{
					poweroff_flag = 0;
				}
			}
		else if(alarmWeekDay == 1)
		{
			if ( alarm_min == stimestructureget.Minutes && alarm_hour == stimestructureget.Hours && alarm_weekday == sdatestructureget.WeekDay)
			{
				  if (modus == 1 || modus == 3)
				  {
					  if (rawValue[2] > minUSB)
					  {
						  poweroff_flag = 0;
						  Power_USB();
					  }
					  else if (modus == 1)
					  {
						  poweroff_flag = 0;
						  Power_Wide();
					  }
					  else if (modus == 3)
					  {
						  poweroff_flag = 0;
						  Power_Bat();
						  powerBat_flag = 1;
					  }
				  }

				  else if (modus == 2 || modus == 4)
				  {
					  if (rawValue[0] > minWide)
					  {
						  poweroff_flag = 0;
						  Power_Wide();
					  }
					  else if (modus == 2)
					  {
						  poweroff_flag = 0;
						  Power_USB();
					  }
					  else if (modus == 4)
					  {
						  poweroff_flag = 0;
						  Power_Bat();
						  powerBat_flag = 1;
					  }
				  }
			}
		}

		else if(alarmDate == 1)
		{
			if ( alarm_min == stimestructureget.Minutes && alarm_hour == stimestructureget.Hours && alarm_day == sdatestructureget.Date && alarm_month == sdatestructureget.Month)
			{
				  if (modus == 1 || modus == 3)
				  {
					  if (rawValue[2] > minUSB)
					  {
						  poweroff_flag = 0;
						  Power_USB();
					  }
					  else if (modus == 1)
					  {
						  poweroff_flag = 0;
						  Power_Wide();
					  }
					  else if (modus == 3)
					  {
						  poweroff_flag = 0;
						  Power_Bat();
						  powerBat_flag = 1;
					  }
				  }

				  else if (modus == 2 || modus == 4)
				  {
					  if (rawValue[0] > minWide)
					  {
						  poweroff_flag = 0;
						  Power_Wide();
					  }
					  else if (modus == 2)
					  {
						  poweroff_flag = 0;
						  Power_USB();
					  }
					  else if (modus == 4)
					  {
						  poweroff_flag = 0;
						  Power_Bat();
						  powerBat_flag = 1;
					  }
				  }
			}
		}
	}
}

/*********************************************************************************/

/*** Only for manufacturing | Checks if the Flash Area of the STM32F031 is blank, so it preprogrmm it with a default configuration ***/

void initialCheck(void)
{
	  if (modus == 0xFF)
	  {
		  modus = 1;
		  alarmDate = 0;
		  alarmWeekDay = 0;
		  alarmTime = 1;
		  alarmPoweroff = 0;
		  alarm_min = 0;
		  alarm_hour = 0;
		  alarm_min_off = 0;
		  alarm_hour_off = 0;
		  alarm_day = 1;
		  alarm_month = 1;
		  alarm_weekday = 1;
		  alarm_enable = 0;
		  shutdown_enable = 0;
		  shutdown_time = 10;
		  warning_enable = 1;

		  flashConfig();
	  }
}

/*********************************************************************************/

/*** Main Task
 *
 * The next section describes the main Task.
 * In the first part (before the main loop) the initial starting condition is prepared
 * and the UART serial console task is initiated.
 *
 * The main loop then is triggered every second by the FreeRTOS Taskscheduler
 * As this give a synchroned timesource, the main task is counting the seconds and after reaching
 * a full minute, its starts the Alarm_Handler()
 *
 * The next part is for the processing of the warning messages, as it would be to critical to
 * resolve them in the ADC Watchdog Interrupt, and for turning the primary PowerPath back on
 * after the ADC have detected that it came back to life.
 *
 * The last part os for reading out the ADC and storing the values into variables for processing.



/* USER CODE END 4 */

/* StartDefaultTask function */
void StartDefaultTask(void const * argument)
{

  /* USER CODE BEGIN 5 */
  uint16_t VDDValue;
  uint8_t sek = 0;

  /*** Initialization ***/

  if (initstart == 0)
  {
	  osDelay(500);
	  MX_ADC_Init();

	  if (modus == 1 || modus == 3)
	  {
		  Power_USB();
		  configureAWD_USB();
	  }
	  else if (modus == 2 || modus == 4)
	  {
		  Power_Wide();
		  configureAWD_Wide();
	  }

	  HAL_ADCEx_Calibration_Start(&hadc);

	  if (HAL_ADC_Start_DMA(&hadc, (uint32_t*)rawValue, 5) != HAL_OK)
		{
		  return 0;
		}

	  osDelay(5000);
	  MX_USART1_UART_Init();


	  /*** Serial Console Task Initialization ***/
	  vUARTCommandConsoleStart();
  }


  for(;;)
  {

	  /*** Counts for a full minute and calls then the Alarm_Handler() ***/

	  if (sek == 60)
	  {
		  Alarm_Handler();
		  sek=0;
	  }
	  sek++;


	  /*** If one of the Events have triggered the shutdown-timer,
	   * then it here cuts off the Power to the Raspberry Pi  ***/
      if (shutdown_time_counter > 0)
	  {
		  shutdown_time_counter--;

		  if (shutdown_time_counter == 0)
		  {
			  Power_Off();
		  }
	  }


      /*** Processing of the shutdown_flag
       * The Counter for the shutdown-timer is set
       * and the warning message for the Raspberry Pi Shutdown
       * is sent out through the serial interface  ***/

	  if (shutdown_enable == 1 && shutdown_flag == 1)
	  {
		  shutdown_time_counter = shutdown_time;
		  ShutdownRPi();
		  shutdown_flag = 0;
		  powerback_flag = 1;
	  }

      /*** Processing of the warning_flag
       * If the shutdown-timer is deactivated, but the
       * warning feature is enabled, then here the powerfail-warning
       * is generated
       */

	  if (warning_enable == 1 && warning_flag == 1 && shutdown_enable != 1)
	  	  {
		  	  PowerfailWarning();
	  		  warning_flag = 0;
	  		  powerback_flag = 1;
	  	  }


      /*** Turns the Raspberry Pi PowerPath backs on if the primary Voltage source has came back to life
       * Also the ADC-Watchdog-Interrupt is turned back on, so it can trigger once again.
       * The transition of the primary voltage source to the backup source, is monitored and will be
       * switched in the most critical manner (as soon as possible: directly in the ADC-Watchdog Interrupt),
       * but the transition from the backup source to the primary voltage is triggered here in the main Task
       * in its "1-second" period of time.
       */

	  if (modus == 1 || modus== 3)
	  {
		  if (rawValue[2] > minUSB && poweroff_flag !=1)
		  		{
		  			Power_USB();
		  			__HAL_ADC_CLEAR_FLAG(&hadc, ADC_FLAG_AWD);
		  			__HAL_ADC_ENABLE_IT(&hadc, ADC_IT_AWD);
		  			shutdown_time_counter = 0;
		  			powerBat_flag = 0;

		  			if (powerback_flag == 1)
		  			{
		  				PowerBack();
		  				powerback_flag = 0;
		  			}
		  		}
	  }

	  if (modus == 2 || modus== 4)
	  {
		  if (rawValue[0] > minWide && poweroff_flag !=1)
		  		{
		  			Power_Wide();
		  			__HAL_ADC_CLEAR_FLAG(&hadc, ADC_FLAG_AWD);
		  			__HAL_ADC_ENABLE_IT(&hadc, ADC_IT_AWD);
		  			shutdown_time_counter = 0;
		  			powerBat_flag = 0;

		  			if (powerback_flag == 1)
		  			{
		  				PowerBack();
		  				powerback_flag = 0;
		  			}
		  		}

	  }


      /*** Reads out the current ADC-Values and stores them into the linked variables ***/
	  HAL_ADCEx_Calibration_Start(&hadc);
	  VDDValue = 3300*(*((unsigned short*)0x1FFFF7BA)) / rawValue[4];
	  measuredValue[0] = VDDValue*rawValue[0]/4095*105100/5100;
	  measuredValue[1] = VDDValue*rawValue[1]/4095*15100/5100;
	  measuredValue[2] = VDDValue*rawValue[2]/4095*15100/5100;
	  measuredValue[3] = VDDValue*rawValue[3]/4095*15100/5100;


	  /*** A small protection function for the Battery.  ***/
	  if (measuredValue[3] < minBat && powerBat_flag == 1 )
	  		  		{
	  		  			Power_Off();
	  		  		}

    osDelay(1000);
  }
  /* USER CODE END 5 */ 
}

/**
  * @brief  Period elapsed callback in non blocking mode
  * @note   This function is called  when TIM14 interrupt took place, inside
  * HAL_TIM_IRQHandler(). It makes a direct call to HAL_IncTick() to increment
  * a global variable "uwTick" used as application time base.
  * @param  htim : TIM handle
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* USER CODE BEGIN Callback 0 */

  /* USER CODE END Callback 0 */
  if (htim->Instance == TIM14) {
    HAL_IncTick();
  }
  /* USER CODE BEGIN Callback 1 */

  /* USER CODE END Callback 1 */
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @param  file: The file name as string.
  * @param  line: The line in file as a number.
  * @retval None
  */
void _Error_Handler(char *file, int line)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  while(1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t* file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/**
  * @}
  */

/**
  * @}
  */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
