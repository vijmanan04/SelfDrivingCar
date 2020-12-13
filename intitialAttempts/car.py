#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from time import sleep

#Basic convenience
GPIO.setwarnings(0)


#set up numbering for points
GPIO.setmode(GPIO.BCM)

#setup pin numbers
in1 = 24
in2 = 25
enA = 23

#Set up all pins as output pins
def setup():
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(enA, GPIO.OUT)

#setup PWM Cycle
#pCycle = p.(enA, 1000)
    
#Stop function   #not Off function
def stop():
    setup()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(enA, GPIO.LOW)
    

#Forward function
def forward():
    setup()
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    time.sleep(1)
    stop()

#Backward function
def backward():
    setup()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    time.sleep(1)
    stop()

#User Interface + command prompt
def UI():
    while(1):
        ui = input()
        while (ui == "w"):
            print("FORWARD")
            forward()
            UI()
        while (ui == "s"):
            print("BACKWARD")
            backward()
            UI()
        
        else:
            print("INVALID INPUT... ENTER AGAIN")
            GPIO.cleanup()
            exit()
UI()
