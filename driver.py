import RPi.GPIO as GPIO


class Driver:
    def __init__(self):
        GPIO.setmode(GPIO.BCM) #set up BCM board numbering
        self.R_EN = 24
        self.L_EN = 23
        self.RPWM = 25
        self.LPWM = 18
        GPIO.setup(self.R_EN, GPIO.OUT) # setup all pins as GPIO
        GPIO.setup(self.RPWM, GPIO.OUT)
        GPIO.setup(self.L_EN, GPIO.OUT)
        GPIO.setup(self.LPWM, GPIO.OUT)
        
        self.rightmotorPWM = GPIO.PWM(self.RPWM, 100) #set up PWM
        self.leftmotorPWM = GPIO.PWM(self.LPWM, 100)
        self.leftmotorPWM.start(0) # start PWM
        self.rightmotorPWM.start(0)

        
        GPIO.output(self.R_EN, False) #make starting condition for motor off
        GPIO.output(self.L_EN, False)


    def neutral(self):
        self.rightmotorPWM.ChangeDutyCycle(0) # turn off dutycycle
        self.leftmotorPWM.ChangeDutyCycle(0)
        
        GPIO.output(self.R_EN, True)
        GPIO.output(self.L_EN, True)
        GPIO.output(self.RPWM, False)  # Stop turning right
        GPIO.output(self.LPWM, False)  # stop turning left

    def right(self):
        self.rightmotorPWM.ChangeDutyCycle(50) #run at 50% duty cycle
        GPIO.output(self.R_EN, True)
        GPIO.output(self.L_EN, True)
        GPIO.output(self.LPWM, False)  # stop turning left
        GPIO.output(self.RPWM, True)  # start turning right

    def left(self):
        self.leftmotorPWM.ChangeDutyCycle(50) #run at 50% duty cycle
        GPIO.output(self.R_EN, True)
        GPIO.output(self.L_EN, True)
        GPIO.output(self.RPWM, False)  # Stop turning right
        GPIO.output(self.LPWM, True)  # start turning left

    def cleanup(self):
        GPIO.cleanup() # cleanup GPIO

