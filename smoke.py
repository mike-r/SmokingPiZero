#!/usr/bin/env python
#/home/pi/temp/smoke.py

#    SMOKING Pi Zero   Version: 1.0

# Python program to read level guage in smoke oil tank and display to an ePaper
# display from Papirus.

# Input is from an Automation hat. 0-4 volts.

# Recalibrated voltage to level reading.
# Added a deadband for level change before updating display.


import automationhat
import time

time.sleep(10.0)  # Wait for the pi to finish booting.

from papirus import PapirusTextPos

time.sleep(0.1)  # short pause after ads1015 class creation

text = PapirusTextPos(False)


text.Clear()
time.sleep(1.0)
text.AddText("N221TM", 10 ,0, 40, Id="Line-1")
text.AddText("SMOKE TANK", 0, 35, 30, Id="lINE-2")
text.AddText("_EMPTY_", 0, 60, 40, Id="Line-3")
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
    if value > 2.80: Level = "_FULL_"
    if value < 2.81: Level = " 3/4"
    if value < 1.30: Level = " 1/2"
    if value < 0.91: Level = " 1/4"
    if value < 0.30: Level = "-EMPTY-"
    print (Level)
    text.UpdateText("Line-3", Level)
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

