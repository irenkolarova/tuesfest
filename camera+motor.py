import cv2
import mediapipe as mp
import time
import RPi.GPIO as GPIO

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
tipIds = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

# Setup GPIO pins for motor control
GPIO.setmode(GPIO.BCM)
motor_pins = [23, 24, 25, 16]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Function to control motor direction
def set_motor_direction(direction):
    if direction == 'forward':
        GPIO.output(motor_pins[0], GPIO.HIGH)
        GPIO.output(motor_pins[1], GPIO.LOW)
        GPIO.output(motor_pins[2], GPIO.HIGH)
        GPIO.output(motor_pins[3], GPIO.LOW)
    elif direction == 'backward':
        GPIO.output(motor_pins[0], GPIO.LOW)
        GPIO.output(motor_pins[1], GPIO.HIGH)
        GPIO.output(motor_pins[2], GPIO.LOW)
        GPIO.output(motor_pins[3], GPIO.HIGH)
    else:
        GPIO.output(motor_pins[0], GPIO.LOW)
        GPIO.output(motor_pins[1], GPIO.LOW)
        GPIO.output(motor_pins[2], GPIO.LOW)
        GPIO.output(motor_pins[3], GPIO.LOW)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = cap.read()
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
        if len(lmList) != 0:
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

            print("Finger count:", finger_counter)

            if finger_counter == 5:
                set_motor_direction('forward')
                cv2.putText(image, 'Forward', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)
            elif finger_counter == 4:
                set_motor_direction('backward')
                cv2.putText(image, 'Backward', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)
            else:
                set_motor_direction('stop')
                cv2.putText(image, 'Stop', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)

        cv2.imshow("result", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
