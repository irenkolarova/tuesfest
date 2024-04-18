import RPi.GPIO as GPIO
import time
import os
import random

time.sleep(5)

GPIO.setmode(GPIO.BCM)

TRIG_PIN = 21
ECHO_PIN1 = 2
ECHO_PIN2 = 3

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN1, GPIO.IN)
GPIO.setup(ECHO_PIN2, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    start_time = time.time()
    while GPIO.input(ECHO_PIN1) == GPIO.LOW:
        if (time.time() - start_time) > 0.1:
            return -1
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN1) == GPIO.HIGH:
        if (time.time() - start_time) > 0.1:
            return -1
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def measure_distance2():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    start_time = time.time()
    while GPIO.input(ECHO_PIN2) == GPIO.LOW:
        if (time.time() - start_time) > 0.1:
            return -1
    pulse_start2 = time.time()
    while GPIO.input(ECHO_PIN2) == GPIO.HIGH:
        if (time.time() - start_time) > 0.1:
            return -1
    pulse_end2 = time.time()

    pulse_duration2 = pulse_end2 - pulse_start2
    distance2 = pulse_duration2 * 17150
    distance2 = round(distance2, 2)

    return distance2

distance = measure_distance()
distance2 = measure_distance2()

in1 = 24
in2 = 23
en = 25
en2 = 17
in12 = 27
in22 = 22

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 100)

GPIO.setup(in12, GPIO.OUT)
GPIO.setup(in22, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.output(in12, GPIO.LOW)
GPIO.output(in22, GPIO.LOW)
p2 = GPIO.PWM(en2, 100)

p.start(100)
p2.start(100)

napred = []
vurti = []
index = []

vremevurti = time.time()

start_time = time.time()
ok = 0
ok2 = 0
while (time.time() - start_time) < 10:
    vurti.append(time.time() - vremevurti)
    ok2 = 0
    if ok == 0:
        vremenapred = time.time()
        ok = 1
    distance = measure_distance()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in12, GPIO.LOW)
    GPIO.output(in22, GPIO.HIGH)

    if distance < 15 or distance2 > 10:
        nakude = random.randint(0, 1)
        napred.append(time.time() - vremenapred)
        ok = 0
        if ok2 == 0:
            vremevurti = time.time()
            ok2 = 1
        if nakude == 0:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in12, GPIO.HIGH)
            GPIO.output(in22, GPIO.LOW)
            index.append(0)
            time.sleep(2)
        else:
            GPIO.output(in12, GPIO.LOW)
            GPIO.output(in22, GPIO.HIGH)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            index.append(1)
            time.sleep(2)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in12, GPIO.LOW)
GPIO.output(in22, GPIO.LOW)

i = len(napred) - 1
j = len(vurti) - 1
z = len(index)

start_time = time.time()
while (time.time() - start_time) < 10:
    if ok2 == 1:
        nazadvreme = time.time()
        while napred[i] > (time.time() - nazadvreme):
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in12, GPIO.HIGH)
            GPIO.output(in22, GPIO.LOW)
        ok2 = 0
        ok = 1
        i = i - 1
    if ok == 1:
        vreme = time.time()
        while j > 0 and vurti[j] > (time.time() - vreme):
            if index[z-1] == 0:
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in12, GPIO.LOW)
                GPIO.output(in22, GPIO.HIGH)
            else:
                GPIO.output(in12, GPIO.HIGH)
                GPIO.output(in22, GPIO.LOW)
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
            ok2 = 1
            ok = 0
        j = j - 1
        z = z - 1

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in12, GPIO.LOW)
GPIO.output(in22, GPIO.LOW)

p.stop()
p2.stop()

GPIO.cleanup()
time.sleep(5)

