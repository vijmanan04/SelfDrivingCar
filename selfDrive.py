#in training delete the first image since it takes time to connect]
#ps -fA | grep python


######################################################################################################################################################
#import all libraries needed
import cv2 # used to capture video
import RPi.GPIO as GPIO # used to control motors and servo
import time # used for multiple reasons(motors, servo, camera, etc...)
from approxeng.input.selectbinder import ControllerResource # import library from approximate engineering for xbox controller sync with RPi
import driver
import numpy as np
from tensorflow.keras.models import load_model
######################################################################################################################################################
#set up numbering for GPIO Pins
GPIO.setmode(GPIO.BCM) #only needed for servo
#Basic convenience
GPIO.setwarnings(False)

######################################################################################################################################################
# Set up Servo
control = 17 # Control pin for servo
GPIO.setup(control, GPIO.OUT) # setup control pin as a output
servo = GPIO.PWM(control, 50) # create PWM instance of servo that sends out signals at 50 hertz
servo.start(0) # start servo motor
######################################################################################################################################################



######################################################################################################################################################
#setup pin numbers for DC motor
drive = driver.Driver()
######################################################################################################################################################
######################################################################################################################################################
model = load_model('/home/pi/Desktop/model.h5')
######################################################################################################################################################
cap = cv2.VideoCapture(0) #set up video object
######################################################################################################################################################
# main code that handles xbox inputs, motor control, servo control, logging data
def main(counter):
    y = 200
    h = 230
    x = 0
    w = 640
    drive.right()
    while 1:
        ret, frame = cap.read() #read frame
        frame = np.asarrary(frame)
        frame = frame[y:y+h, x:x+w] #crop images
        frame = cv2.GaussianBlur(img, (3, 3), 0))
        frame = cv2.resize(frame, (66, 198))
        frame = np.array([frame])
        angle = float(model.predict(frame))
        servo.ChangeDutyCycle(angle)
        time.sleep(0.5)
        
    


