#!/usr/bin/env python
#/home/pi/temp/smoke.py

#    SMOKING Pi Zero   Version: 2.0

# Python program to read level guage in smoke oil tank and display to an ePaper
# display from Papirus.
		  
		

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

### time.sleep(7.0)  # Wait for the pi to finish booting.
from papirus import PapirusTextPos


# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
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
draw.rectangle((0,0,width,height), outline=0, fill=0)

#   cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
#   CPU = subprocess.check_output(cmd, shell = True )

OLED = "  N221TM"
	
# Write two lines of text.

draw.text((x, top+4),     str(OLED), font=font, fill=255)

# Display image.
disp.image(image)
disp.display()	
time.sleep(2.0)


while True:

    value = automationhat.analog.one.read()
    print(value)
    gallons = (value - 0.208)/0.738
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
 	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((x, top+4),     str(OLED), font=font, fill=255)
	disp.image(image)	
	disp.display()
        while automationhat.input.three.read():     # Snmoke ON, so Wait
 		time.sleep(1)
        text.UpdateText("Line-3", "<-OFF->")        # Smoke OFF
        text.WriteAll()
	OLED = "<-OFF->"
    # Draw a black filled box to clear the image.
 	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text((x, top+4),     str(OLED), font=font, fill=255)
	disp.image(image)
	disp.display()
        time.sleep(2.0)
    if value > 3.20: Level = "-FULL-"
    if value < 3.21: Level = " 3/4"
    if value < 2.30: Level = " 1/2"
    if value < 1.40: Level = " 1/4"
    if value < 0.30: Level = "-EMPTY-"
	
    if value > 3.20: gallonsF = "--FULL--"
    if value < 0.30: gallonsF = "-EMPTY-"
	
    print (Level)
    text.UpdateText("Line-3", Level)
    text.UpdateText("Line-1", Level3)
    text.WriteAll()
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top+4),     str(gallonsF), font=font, fill=255)
    disp.image(image)
    disp.display()

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
