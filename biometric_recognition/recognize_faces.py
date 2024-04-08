# This file is to train the face recognition algorithm to recognize the faces of the users.
import struct
import spidev
import face_recognition

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device 0
spi.max_speed_hz = 1_000_000  # 1MHz
spi.mode = 0 # CPOL=0, CPHA=0

# Loading sample picture and learn how to recognize it
ronny_image = face_recognition.load_image_file("biometric_recognition/train/ronny/ronny.png")
ronny_face_encoding = face_recognition.face_encodings(ronny_image)[0]

# Load a second sample picture and learn how to recognize it
obama_image = face_recognition.load_image_file("biometric_recognition/train/obama/obama.png")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Create array(s) of known face encodings and their names
known_faces = [
    ronny_face_encoding,
    obama_face_encoding,
]
known_faces_names = [
    "Ronny",
    "Obama",
]

def serialize_face_encodings(face_encodings):
    # Serialize face encodings into a byte stream.
    bytes_list = []
    for encoding in face_encodings:
        # Assuming each encoding is a 128-dimensional vector of floats.
        for float_num in encoding:
            bytes_list.extend(struct.pack('d', float_num))  # 'd' for double-precision float.
    return bytes_list

def recognize_faces(image):
    # Find all the faces and face encodings in the image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    names = []

    # Loop through each face found in the image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        size_of_response = 1  # Assuming a single byte response
        special_value_for_no_match = 255  # Assuming 255 indicates no match
        
        # Serialize the face encoding to bytes
        face_encoding_bytes = serialize_face_encodings([face_encoding])
        
        # Send the serialized face encoding to the FPGA
        spi.xfer2(face_encoding_bytes)

        # I need to adjust the code to receive the response from the FPGA.
        # Assume a simple response indicating the index of the recognized face.
        # Need to define the logic based on how I implement the FPGA side.
        response = spi.readbytes(size_of_response)  # Define `size_of_response` based on my FPGA implementation
        
        # Process the response to get the recognized face name
        # This part needs to be adjusted based on FPGA specific implementation.
        if response[0] != special_value_for_no_match:  # Define this value
            name = known_faces_names[response[0]]
        else:
            name = "Unknown"

        names.append((name, (top, right, bottom, left)))
    return names