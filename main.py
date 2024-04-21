import threading
from Flask.Website import create_app  # Importing create_app function
<<<<<<< HEAD
import camera.camera_module as camera  # Importing camera module

# Creating Flask app instance using factory function
=======
import camera.camera_module as camera  # Importing 
#Creating Flask app instance using factory function
>>>>>>> 26f58b0f196b561e4986b4d1a92d6e86f7aec2a6
app = create_app()

def run_camera():
    with app.app_context():
        camera.start()

if __name__ == "__main__":
    # Run the camera in a separate thread
    camera_thread = threading.Thread(target=run_camera)
    camera_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)