import camera.camera_module as camera
from biometric_recognition.recognize_faces import refresh_known_faces
import threading

def run_camera():
    # Load known faces before starting the camera
    refresh_known_faces()
    # Start the camera
    camera.start()

if __name__ == "__main__":
    camera_thread = threading.Thread(target=run_camera)
    camera_thread.start()
    camera_thread.join()  # Ensure the thread runs continuously
