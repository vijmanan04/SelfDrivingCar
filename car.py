#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

#set up numbering for points
GPIO.setmode(GPIO.BCM)

#setup pin numbers
in1 = 24
in2 = 25
enA = 23

#Set up all pins as output pins
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)

#setup PWM Cycle
#pCycle = p.(enA, 1000)

#Forward function
def forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.cleanup()

#Backward function
def backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.cleanup()

#User Interface + command prompt
def UI():
    while(1):
        ui = input()
        ui = str(ui)
        if (ui == "w"):
            print("FORWARD")
            forward()
        if (ui == "b"):
            print("BACKWARD")
            backward()
        else:
            print("INVALID INPUT... SHUTTING DOWN")
            GPIO.cleanup()
            break()
