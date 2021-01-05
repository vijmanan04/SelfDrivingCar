#in training delete the first image since it takes time to connect




import threading
import cv2
import RPi.GPIO as GPIO
import time
from time import sleep
from approxeng.input.selectbinder import ControllerResource
import vid_to_pic


#set up numbering for points
GPIO.setmode(GPIO.BCM)

control = 17
GPIO.setup(control, GPIO.OUT)
servo = GPIO.PWM(control, 50)
#Get Joystick
#Basic convenience
GPIO.setwarnings(False)


#setup pin numbers for DC motor
in1 = 24
in2 = 25
enA = 23
held = "nothing"
servo.start(0)
start_count = 0
def setup():
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(enA, GPIO.OUT)
state = 1
vid_to_pic_state = 0

control_dict_first ={
    "time":0,
    "left": 0,
    "right": 0,
    "straight":1,
    "forward": 0,
    "backward":0,
    "stopped" : 1
}
df = [control_dict_first]
not_now = 0
def main():
    input_time = -1
    global state
    try:
        with ControllerResource() as joystick:
            print("Connected")
            while joystick.connected:
                control_dict ={
                    "time":0,
                    "left": 0,
                    "right": 0,
                    "straight":1,
                    "forward": 0,
                    "backward":0,
                    "stopped" : 1
                }
                servo.ChangeDutyCycle(0)
                time.sleep(0.05)
                x, y = joystick['l']
                held = joystick.check_presses()
                x = x * 100
                y = y * 100
                if held['cross']:
                    GPIO.cleanup()
                    print(df)
                    state = 0
                    exit()
                if held['dup']:
                    setup()
                    GPIO.output(in1, GPIO.LOW)
                    GPIO.output(in2, GPIO.HIGH)
                    GPIO.output(enA, GPIO.HIGH)
                    control_dict["backward"] = 0
                    control_dict["stopped"] = 0
                    control_dict["forward"] = 1
                if held['ddown']:
                    setup()
                    GPIO.output(in1, GPIO.HIGH)
                    GPIO.output(in2, GPIO.LOW)
                    GPIO.output(enA, GPIO.HIGH)
                    control_dict["backward"] = 1
                    control_dict["stopped"] = 0
                    control_dict["forward"] = 0
                if held == "nothing" or held["l1"]:
                    setup()
                    GPIO.output(in1, GPIO.LOW)
                    GPIO.output(in2, GPIO.HIGH)
                    GPIO.output(enA, GPIO.LOW)
                    control_dict["backward"] = 0
                    control_dict["stopped"] = 1
                    control_dict["forward"] = 0
                if x > 10:
                    servo.ChangeDutyCycle(8)
                    time.sleep(0.09)
                    servo.ChangeDutyCycle(0)
                    control_dict["right"] = 1
                    control_dict["left"] = 0
                    control_dict["straight"] = 0
                if x < -10:
                    servo.ChangeDutyCycle(10.5)
                    time.sleep(0.09)
                    servo.ChangeDutyCycle(0)
                    control_dict["right"] = 0
                    control_dict["left"] = 1
                    control_dict["straight"] = 0
                if x > -10 and x < 10:
                    servo.ChangeDutyCycle(9)
                    time.sleep(0.09)
                    servo.ChangeDutyCycle(0)
                    control_dict["right"] = 0
                    control_dict["left"] = 0
                    control_dict["straight"] = 1
                held = ""
                if input_time < time.localtime(time.time()).tm_sec:
                    control_dict["time"] = [time.localtime(time.time()).tm_mon, time.localtime(time.time()).tm_mday, time.localtime(time.time()).tm_year, time.localtime(time.time()).tm_hour, time.localtime(time.time()).tm_min, time.localtime(time.time()).tm_sec]
                    #print(time.localtime(time.time()).tm_sec)
                    df.append(control_dict)
                    print(control_dict)
                    input_time = time.localtime(time.time()).tm_sec
                    if input_time == 59:
                        input_time = 0
                    
                
        #Disconnected
        print("Joystick disconnected")
    except IOError:
        state = 0
        print("No joystick found")
        exit()

thread = threading.Thread(target = main)
thread.daemon = 1
thread.start()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    result = cv2.VideoWriter('stream2.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, size)
    while 1 and state != 0:
        sucess, img = cap.read()
        if sucess == 1:
            #cv2.imshow('Video Stream', img)
            result.write(img)
            cv2.waitKey(1)
    if vid_to_pic_state == 0 and not_now == 0:
        cap.release()
        result.release()
        vid_to_pic.vid_to_pic('stream2.avi')

