import RPi.GPIO as GPIO
import time

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO pins to use on the Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# Set up the GPIO pins
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def measure_distance():
    # Ensure the trigger pin is set low
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.5)

    # Send a 10us pulse to start the measurement
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = start_time

    # Save the start time
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Save the arrival time
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Calculate distance
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Divide by 2 for return journey

    return distance

try:
    while True:
        dist = measure_distance()
        print("Measured Distance = %.1f cm" % dist)
        time.sleep(1)  # Delay between measurements

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
