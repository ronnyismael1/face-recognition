# This code is responsible for capturing frames from the camera, detecting the user's face, 
# and drawing a box around it. It will provide the input (video frames) that the face
# recognition algorithm will use to recognize the user's face.

import cv2
import sys
import os
import face_recognition
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Import your face recognition module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'biometric_recognition'))
from biometric_recognition.recognize_faces import recognize_faces
from utilities.lock_module import unlock_door

# Initialize camera
cap = cv2.VideoCapture(0)

def process_frame(frame, executor):
    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Submit the frame for processing
    future = executor.submit(recognize_faces, small_frame)
    return future

def main():
    with ThreadPoolExecutor(max_workers=1) as executor:
        frame_futures = []
        last_names_scaled = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("\nError: Could not read frame from camera. Please check your camera connection and try again.\n")
                break
            
            # Submit the current frame for processing
            future = process_frame(frame, executor)
            frame_futures.append((future, frame))
            
            # Check for any completed futures
            for future, original_frame in frame_futures:
                if future.done():
                    names = future.result()
                    last_names_scaled = [(name, (top * 4, right * 4, bottom * 4, left * 4)) for name, (top, right, bottom, left) in names]
                    frame_futures.remove((future, original_frame))
                # Check if a known face is detected and unlock the door
                for name, _ in last_names_scaled:
                    if name != "Unknown":
                        print(f"Detected: {name}")
                        unlock_door()
                        break  # If at least one known face is detected, unlock the door
                    
            # Draw boxes and names on the original frame
            for name, (top, right, bottom, left) in last_names_scaled:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
            
            cv2.imshow('Video', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q') < 1:
                break
        
        # Wait for all tasks to complete before exiting
        futures_only = [future for future, _ in frame_futures]
        for future in as_completed(futures_only):
            # You could process results here if needed
            pass        
        
    cap.release()
    cv2.destroyAllWindows()
    
def start():
    main()
if __name__ == "__main__":
    start()
