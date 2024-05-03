import sys
import threading
from Flask.Website import create_app  # Importing create_app function
import camera.camera_module as camera  # Importing 

from biometric_recognition.recognize_faces import refresh_known_faces
#Creating Flask app instance using factory function

app = create_app()

def run_camera():
    with app.app_context():
        camera.start()

if __name__ == "__main__":
    # Initial loading of known faces
    refresh_known_faces()
    # Run the camera in a separate thread
    camera_thread = threading.Thread(target=run_camera)
    camera_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)