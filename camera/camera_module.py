import cv2
import sys
import os
import threading
import queue
from Flask.Website.models import User
from biometric_recognition.recognize_faces import recognize_faces

from utilities.lock_module import unlock_door

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    biometric_recognition_dir = os.path.join(current_dir, '..', 'biometric_recognition')
    sys.path.append(biometric_recognition_dir)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_counter = 0
    skip_frames = 5
    last_names_scaled = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("\nError: Could not read frame from camera.")
            break

        if frame_counter % skip_frames == 0:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            names = recognize_faces(small_frame)

            last_names_scaled = [(name, (top * 4, right * 4, bottom * 4, left * 4))
                                 for name, (top, right, bottom, left) in names]

            for name, (top, right, bottom, left) in last_names_scaled:
                if name != "Unknown":
                    recognized_user = User.find_by_name_and_logged_in_status(name)
                    if recognized_user:
                        print(f"Detected and logged in: {name}")
                        unlock_door()

        for name, (top, right, bottom, left) in last_names_scaled:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_counter += 1

    cap.release()
    cv2.destroyAllWindows()

def start():
    main()
    
if __name__ == "__main__":
    start()
