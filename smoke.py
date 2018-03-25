#!/usr/bin/env python
#/home/pi/temp/smoke.py

#    SMOKING Pi Zero    Version: 0.00

# Python program to read level guage in smoke oil tank and display to an ePaper
# display from Papirus.

# Input is from an Automation hat. 0-4 volts.


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
text.AddText("EMPTY", 20, 60, 40, Id="Line-3")
text.WriteAll()
time.sleep(2.0)

while True:
    
    value= automationhat.analog.one.read()
#    print(value)
    Level2 = "{:.3f}".format(value)
#    print(Level2)
    if value < 4.0: Level = "1/2"
    if value < 2.0: Level = "1/4"
    if value < 1.0: Level = "EMPTY"
    if value > 4.0: Level = "FULL"
#    print (Level)
    text.UpdateText("Line-3", Level2)
    input2 = automationhat.input.two.read()
#    print(input2)
    text.WriteAll()
    if automationhat.input.two.read():  # Quit when input-2 goes high
        break
    time.sleep(5.0)

exit()

