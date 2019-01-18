/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
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

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H__
#define __MAIN_H__

/* Includes ------------------------------------------------------------------*/

/* USER CODE BEGIN Includes */
#include <stdint.h>
/* USER CODE END Includes */

/* Private define ------------------------------------------------------------*/

#define CTRL_VUSB_Pin GPIO_PIN_0
#define CTRL_VUSB_GPIO_Port GPIOA
#define CTRL_VREG5_Pin GPIO_PIN_1
#define CTRL_VREG5_GPIO_Port GPIOA
#define BOOST_EN_Pin GPIO_PIN_2
#define BOOST_EN_GPIO_Port GPIOA
#define RESET_Rasp_Pin GPIO_PIN_3
#define RESET_Rasp_GPIO_Port GPIOA
#define CTRL_L7987_Pin GPIO_PIN_4
#define CTRL_L7987_GPIO_Port GPIOA
#define ADC_WIDE_Pin GPIO_PIN_5
#define ADC_WIDE_GPIO_Port GPIOA
#define ADC_VBAT_Pin GPIO_PIN_6
#define ADC_VBAT_GPIO_Port GPIOA
#define ADC_VUSB_Pin GPIO_PIN_7
#define ADC_VUSB_GPIO_Port GPIOA
#define ADC_VOUT_Pin GPIO_PIN_1
#define ADC_VOUT_GPIO_Port GPIOB

/* ########################## Assert Selection ############################## */
/**
  * @brief Uncomment the line below to expanse the "assert_param" macro in the 
  *        HAL drivers code
  */
/* #define USE_FULL_ASSERT    1U */

/* USER CODE BEGIN Private defines */

//ADC Value Buffer
uint16_t rawValue[5];
uint16_t measuredValue[5];

void configureAWD_Wide(void);
void configureAWD_USB(void);

void Power_Wide(void);
void Power_USB(void);
void Power_Bat(void);
void Power_Off(void);
void ShutdownRPi(void);
void PowerfailWarning(void);
void PowerBack(void);
void Alarm_Handler(void);
void initialCheck(void);
void Config_Reset_Pin_Input(void);
void Config_Reset_Pin_Output(void);

#define minWide 300
#define minUSB  1800
#define minBatConnect  10
#define minBat 2550

uint8_t poweroff_flag;
uint8_t manual_poweroff_flag;

uint8_t power_on_button_counter;

uint8_t powerback_flag;
uint8_t powerBat_flag;

uint8_t warning_flag;

uint8_t modus;

uint8_t alarmDate;

uint8_t alarmWeekDay;

uint8_t alarmTime;

uint8_t alarmPoweroff;

uint8_t alarmInterval;

uint16_t alarmIntervalMinOn;

uint16_t alarmIntervalMinOff;

uint16_t alarmIntervalMinOn_Counter;

uint16_t alarmIntervalMinOff_Counter;


uint8_t alarm_enable;

uint8_t alarm_min;
uint8_t alarm_hour;

uint8_t alarm_min_off;
uint8_t alarm_hour_off;

uint8_t alarm_day;
uint8_t alarm_month;

uint8_t alarm_weekday;

uint8_t shutdown_flag;
uint8_t shutdown_time_counter;
uint8_t alarm_shutdown_time_counter;

uint16_t shutdown_time;
uint8_t shutdown_enable;

uint8_t alarm_shutdown_enable;

uint8_t serialLessMode;

uint8_t warning_enable;

uint8_t batLevel;
uint8_t batLevel_shutdown;
uint8_t batLevel_shutdown_flag;

uint8_t charging;

#define chargingOffset 90

#define modus_FlashAdress 0x8007C00
#define alarmDate_FlashAdress 0x8007C10
#define alarmWeekDay_FlashAdress 0x8007C20
#define alarmTime_FlashAdress 0x8007C30
#define alarmPoweroff_FlashAdress 0x8007C40
#define alarm_min_FlashAdress 0x8007C50
#define alarm_hour_FlashAdress 0x8007C60
#define alarm_min_off_FlashAdress 0x8007C70
#define alarm_hour_off_FlashAdress 0x8007C80
#define alarm_day_FlashAdress 0x8007C90
#define alarm_month_FlashAdress 0x8007CA0
#define alarm_weekday_FlashAdress 0x8007CB0
#define alarm_enable_FlashAdress 0x8007CC0
#define shutdown_enable_FlashAdress 0x8007CD0
#define shutdown_time_FlashAdress 0x8007CE0
#define warning_enable_FlashAdress 0x8007CF0
#define serialLessMode_FlashAdress 0x8007D00
#define batLevel_shutdown_FlashAdress 0x8007D10
#define alarmInterval_FlashAdress 0x8007D20
#define alarmIntervalMinOn_FlashAdress 0x8007D30
#define alarmIntervalMinOff_FlashAdress 0x8007D40

void flashConfig(void);
void flashValue(uint32_t address, uint32_t data);

/* USER CODE END Private defines */

#ifdef __cplusplus
 extern "C" {
#endif
void _Error_Handler(char *, int);

#define Error_Handler() _Error_Handler(__FILE__, __LINE__)
#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H__ */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
