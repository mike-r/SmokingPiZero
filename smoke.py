#!/usr/bin/env python
#/home/pi/temp/smoke.py

#					SMOKING Pi Zero   Version: 2.3.2

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



print("Hi from Smoke.py")

import automationhat
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

### time.sleep(7.0)  # Papirus needs to wait for the pi to finish booting.
from papirus import PapirusTextPos


# 128x32 OLED display with hardware I2C:
##disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize OLED Display library.
##disp.begin()

# Clear OLED display.
##disp.clear()
##disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
##width = disp.width
##height = disp.height
##image = Image.new('1', (width, height))

# Get drawing object to draw on image.
##draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
##draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
##bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
font = ImageFont.truetype('/home/pi/temp/upheavtt.ttf' , 30)


time.sleep(0.1)  # short pause after ads1015 class creation

text = PapirusTextPos(False)

text.Clear()
time.sleep(1.0)
text.AddText("N221TM", 10 ,0, 40, Id="Line-1")
text.AddText("SMOKE TANK", 0, 35, 30, Id="lINE-2")
text.AddText("BOOTING", 0, 60, 40, Id="Line-3")
text.WriteAll()

# Draw a black filled box to clear the image.
##draw.rectangle((0,0,width,height), outline=0, fill=0)

#	cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
#	CPU = subprocess.check_output(cmd, shell = True )

OLED = "  N221TM"

# Write two lines of text.

##draw.text((x, top+4),	str(OLED), font=font, fill=255)

# OLED Display image.
##disp.image(image)
##disp.display()
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
		OLED = "@@@@@@"
# Draw a black filled box to clear the image.
##		draw.rectangle((0,0,width,height), outline=0, fill=0)
##		draw.text((x, top+4),     str(OLED), font=font, fill=255)
##		disp.image(image)	
##		disp.display()
		while automationhat.input.three.read():     # Snmoke ON, so Wait
			time.sleep(1)
		text.UpdateText("Line-3", "<-OFF->")        # Smoke OFF
		text.WriteAll()
		OLED = "<-OFF->"
# Draw a black filled box to clear the image.
##		draw.rectangle((0,0,width,height), outline=0, fill=0)
##		draw.text((x, top+4),     str(OLED), font=font, fill=255)
##		disp.image(image)
##		disp.display()
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
# Draw a black filled box to clear the image.
##	draw.rectangle((0,0,width,height), outline=0, fill=0)
##	draw.text((x, top+4),     str(gallonsF), font=font, fill=255)
##	disp.image(image)
##	disp.display()
	
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
