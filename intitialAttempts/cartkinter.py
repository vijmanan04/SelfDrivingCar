#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from time import sleep
import tkinter

#Basic convenience
GPIO.setwarnings(0)


#set up numbering for points
GPIO.setmode(GPIO.BCM)

#setup pin numbers for DC motor
in1 = 24
in2 = 25
enA = 23

#setup pin numbers for servo motor
control = 17

#setup PWM clock, range, Rpi base frequency is 19.2MHz and set output to 50Hz for SG90 servo
#OutputHz = 19.2 MHz / clock / range
#Defaults: Clock = 1500MHz
#Use formula to calculate range: 3906.25 HZ
#For sg90 servo, pulse duration is 1-2 ms --> 1.5 duty cycle givees angle of 90(Half way between 0 and 180)

#Set up all pins as output pins
def setup():
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(enA, GPIO.OUT)
    GPIO.setup(control, GPIO.OUT)
    servo = GPIO.PWM(control, 50) #initializes servo to send out 50Hz
    servo.start(0) #starts servo at 0 pulse(not the same as 0 duty cycle, but just means that servo is not moving)

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
    servo.ChangeDutyCycle(6) #change to face forward
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    time.sleep(0.5)
    stop()

#Backward function
def backward():
    servo.ChangeDutyCycle(6) #change to face forward
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    time.sleep(0.5)
    stop()


#servo range is from 2 to 12 percent duty cycle(2 = 0 degrees, 12 = 180 degrees)
def right():
    servo.ChangeDutyCycle(12)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def left():
    servo.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)


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
    if event.char.lower() == 'd':
        right()
    if event.char.lower() == 'a':
        left()

ui = tk.Tk()

def intake():
    ui.bind('<KeyPress>', system) #binds system function with <KeyPress> (from tkinter)
ui.after(1000, command = intake)
ui.mainloop()
