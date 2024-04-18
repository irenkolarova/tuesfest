import RPi.GPIO as GPIO          
from time import sleep

in1 = 24
in2 = 23
en = 25
en2 = 17
in12 = 27
in22 = 22
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,100)

GPIO.setmode(GPIO.BCM)
GPIO.setup(in12,GPIO.OUT)
GPIO.setup(in22,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in12,GPIO.LOW)
GPIO.output(in22,GPIO.LOW)
p2=GPIO.PWM(en2,100)


p.start(25)
p2.start(25)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

while(1):

    x=str(input("Kur kaji kvo ti trqq: "))
    
    if x=='g':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in12,GPIO.HIGH)
         GPIO.output(in22,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in12,GPIO.LOW)
         GPIO.output(in22,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in12,GPIO.LOW)
        GPIO.output(in22,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in12,GPIO.HIGH)
        GPIO.output(in22,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in12,GPIO.LOW)
        GPIO.output(in22,GPIO.HIGH)
        temp1=0
        x='z'
 
    elif x=='l':
        print("left")
        GPIO.output(in12,GPIO.HIGH)
        GPIO.output(in22,GPIO.LOW)
        p2.ChangeDutyCycle(25)

        x='z'

    elif x=='r':
        print("medium")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)

        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(100)
        p2.ChangeDutyCycle(100)
        x='z'
                                       
    
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
