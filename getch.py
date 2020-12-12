#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from time import sleep
import getch as g

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

#set up servo control pin. This one must be a global variable of 'servo' because it must be used within multiple functions.
# GPIO.setup must come before servo initialization to setup correct pin
GPIO.setup(control, GPIO.OUT)
servo = GPIO.PWM(control, 50) #initializes servo to send out 50Hz

ts = 0.2 #set timer for sleep function
#Set up all pins as output pins for DC Motor
def setup():
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(enA, GPIO.OUT)
    servo.start(0) #starts servo at 0 pulse(not the same as 0 duty cycle, but just means that servo is not moving)

#Stop function   #not Off function
def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(enA, GPIO.LOW)


#Forward function
def forward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    servo.ChangeDutyCycle(0)
    time.sleep(ts)
    stop()

#Backward function
def backward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    time.sleep(ts)
    stop()


#servo range is from 2 to 12 percent duty cycle(2 = 0 degrees, 12 = 180 degrees)
def right():
    servo.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def left():
    servo.ChangeDutyCycle(12)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
def fix():
    servo.ChangeDutyCycle(8.7)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)



#class
while 1:
    comm = g.getch()
    if comm == "w":
        forward()
    if comm == "s":
        backward()
    if comm == "d":
        right()
    if comm == "a":
        left()
    if comm == "p":
        fix()
    if comm == "q":
        exit()
    comm = "" #listens for next command and removes previous one
