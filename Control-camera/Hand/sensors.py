import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def measure_distance():
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.5)

    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)  # 10 ms
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = start_time

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

     while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2

    return distance

try:
    while True:
        dist = measure_distance()
        print("Measured Distance = %.1f cm" % dist)
        time.sleep(1) 
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
