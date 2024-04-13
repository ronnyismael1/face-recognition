# This file is to train the face recognition algorithm to recognize the faces of the users.
import face_recognition
from Flask.Website.models import User  # adjust the import path as necessary
from Flask.Website import db, create_app  # adjust the import path as necessary
from io import BytesIO

app = create_app()  # create an instance of the Flask application

def load_known_faces_and_names():
    with app.app_context():  # necessary to access the database outside of Flask context
        users = User.query.all()
        known_faces = []
        known_names = []
        for user in users:
            if user.profile_picture and user.first_name:
                user_image = face_recognition.load_image_file(
                    BytesIO(user.profile_picture)
                )
                user_face_encoding = face_recognition.face_encodings(user_image)[0]
                known_faces.append(user_face_encoding)
                known_names.append(user.first_name)
        return known_faces, known_names


known_faces, known_faces_names = load_known_faces_and_names()

# Loading sample picture and learn how to recognize it
#ronny_image = face_recognition.load_image_file("biometric_recognition/train/ronny/ronny.png")
#ronny_face_encoding = face_recognition.face_encodings(ronny_image)[0]

# Load a second sample picture and learn how to recognize it
#obama_image = face_recognition.load_image_file("biometric_recognition/train/obama/obama.png")
#obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Create array(s) of known face encodings and their names
#known_faces = [
    #ronny_face_encoding,
    #obama_face_encoding,
#]
#known_faces_names = [
    #"Ronny",
    #"obama",
#]

def recognize_faces(image):
    # Find all the faces and face encodings in the image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    names = []

    # Loop through each face found in the image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_faces, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one
        if True in matches:
            first_match_index = matches.index(True)
            name = known_faces_names[first_match_index]

        names.append((name, (top, right, bottom, left)))
    return names