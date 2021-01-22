#in training delete the first image since it takes time to connect


######################################################################################################################################################
#import all libraries needed
import cv2 # used to capture video
import RPi.GPIO as GPIO # used to control motors and servo
import time # used for multiple reasons(motors, servo, camera, etc...)
from approxeng.input.selectbinder import ControllerResource # import library from approximate engineering for xbox controller sync with RPi
import datetime #for image file number
import driver
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
#load driver functions
drive = driver.Driver()
######################################################################################################################################################
# Set up variables that will be used later
held = "NA"
two = 0
######################################################################################################################################################
# define dictionary for control logging
lognum = 1
df = [] # create a list with the first entry being the starting conditions in dictionary 
######################################################################################################################################################
cap = cv2.VideoCapture(0) #set up video object
ret, frame = cap.read() #read frame
images_folder = "/home/pi/Desktop/pictures/" #set picture directory
######################################################################################################################################################
# main code that handles xbox inputs, motor control, servo control, logging data
def main(counter):
    global two, lognum, df
    input_time = -1 # Used with to log data every second(see end of main())
    control_dict = { # dictionary for logging data after initial set up
    "imgfile": "filename",
    "whichRun": counter,
    "lognum":0,
    "left": 0,
    "right": 0,
    "straight":1,
    "forward": 0,
    "backward":0,
    "stopped" : 1
    }
    try:
        with ControllerResource() as joystick: # When xbox is connected, create a instance of the xbox with alias 'joystick'
            print("Connected")
            while joystick.connected:  # run while xbox is connected to RPi
                servo.ChangeDutyCycle(0) 
                time.sleep(0.05)  # try to stabalize servo wheel jitter
                
                x, y = joystick['l'] # get x and y coordinates from left joystick on xbox
                held = joystick.check_presses() # check for xbox controller presses 
                x = x * 100. # augment data since x coordinates are very small
                
                if held['cross']: # 'cross' = 'a' on xbox, if a pressed, cleanup motors, print the dictionary df with logged data, change state to 0, and exit thread
                    GPIO.cleanup()
                    df.pop(0)
                    df.pop(0)
                    df = df[:-1]
                    return df #returns 3 less than the amount of data collected
                if held['dup']: # 'dup' = d-pad up on xbox,
                    drive.right()
                    control_dict["backward"] = 0 # change dictionary values respectively 
                    control_dict["stopped"] = 0
                    control_dict["forward"] = 1
                if held['ddown']:
                    drive.left()
                    control_dict["backward"] = 1 # change dictionary values respectively
                    control_dict["stopped"] = 0
                    control_dict["forward"] = 0
                if held == "NA" or held["l1"]: # run this block when xbox first connects or 'l1' (aka Y on xbox) is pressed
                    drive.neutral()
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
                #cv2.imshow('img', frame)
                #cv2.waitKey(1)
                if input_time == 65:
                    input_time = -1

                if input_time < time.localtime(time.time()).tm_sec: #ad hoc method to log data every second
                    control_dict["lognum"] = lognum
                    lognum += 1
                    input_time = time.localtime(time.time()).tm_sec #change input time to make it current time, which will be less than the time in the next second, causing this if statment to run again
                    frameId = cap.get(1)
                    filename = images_folder + "trial_"+ str(counter) + "_image_id:" + str(lognum-2) + ".jpg"
                    control_dict["imgfile"] = filename
                    if two <= 2:
                        two += 1
                        continue
                    cv2.imwrite(filename, frame)
                    df.append(control_dict.copy()) # add the control_dict dictionary with user inputs into df list
                    print(control_dict.copy())
                    while time.localtime(time.time()).tm_sec == 59:#If time reaches 59, reset input_time to make it keep running
                        input_time = 65

                            
                
                
        #Disconnected
        print("Joystick disconnected") # When xbox disconnects, print this
    except IOError: #Run when xbox does not connect
        state = 0 # Keep state 0 to make the video part not run since xbox never connected
        print("No joystick found")
        exit()
######################################################################################################################################################

######################################################################################################################################################

######################################################################################################################################################

if __name__ == "__main__":
    main(1)

