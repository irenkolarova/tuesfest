import cv2
import mediapipe as mp
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)


mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
tipIds = [4, 8, 12, 16, 20]


cap = cv2.VideoCapture(0)


GPIO.setmode(GPIO.BCM)
motor1A = 17
motor1B = 27
motor2A = 22
motor2B = 23
motor3A = 24
motor3B = 25
motor4A = 5
motor4B = 6


for pin in [motor1A, motor1B, motor2A, motor2B, motor3A, motor3B, motor4A, motor4B]:
    GPIO.setup(pin, GPIO.OUT)


def stop_all():
    for pin in [motor1A, motor1B, motor2A, motor2B, motor3A, motor3B, motor4A, motor4B]:
        GPIO.output(pin, False)

def forward():
    for pin in [motor1A, motor2A, motor3A, motor4A]:
        GPIO.output(pin, True)
    for pin in [motor1B, motor2B, motor3B, motor4B]:
        GPIO.output(pin, False)

def backward():
    for pin in [motor1A, motor2A, motor3A, motor4A]:
        GPIO.output(pin, False)
    for pin in [motor1B, motor2B, motor3B, motor4B]:
        GPIO.output(pin, True)

def left():
    GPIO.output(motor1A, True)
    GPIO.output(motor1B, False)
    GPIO.output(motor2A, True)
    GPIO.output(motor2B, False)
    GPIO.output(motor3A, False)
    GPIO.output(motor3B, True)
    GPIO.output(motor4A, False)
    GPIO.output(motor4B, True)

def right():
    GPIO.output(motor1A, False)
    GPIO.output(motor1B, True)
    GPIO.output(motor2A, False)
    GPIO.output(motor2B, True)
    GPIO.output(motor3A, True)
    GPIO.output(motor3B, False)
    GPIO.output(motor4A, True)
    GPIO.output(motor4B, False)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = cap.read()
        if ret:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            lmList = []
            if results.multi_hand_landmarks:
                for hand_landmark in results.multi_hand_landmarks:
                    myHands = results.multi_hand_landmarks[0]
                    for id, lm in enumerate(myHands.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)

            fingers = []
            if lmList:
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                finger_counter = fingers.count(1)

                if finger_counter == 5:
                    forward()
                elif finger_counter == 4:
                    backward()
                elif finger_counter == 0:
                    stop_all()
                elif finger_counter == 2:
                    right()
                elif finger_counter == 1:
                    left()

            cv2.imshow("result", image)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
