import face_recognition
from Flask.Website.models import User  # Ensure this path matches the location of your User class
from io import BytesIO
import base64

# This function now uses Firebase to fetch user data
def load_known_faces_and_names():
    users = User.get_all()  # Using the get_all method from your Firebase User model
    known_faces = []
    known_names = []
    for user in users:
        if user.profile_picture and user.first_name:
            try:
                # Decode the base64 string; handle the case where you might not have the header
                profile_picture_data = user.profile_picture
                if ',' in profile_picture_data:
                    # Split the string on the comma to remove the data URL prefix if present
                    _, base64_encoded_data = profile_picture_data.split(',', 1)
                else:
                    base64_encoded_data = profile_picture_data

                # Convert the base64 encoded data into bytes
                user_image_data = base64.b64decode(base64_encoded_data)
                # Convert bytes data to a stream
                user_image_stream = BytesIO(user_image_data)
                user_image = face_recognition.load_image_file(user_image_stream)
                
                # Try to obtain face encodings; skip if no faces are found in the image
                user_face_encodings = face_recognition.face_encodings(user_image)
                if user_face_encodings:
                    user_face_encoding = user_face_encodings[0]
                    known_faces.append(user_face_encoding)
                    known_names.append(user.first_name)
            except Exception as e:
                print(f"Failed to process image for user {user.first_name}: {e}")
    return known_faces, known_names


known_faces, known_faces_names = load_known_faces_and_names()

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
