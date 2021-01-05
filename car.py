#in training delete the first image since it takes time to connect


######################################################################################################################################################
#import all libraries needed
import threading # will be used to accept xbox controls while recording 
import cv2 # used to capture video
import RPi.GPIO as GPIO # used to control motors and servo
import time # used for multiple reasons(motors, servo, camera, etc...)
from approxeng.input.selectbinder import ControllerResource # import library from approximate engineering for xbox controller sync with RPi
import vid_to_pic # Another file I made to convert video from car into pictures
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
start_count = 0
state = 1
vid_to_pic_state = 0 # don't run vid_to_pic right away
not_now = 0

######################################################################################################################################################
# define dictionary for control logging 
control_dict_first ={
    "time":0,
    "left": 0,
    "right": 0,
    "straight":1,
    "forward": 0,
    "backward":0,
    "stopped" : 1
}
df = [control_dict_first] # create a list with the first entry being the starting conditions in dictionary 
######################################################################################################################################################


######################################################################################################################################################
# main code that handles xbox inputs, motor control, servo control, logging data
def main():
    input_time = -1 # Used with to log data every second(see end of main())
    global state # define state as a global variable to be used between threads
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
                
                x, y = joystick['l']. # get x and y coordinates from left joystick on xbox
                held = joystick.check_presses() # check for xbox controller presses 
                x = x * 100. # augment data since x coordinates are very small
                
                if held['cross']: # 'cross' = 'a' on xbox, if a pressed, cleanup motors, print the dictionary df with logged data, change state to 0, and exit thread
                    GPIO.cleanup()
                    print(df)
                    state = 0 # stop running camera
                    exit()
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
                    servo.ChangeDutyCycle(8). #This value causes wheel to turn right
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
                
                if input_time < time.localtime(time.time()).tm_sec: #ad hoc method to log data every second
                    control_dict["time"] = [time.localtime(time.time()).tm_mon, time.localtime(time.time()).tm_mday, time.localtime(time.time()).tm_year, time.localtime(time.time()).tm_hour, time.localtime(time.time()).tm_min, time.localtime(time.time()).tm_sec] #insert time into data frame
                    df.append(control_dict) # add the control_dict dictionary with user inputs into df list
                    print(control_dict)
                    input_time = time.localtime(time.time()).tm_sec #change input time to make it current time, which will be less than the time in the next second, causing this if statment to run again
                    if input_time == 59: #If time reaches 59, reset input_time to make it keep running
                        input_time = 0
                    
                
        #Disconnected
        print("Joystick disconnected") # When xbox disconnects, print this
    except IOError: #Run when xbox does not connect
        state = 0 # Keep state 0 to make the video part not run since xbox never connected
        print("No joystick found")
        exit()
######################################################################################################################################################
thread = threading.Thread(target = main) # create a thread instance that will target the main function
thread.daemon = 1
thread.start() #start thread to accept user input
######################################################################################################################################################

######################################################################################################################################################
if __name__ == "__main__": #if the current program is called directly, run video
    cap = cv2.VideoCapture(0) # create OpenCV instance of a camera(using RPi camera)
    frame_width = int(cap.get(3)) # getting dimensions of frames
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    
    result = cv2.VideoWriter('stream2.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, size) #create an object into which to put data, 30 is fps, VideoWriter_fourcc is a way to compress the file
    while 1 and state != 0: # keep running while state is not 0
        sucess, img = cap.read()
        if sucess == 1:
            #cv2.imshow('Video Stream', img) --> use this to display data, but I will change this to a video stream over socket
            result.write(img) # write the video file 
            cv2.waitKey(1) 
    if vid_to_pic_state == 0 and not_now == 0: #once previous video is written to result, release it and feed it into vid_to_pic to convrert to pictures
        cap.release()
        result.release()
        vid_to_pic.vid_to_pic('stream2.avi')

