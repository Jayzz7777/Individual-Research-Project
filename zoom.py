import cv2

# Load the Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Set the zoom scale factor
scale_factor = 1.5
#activeWindow = []

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    #currentWin = []
    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Iterate over each detected face
    for index, (x, y, w, h) in enumerate(faces):
        # Calculate the coordinates of the ROI
        roi_x = int(x - (scale_factor - 1) * w / 2)
        roi_y = int(y - (scale_factor - 1) * h / 2)
        roi_w = int(w * scale_factor)
        roi_h = int(h * scale_factor)

        # Crop the ROI from the image
        roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Resize the ROI to a larger size
        zoomed_roi = cv2.resize(roi, (w, h))

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Create a unique window name for each face
        zoomed_window_name = f'Zoomed ROI {index+1}'
        cv2.namedWindow(zoomed_window_name, cv2.WINDOW_NORMAL)
        #currentWin.append(zoomed_window_name)
        #if zoomed_window_name not in activeWindow:
         #   cv2.namedWindow(zoomed_window_name, cv2.WINDOW_NORMAL)


        # Display the zoomed ROI
        cv2.imshow(zoomed_window_name, zoomed_roi)
        # Set the zoomed window size
        cv2.resizeWindow(zoomed_window_name, 300, 300)

    # Display the original frame
    cv2.imshow('Original', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()

"""

#-----------------------------------------------------------------Image Detection---------------------------------------------------------
# Load the Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the image
img = cv2.imread('image2.jpg')

# Set the zoom scale factor
scale_factor = 1.5

# Convert the image to grayscale for face detection
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the grayscale image
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# Iterate over each detected face
for (x, y, w, h) in faces:
    # Calculate the coordinates of the ROI
    roi_x = int(x - (scale_factor - 1) * w / 2)
    roi_y = int(y - (scale_factor - 1) * h / 2)
    roi_w = int(w * scale_factor)
    roi_h = int(h * scale_factor)

    # Crop the ROI from the image
    roi = img[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

    # Resize the ROI to a larger size
    zoomed_roi = cv2.resize(roi, (w, h))

    # Draw a rectangle around the face
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the zoomed ROI
    cv2.imshow('Zoomed ROI', zoomed_roi)

# Display the original image
cv2.imshow('Original', img)

# Wait for a key press and then exit
cv2.waitKey(0)
cv2.destroyAllWindows()
"""