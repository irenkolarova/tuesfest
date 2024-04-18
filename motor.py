import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for motor control
motor1A = 23
motor1B = 24
motor2A = 25
motor2B = 16
motor3A = 17
motor3B = 27
motor4A = 17  # Reusing GPIO 17 for sensor 2 trigger
motor4B = 22  # Reusing GPIO 22 for sensor 2 echo

# Set up GPIO pins as outputs
GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)
GPIO.setup(motor3A, GPIO.OUT)
GPIO.setup(motor3B, GPIO.OUT)
GPIO.setup(motor4A, GPIO.OUT)
GPIO.setup(motor4B, GPIO.OUT)

# Function to control motor direction
def set_motor_speed(motor, speed):
    if speed > 0:
        GPIO.output(motor[0], GPIO.HIGH)
        GPIO.output(motor[1], GPIO.LOW)
    elif speed < 0:
        GPIO.output(motor[0], GPIO.LOW)
        GPIO.output(motor[1], GPIO.HIGH)
    else:
        GPIO.output(motor[0], GPIO.LOW)
        GPIO.output(motor[1], GPIO.LOW)

# Function to stop all motors
def stop_all_motors():
    GPIO.output(motor1A, GPIO.LOW)
    GPIO.output(motor1B, GPIO.LOW)
    GPIO.output(motor2A, GPIO.LOW)
    GPIO.output(motor2B, GPIO.LOW)
    GPIO.output(motor3A, GPIO.LOW)
    GPIO.output(motor3B, GPIO.LOW)
    GPIO.output(motor4A, GPIO.LOW)
    GPIO.output(motor4B, GPIO.LOW)

# Test motor control
try:
    while True:
        direction = input("Enter direction (l - left, r - right, b - backwards, f - forwards, s - stop): ")
        if direction == 'l':
            set_motor_speed((motor1A, motor1B), 50)  # Motor 1 forwards
            set_motor_speed((motor2A, motor2B), -50) # Motor 2 backwards
            set_motor_speed((motor3A, motor3B), 50)  # Motor 3 forwards
            set_motor_speed((motor4A, motor4B), -50) # Motor 4 backwards
        elif direction == 'r':
            set_motor_speed((motor1A, motor1B), -50) # Motor 1 backwards
            set_motor_speed((motor2A, motor2B), 50)  # Motor 2 forwards
            set_motor_speed((motor3A, motor3B), -50) # Motor 3 backwards
            set_motor_speed((motor4A, motor4B), 50)  # Motor 4 forwards
        elif direction == 'b':
            set_motor_speed((motor1A, motor1B), -50) # Motor 1 backwards
            set_motor_speed((motor2A, motor2B), -50) # Motor 2 backwards
            set_motor_speed((motor3A, motor3B), -50) # Motor 3 backwards
            set_motor_speed((motor4A, motor4B), -50) # Motor 4 backwards
        elif direction == 'f':
            set_motor_speed((motor1A, motor1B), 50)  # Motor 1 forwards
            set_motor_speed((motor2A, motor2B), 50)  # Motor 2 forwards
            set_motor_speed((motor3A, motor3B), 0)  # Motor 3 forwards
            set_motor_speed((motor4A, motor4B), 0)  # Motor 4 forwards
        elif direction == 's':
            stop_all_motors()
        else:
            print("Invalid direction. Please enter l, r, b, f, or s.")
            continue
except KeyboardInterrupt:
    GPIO.cleanup()
import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for motor control
motor1A = 23
motor1B = 24
motor2A = 25
motor2B = 16
motor3A = 17
motor3B = 27
motor4A = 17  # Reusing GPIO 17 for sensor 2 trigger
motor4B = 22  # Reusing GPIO 22 for sensor 2 echo

# Set up GPIO pins as outputs
GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)
GPIO.setup(motor3A, GPIO.OUT)
GPIO.setup(motor3B, GPIO.OUT)
GPIO.setup(motor4A, GPIO.OUT)
GPIO.setup(motor4B, GPIO.OUT)

# Function to control motor direction
def set_motor_speed(motor, speed):
    if speed > 0:
        GPIO.output(motor[0], GPIO.HIGH)
        GPIO.output(motor[1], GPIO.LOW)
    elif speed < 0:
        GPIO.output(motor[0], GPIO.LOW)
        GPIO.output(motor[1], GPIO.HIGH)
    else:
        GPIO.output(motor[0], GPIO.LOW)
        GPIO.output(motor[1], GPIO.LOW)

# Function to stop all motors
def stop_all_motors():
    GPIO.output(motor1A, GPIO.LOW)
    GPIO.output(motor1B, GPIO.LOW)
    GPIO.output(motor2A, GPIO.LOW)
    GPIO.output(motor2B, GPIO.LOW)
    GPIO.output(motor3A, GPIO.LOW)
    GPIO.output(motor3B, GPIO.LOW)
    GPIO.output(motor4A, GPIO.LOW)
    GPIO.output(motor4B, GPIO.LOW)

# Test motor control
try:
    while True:
        direction = input("Enter direction (l - left, r - right, b - backwards, f - forwards, --s - stop): ")
        if direction == 'l':
            set_motor_speed((motor1A, motor1B), 50)  # Motor 1 forwards
            set_motor_speed((motor2A, motor2B), -50) # Motor 2 backwards
            set_motor_speed((motor3A, motor3B), 50)  # Motor 3 forwards
            set_motor_speed((motor4A, motor4B), -50) # Motor 4 backwards
        elif direction == 'r':
            set_motor_speed((motor1A, motor1B), -50) # Motor 1 backwards
            set_motor_speed((motor2A, motor2B), 50)  # Motor 2 forwards
            set_motor_speed((motor3A, motor3B), -50) # Motor 3 backwards
            set_motor_speed((motor4A, motor4B), 50)  # Motor 4 forwards
        elif direction == 'b':
            set_motor_speed((motor1A, motor1B), -50) # Motor 1 backwards
            set_motor_speed((motor2A, motor2B), -50) # Motor 2 backwards
            set_motor_speed((motor3A, motor3B), -50) # Motor 3 backwards
            set_motor_speed((motor4A, motor4B), -50) # Motor 4 backwards
        elif direction == 'f':
            set_motor_speed((motor1A, motor1B), 50)  # Motor 1 forwards
            set_motor_speed((motor2A, motor2B), 50)  # Motor 2 forwards
            set_motor_speed((motor3A, motor3B), 50)  # Motor 3 forwards
            set_motor_speed((motor4A, motor4B), 0)  # Motor 4 forwards
        elif direction == 's':
            stop_all_motors()
            continue
        else:
            print("Invalid direction. Please enter l, r, b, f, or --s.")
            continue
        
        time.sleep(2) # Change this value as needed for the duration of movement
        stop_all_motors()
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()



