from gpiozero import CPUTemperature, PWMLED
from time import sleep

led = PWMLED(2)	# PWM-Pin (GPIO2)

startTemp = 55	# Temperature at which the fan switches on

pTemp = 4		# Proportional part
iTemp = 0.2		# Integral part

fanSpeed = 0	# Fan speed
sum = 0			# variable for i part


while True:		# Control loop
	cpu = CPUTemperature()		# Reading the current temperature values
	actTemp = cpu.temperature		# Current temperature as float variable

	diff = actTemp - startTemp
	sum = sum + diff
	pDiff = diff * pTemp
	iDiff = sum * iTemp
	fanSpeed = pDiff + iDiff + 35
 

	if fanSpeed > 100:
		fanSpeed = 100
	elif fanSpeed < 35:
		fanSpeed = 0
	
	if sum > 100:
		sum = 100
	elif sum < -100:
		sum = -100
	
	#print(str(actTemp) + "C, " + str(fanSpeed))
	
	led.value = fanSpeed / 100	# PWM Output

	sleep(1)
