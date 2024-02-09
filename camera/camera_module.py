# This code is responsible for capturing frames from the camera, detecting the user's face, 
# and drawing a box around it. It will provide the input (video frames) that the face
# recognition algorithm will use to recognize the user's face.

import cv2
import sys
import os
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

process_this_frame = True
last_names_scaled = []  # Store the last known faces and locations

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame was successfully read
    if not ret:
        print("\nError: Could not read frame from camera. Please check your camera connection and try again.\n")
        break

    # Resize frame of video for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    if process_this_frame:
        # Recognize faces in the resized frame
        names = recognize_faces(small_frame)

        # Scale back up face locations to the original frame size and store them
        last_names_scaled = [
            (name, (top * 4, right * 4, bottom * 4, left * 4))
            for name, (top, right, bottom, left) in names
        ]

    # Draw a box and name for each recognized face in the original frame using the last known data
    for name, (top, right, bottom, left) in last_names_scaled:
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Determine the size of the text to be drawn
        font = cv2.FONT_HERSHEY_DUPLEX
        text_width, text_height = cv2.getTextSize(name, font, 1.0, 1)[0]

        # Draw a filled rectangle to use as the label background
        label_height = text_height + 10  # Adjust padding as needed
        cv2.rectangle(frame, (left, top - label_height), (right, top), (0, 255, 0), cv2.FILLED)
        
        # Draw the text (name) on the label
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
    
    process_this_frame = not process_this_frame

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Quit the program when 'q' is pressed or the window is closed
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
        break

# When everything is done, release the capture and close the windows
cap.release()
cv2.destroyAllWindows()