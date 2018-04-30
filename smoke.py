#!/usr/bin/env python
#/home/pi/temp/smoke.py

#					SMOKING Pi Zero   Version: 2.3.ePaper.1

# Python program to read level guage in smoke oil tank and display to an ePaper
# display from Papirus.

# To run at boot add the following to the END of /etc/rc.local

#			sudo python /home/pi/temp/smoke.py &



# Input is from an Automation hat. 0-4 volts.


# V 1.0
# Recalibrated voltage to level reading.
# Added a deadband for level change before updating display.

# V 1.1
# Recalibrated again.
# Reduced sleep time.
# Changed booting text.

# V 2.0
# Added debug printing to counsel.
# Added Adafruit 128x32 OLED display (ePaper display broke).
# Calculate Gallons from voltage and display that.

# V 2.1
# Fixed weird identing.  ie. converted spaces to TABs.

# V 2.2
# Recalibration at .5 gallon marks really done in V 2.2 not 2.1

# V 2.3   (3/25/2018}
# Fixed syntax errors.

# V 2.3.1 (3/27)
# Version without OLED display.
# V 2.3.2 found more "disp.", ".draw", and "height" lines to comment out.

# V2.3.ePaper.1
# updated version standard



print("PaPiRus ePaper Smoke.py")
print(" V 2.3.ePaper.1 without OLED")

import automationhat
import time
import Adafruit_GPIO.SPI as SPI
###import Adafruit_SSD1306

###from PIL import Image
###from PIL import ImageDraw
###from PIL import ImageFont

import subprocess

 time.sleep(7.0)  # Papirus needs to wait for the pi to finish booting.
from papirus import PapirusTextPos




text = PapirusTextPos(False)

text.Clear()
time.sleep(1.0)
text.AddText("N221TM", 10 ,0, 40, Id="Line-1")
text.AddText("SMOKE TANK", 0, 35, 30, Id="lINE-2")
text.AddText("BOOTING", 0, 60, 40, Id="Line-3")
text.WriteAll()

time.sleep(2.0)


while True:
	
	value = automationhat.analog.one.read()
	print(value)
	gallons = (value - 0.216)/0.630
	if value   > 3.84: gallons = 5.5
	elif value > 3.30: gallons = 5.0
	elif value > 3.03: gallons = 4.5
	elif value > 2.74: gallons = 4.0
	elif value > 2.33: gallons = 3.5
	elif value > 1.90: gallons = 3.0
	elif value > 1.57: gallons = 2.5
	elif value > 1.24: gallons = 2.0
	elif value > 0.70: gallons = 1.5
	elif value > 0.25: gallons = 1.0
	elif value > 0.22: gallons = 0.5
	
	print(gallons)
	gallonsF = "{:.1f}".format(gallons)
	gallonsF = gallonsF + " Gallons"
	print(gallonsF)
	Level2 = "{:.2f}".format(value)
	print(Level2)
	Level3 = Level2 + " V"
	print (Level3)
	
	if automationhat.input.three.read():        # Smoke is ON
		text.UpdateText("Line-3", "<@@@@@>")
		text.WriteAll()
		while automationhat.input.three.read():     # Snmoke ON, so Wait
			time.sleep(1)
		text.UpdateText("Line-3", "<-OFF->")        # Smoke OFF
		text.WriteAll()
		time.sleep(2.0)
	if value > 3.20: Level = "-FULL-"
	if value < 3.21: Level = " 3/4"
	if value < 2.30: Level = " 1/2"
	if value < 1.40: Level = " 1/4"
	if value < 0.30: Level = "-EMPTY-"
	
##	if value > 3.20: gallonsF = "--FULL--"
	if value < 0.22: gallonsF = "-EMPTY-"
	
	print (Level)
	text.UpdateText("Line-3", Level)
	text.UpdateText("Line-1", Level3)
	text.WriteAll()
	
	input2 = automationhat.input.two.read()
	print("Input2=", input2)
	
	if automationhat.input.two.read(): break # Quit when input-2 goes high
	
	newValue = automationhat.analog.one.read()
	change = abs(newValue - value)
	print("change ", change)
	
	while change < 0.05:
		time.sleep(1.0)         # Sit here if input isn't changing
		print("level not changing")
		newValue = automationhat.analog.one.read()
		change = abs(newValue - value)
		if automationhat.input.two.read(): break   # Quit when input-2 goes high
		if automationhat.input.three.read(): break # Smoke is ON
	print("change ", change)
	time.sleep(0.01)
	
exit()
