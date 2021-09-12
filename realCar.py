in training delete the first image since it takes time to connect]
#ps -fA | grep python


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
GPIO.setmode(GPIO.BCM) #only needed for servo
#Basic convenience
GPIO.setwarnings(False)

######################################################################################################################################################
# Set up Servo
control = 17 # Control pin for servo
GPIO.setup(control, GPIO.OUT) # setup control pin as a output
servo = GPIO.PWM(control, 50) # create PWM instance of servo that sends out signals at 50 hertz
servo.start(0) # start servo motor
right = 7
left = 10
######################################################################################################################################################



######################################################################################################################################################
#setup pin numbers for DC motor
drive = driver.Driver()
######################################################################################################################################################
# Set up variables that will be used later
held = "NA"
two = 0
######################################################################################################################################################
# define dictionary for control logging
lognum = 1
df = [] # create a list with the first entry being the starting conditions in dictionary
collect = 1
######################################################################################################################################################
cap = cv2.VideoCapture(0) #set up video object
ret, frame = cap.read() #read frame
images_folder = "/home/pi/Desktop/pictures/" #set picture directory
colab_filename = "/content/pictures/"

def mapping(x, in_min, in_max, out_min, out_max):
    return ((x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min)
time.sleep(1)
print("Waiting 1 second ...")
######################################################################################################################################################
# main code that handles xbox inputs, motor control, servo control, logging data
def main(counter):
    global two, lognum, df, collect, cap
    input_time = -1 # Used with to log data every second(see end of main())
    control_dict = { # dictionary for logging data after initial set up
    "imgfile": "filename",
    "whichRun": counter,
    "lognum":0,
    "turn":0,
    "forward": 0,
    "backward":0,
    "stopped" : 1
    }
    add = 1
    try:
        with ControllerResource() as joystick: # When xbox is connected, create a instance of the xbox with alias 'joystick'
            print("Connected")
            while joystick.connected:  # run while xbox is connected to RPi
                #servo.ChangeDutyCycle(0) 
                #time.sleep(0.01)  # try to stabalize servo wheel jitter
                
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
                    print('forward')
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
                angle = mapping(x, -50, 50, left, right)
                if x > -5 and x < 5:
                    servo.ChangeDutyCycle(9)
                else:
                    servo.ChangeDutyCycle(angle)
                control_dict['turn'] = angle

                
                held = "" # clear the previous entry from keyboard to not get stuck
                ret, frame = cap.read()
                #cv2.imshow('img', frame)
                #cv2.waitKey(1)
                frameId = cap.get(1)
                filename = images_folder + "trial_"+ str(counter) + "_image_id:" + str(lognum-2) + ".jpg"
                colab_file = colab_filename + "trial_"+ str(counter) + "_image_id:" + str(lognum-2) + ".jpg"
                control_dict["imgfile"] = colab_file
                if add % 11 == 0:
                    control_dict["lognum"] = lognum
                    lognum += 1
                    cv2.imwrite(filename, frame)
                    df.append(control_dict.copy()) # add the control_dict dictionary with user inputs into df list
                    print(control_dict.copy())
                    #while time.localtime(time.time()).tm_sec == 59:#If time reaches 59, reset input_time to make it keep running
                     #   input_time = 65
                add += 1
                print(-x)
                time.sleep(0.001)
                                             
                
                
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
#    t.start()
    collect = 0
    main(1)



