#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from time import sleep
import tkinter

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
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    time.sleep(1)
    GPIO.cleanup()

#Backward function
def backward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    time.sleep(1)
    GPIO.cleanup()

#User Interface + command prompt
def system(event):     #event is an in built tkinter object
    setup()
    print ('Key: ', event.char) #event.char is an attribute for event that returns single-character strings
    if event.char.lower() == 'w':
        forward()
    if event.char.lower() == 's':
        backward()
    if event.char.lower() == 'q':
        exit()

ui = tk.TK()
ui.bind('<KeyPress>', system) #binds system function with <KeyPress> (from tkinter)
ui.mainloop()
