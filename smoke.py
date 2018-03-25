#!/usr/bin/env python
#/home/pi/temp/smoke.py

#    SMOKING Pi Zero   Version: 1.1

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

import automationhat
import time

time.sleep(7.0)  # Wait for the pi to finish booting.

from papirus import PapirusTextPos

time.sleep(0.1)  # short pause after ads1015 class creation

text = PapirusTextPos(False)


text.Clear()
time.sleep(1.0)
text.AddText("N221TM", 10 ,0, 40, Id="Line-1")
text.AddText("SMOKE TANK", 0, 35, 30, Id="lINE-2")
text.AddText("BOOTING", 0, 60, 40, Id="Line-3")
text.WriteAll()
time.sleep(2.0)

while True:
    
    value= automationhat.analog.one.read()
    print(value)
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
    if value > 1.50: Level = "_FULL_"
    if value < 1.20: Level = " 3/4"
    if value < 0.80: Level = " 1/2"
    if value < 0.40: Level = " 1/4"
    if value < 0.20: Level = "-EMPTY-"
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
    
    while change < 0.08:
        time.sleep(1.0)         # Sit here if input isn't changing
        print("level not changing")
        newValue = automationhat.analog.one.read()
        change = abs(newValue - value)
        if automationhat.input.two.read(): break   # Quit when input-2 goes high
        if automationhat.input.three.read(): break # Smoke is ON
    print("change ", change)
    time.sleep(1.0)
    
exit()

