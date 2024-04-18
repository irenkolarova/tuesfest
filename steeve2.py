#!/usr/bin/python3
import cv2
import numpy as np
import zmq
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import imghdr
import os
from password import ivan_password
import time

sender_email = 'ivan.g.genov.2021@elsys-bg.org'
password = ivan_password
receiver_email = 'gixirobot@gmail.com'
subject = 'Person detected'
body = 'A person has been detected in the video stream.'

face_cascade = cv2.CascadeClassifier('/home/cplisplqs/Desktop/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5555')

save_folder = 'face_images'
os.makedirs(save_folder, exist_ok=True)

while True:
    
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
    
        face_img = frame[y:y+h, x:x+w]

        filename = os.path.join(save_folder, f"face_{len(os.listdir(save_folder))}.png")
        cv2.imwrite(filename, face_img)

        _, img_encoded = cv2.imencode('.png', face_img)
        img_bytes = img_encoded.tobytes()

        footage_socket.send(img_bytes)

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Face Detection"
        message.attach(MIMEImage(img_bytes, name="face.png"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(message)
