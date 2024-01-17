import cv2
import time
import datetime

frame = cv2.imread("image2.jpg")

face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
hog_body_detection = cv2.HOGDescriptor()
hog_body_detection.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


detection = False
detection_stopped_time = None
timer_started = False
start_record_in = 5

frame_size = (frame.shape[1], frame.shape[0])
fourcc = cv2.VideoWriter_fourcc(*"mp4v")           # Four Character Code for mp4v

body_count = 0
face_count = 0

while True:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)          # Gray Scale Image
    faces = face_detection.detectMultiScale(gray, 1.3, 5)     # Image, Speed+accuracy(1-1.5), min no. to detect
    bodies, _ = hog_body_detection.detectMultiScale(gray)

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
                print("End Recording")
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    for (x, y, width, height) in bodies:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)

    cv2.putText(frame, f"Face Count = {face_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f"Body Count: {body_count}", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("image", frame)

    if cv2.waitKey(0) == ord('q'):
        break

out.release()
cv2.destroyAllWindows()
