import cv2
import time
import datetime
import numpy as np
from cryptography.fernet import Fernet
import tensorflow as tf

# Generate key for encryption
key = Fernet.generate_key()

# Create Fernet object using the key
fernet = Fernet(key)

# Save the key to a file
with open('key.key', 'wb') as key_file:
    key_file.write(key)

cap = cv2.VideoCapture(0)

face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

model = tf.saved_model.load("models/detect")
infer = model.signatures["serving_default"]

detection = False
detection_stopped_time = None
timer_started = False
start_record_in = 5
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Four Character Code for mp4v

body_count = 0
face_count = 0

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray, 1.3, 5)

    input_data = cv2.resize(frame, (300, 300))
    input_data = np.expand_dims(input_data, axis=0).astype(np.float32)
    output_data = infer(input_1=input_data)['output_1'].numpy()
    bodies = output_data[0]

    body_count = len(bodies)
    face_count = len(faces)

    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter("C:/Users/Jay_s/PycharmProjects/IRP/Recorded_Videos/" + f"{current_time}.mp4", fourcc, 20, frame_size)

            print("Recording")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= start_record_in:
                detection = False
                timer_started = False
                out.release()

                # Read the recorded video file and convert it into bytes
                with open(f"C:/Users/Jay_s/PycharmProjects/IRP/Recorded_Videos/{current_time}.mp4", 'rb') as video_file:
                    video_bytes = video_file.read()

                # Encrypt the video bytes using Fernet
                encrypted_video_bytes = fernet.encrypt(video_bytes)

                # Write the encrypted bytes to a new file
                with open(f"C:/Users/Jay_s/PycharmProjects/IRP/Recorded_Videos/{current_time}_encrypted.mp4",
                          'wb') as encrypted_file:
                    encrypted_file.write(encrypted_video_bytes)

                print("Video encrypted and saved")

        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    for (x, y, width, height) in bodies:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)

    cv2.putText(frame, f"Face Count = {face_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f", Body Count: {body_count}", (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("camera", frame)

    if cv2.waitKey(1) == ord('q'):  # exit program with 'q'
        break

out.release()
cap.release()
cv2.destroyAllWindows()
