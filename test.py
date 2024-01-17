import cv2
import os

# Load an image file
image_path = "C:/Users/Jay_s/PycharmProjects/IRP/Test_images/image10.jpg"
image = cv2.imread(image_path)

face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
hog_body_detection = cv2.HOGDescriptor()
hog_body_detection.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = face_detection.detectMultiScale(gray, 1.3, 5)
bodies, _ = hog_body_detection.detectMultiScale(gray)

body_count = len(bodies)
face_count = len(faces)

for (x, y, width, height) in faces:
    cv2.rectangle(image, (x, y), (x + width, y + height), (255, 0, 0), 3)

#for (x, y, width, height) in bodies:
    #cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 3)

cv2.putText(image, f"Face Count = {face_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#cv2.putText(image, f"Body Count: {body_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


# Save the processed image
cv2.imwrite("output_image.jpg", image)

# Show the processed image
cv2.imshow("Processed Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
