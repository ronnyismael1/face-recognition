# This code is responsible for capturing frames from the camera, detecting the user's face, 
# and drawing a box around it. It will provide the input (video frames) that the face
# recognition algorithm will use to recognize the user's face.

import sys
import os
import cv2
import face_recognition

# Get the directory containing this file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the biometric_recognition directory
biometric_recognition_dir = os.path.join(current_dir, '..', 'biometric_recognition')
# Add the biometric_recognition directory to the Python path
sys.path.append(biometric_recognition_dir)

from biometric_recognition.recognize_faces import recognize_faces

# Initialize the camera (use 0 for the laptop's built-in camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame was successfully read
    if not ret:
        print("\nError: Could not read frame from camera. Please check your camera connection and try again.\n")
        break

    # Recognize faces in the frame
    names = recognize_faces(frame)

    # Draw a box and name for each recognized face
    for name, (top, right, bottom, left) in names:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Quit the program when 'q' is pressed or the window is closed
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
        break

# When everything is done, release the capture and close the windows
cap.release()
cv2.destroyAllWindows()
