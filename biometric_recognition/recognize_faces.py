import face_recognition
from Flask.Website.models import User
from io import BytesIO
import base64
from threading import Lock
import time

# Caching and lock for thread-safe operations
known_faces = []
known_names = []
cache_lock = Lock()
last_update_time = 0
cache_update_interval = 5  # seconds, adjust as needed

def load_known_faces_and_names():
    users = User.get_all()
    new_known_faces = []
    new_known_names = []
    for user in users:
        if user.profile_picture and user.first_name:
            try:
                if ',' in user.profile_picture:
                    _, base64_encoded_data = user.profile_picture.split(',', 1)
                else:
                    base64_encoded_data = user.profile_picture
                user_image_data = base64.b64decode(base64_encoded_data)
                user_image_stream = BytesIO(user_image_data)
                user_image = face_recognition.load_image_file(user_image_stream)
                user_face_encodings = face_recognition.face_encodings(user_image)
                if user_face_encodings:
                    new_known_faces.append(user_face_encodings[0])
                    new_known_names.append(user.first_name)
            except Exception as e:
                print(f"Error processing image for user {user.first_name}: {e}")
    return new_known_faces, new_known_names

def refresh_known_faces():
    global known_faces, known_names, last_update_time
    with cache_lock:
        known_faces, known_names = load_known_faces_and_names()
        last_update_time = time.time()

def recognize_faces(image):
    current_time = time.time()
    if current_time - last_update_time > cache_update_interval:
        refresh_known_faces()

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    names = []
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"
        
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        
        names.append((name, (top, right, bottom, left)))
    return names

