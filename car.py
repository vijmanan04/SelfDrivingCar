#delay in camera has been accounted for
######################################################################################################################################################
#import all libraries needed
import cv2 # used to capture video
import RPi.GPIO as GPIO # used to control motors and servo
import time # used for multiple reasons(motors, servo, camera, etc...)
from approxeng.input.selectbinder import ControllerResource # import library from approximate engineering for xbox controller sync with RPi
import datetime #for image file number
######################################################################################################################################################
#set up numbering for GPIO Pins
GPIO.setmode(GPIO.BCM) 
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
in1 = 24 #define pin numbers for in1, in2, and enable for DROK motor controller
in2 = 25
enA = 23
def setup():  #define setup function for motors and set all pins as output pins
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(enA, GPIO.OUT)
######################################################################################################################################################
# Set up variables that will be used later
held = "NA"
two = 0
######################################################################################################################################################
# define dictionary for control logging 
control_dict_ex ={
    "time":0,
    "left": 0,
    "right": 0,
    "straight":1,
    "forward": 0,
    "backward":0,
    "stopped" : 1
}
df = [] # create a list with the first entry being the starting conditions in dictionary 
######################################################################################################################################################
cap = cv2.VideoCapture(0) #set up video object
ret, frame = cap.read() #read frame
images_folder = "/home/pi/Desktop/pictures" #set picture directory
######################################################################################################################################################
# main code that handles xbox inputs, motor control, servo control, logging data
def main():
    global two
    input_time = -1 # Used with to log data every second(see end of main())
    try:
        with ControllerResource() as joystick: # When xbox is connected, create a instance of the xbox with alias 'joystick'
            print("Connected")
            while joystick.connected:  # run while xbox is connected to RPi
                control_dict = { # dictionary for logging data after initial set up
                    "time":0,
                    "left": 0,
                    "right": 0,
                    "straight":1,
                    "forward": 0,
                    "backward":0,
                    "stopped" : 1
                }
                servo.ChangeDutyCycle(0) 
                time.sleep(0.05)  # try to stabalize servo wheel jitter
                
                x, y = joystick['l'] # get x and y coordinates from left joystick on xbox
                held = joystick.check_presses() # check for xbox controller presses 
                x = x * 100. # augment data since x coordinates are very small
                
                if held['cross']: # 'cross' = 'a' on xbox, if a pressed, cleanup motors, print the dictionary df with logged data, change state to 0, and exit thread
                    GPIO.cleanup()
                    df.pop(0)
                    df.pop(0)
                    print(df)
                    state = 0 # stop running camera
                    return df
                if held['dup']: # 'dup' = d-pad up on xbox, 
                    setup()
                    GPIO.output(in1, GPIO.LOW) #LOW, HIGH, HIGH turns motor forward
                    GPIO.output(in2, GPIO.HIGH)
                    GPIO.output(enA, GPIO.HIGH)
                    control_dict["backward"] = 0 # change dictionary values respectively 
                    control_dict["stopped"] = 0
                    control_dict["forward"] = 1
                if held['ddown']:
                    setup()
                    GPIO.output(in1, GPIO.HIGH) # HIGH, LOW, HIGH turns motor backward
                    GPIO.output(in2, GPIO.LOW)
                    GPIO.output(enA, GPIO.HIGH)
                    control_dict["backward"] = 1 # change dictionary values respectively
                    control_dict["stopped"] = 0
                    control_dict["forward"] = 0
                if held == "NA" or held["l1"]: # run this block when xbox first connects or 'l1' (aka Y on xbox) is pressed
                    setup()
                    GPIO.output(in1, GPIO.LOW) #LOW, LOW, LOW turns both outputs low and turns motor off
                    GPIO.output(in2, GPIO.LOW)
                    GPIO.output(enA, GPIO.LOW)
                    control_dict["backward"] = 0 # change dictionary values respectively
                    control_dict["stopped"] = 1
                    control_dict["forward"] = 0
                if x > 10:  # If joystick is right, turn servo right
                    servo.ChangeDutyCycle(8) #This value causes wheel to turn right
                    time.sleep(0.09)
                    servo.ChangeDutyCycle(0)
                    control_dict["right"] = 1 # change dictionary values respectively
                    control_dict["left"] = 0
                    control_dict["straight"] = 0
                if x < -10: #If joystick is left, turn servo left
                    servo.ChangeDutyCycle(10.5) #This values causes wheel to turn left
                    time.sleep(0.09)
                    servo.ChangeDutyCycle(0)
                    control_dict["right"] = 0 # change dictionary values respectively
                    control_dict["left"] = 1
                    control_dict["straight"] = 0
                if x > -10 and x < 10: #If joystick is not moving within a certain margin, turn wheels straight
                    servo.ChangeDutyCycle(9) #This values makes wheels straight
                    time.sleep(0.09)
                    servo.ChangeDutyCycle(0) 
                    control_dict["right"] = 0 # change dictionary values respectively
                    control_dict["left"] = 0
                    control_dict["straight"] = 1
                held = "" # clear the previous entry from keyboard to not get stuck
                ret, frame = cap.read()
                cv2.imshow('img', frame)
                cv2.waitKey(1)
                if input_time < time.localtime(time.time()).tm_sec: #ad hoc method to log data every second
                    control_dict["time"] = [time.localtime(time.time()).tm_mon, time.localtime(time.time()).tm_mday, time.localtime(time.time()).tm_year, time.localtime(time.time()).tm_hour, time.localtime(time.time()).tm_min, time.localtime(time.time()).tm_sec] #insert time into data frame
                    df.append(control_dict) # add the control_dict dictionary with user inputs into df list
                    print(control_dict)
                    input_time = time.localtime(time.time()).tm_sec #change input time to make it current time, which will be less than the time in the next second, causing this if statment to run again
                    if input_time == 59: #If time reaches 59, reset input_time to make it keep running
                        input_time = 0
                    img_time = datetime.datetime.fromtimestamp(time.time()).strftime('%H-%M-%S')
                    frameId = cap.get(1)
                    filename = images_folder + "/image_" + str(int(frameId)) + "_" + str(img_time) + ".jpg"
                    if two <= 2:
                        two += 1
                        continue
                    cv2.imwrite(filename, frame)
                    
                
        #Disconnected
        print("Joystick disconnected") # When xbox disconnects, print this
    except IOError: #Run when xbox does not connect
        state = 0 # Keep state 0 to make the video part not run since xbox never connected
        print("No joystick found")
        exit()
######################################################################################################################################################

######################################################################################################################################################

######################################################################################################################################################
main()


