# Security Video Smart Lock

![board-prototype](images\board_prototype.png "Prototype of System")

## Overview

This project is a smart lock system that uses face recognition.
It is best used in a Linux environment, but it can also work in other environments.

## How it works

The ```recognize_faces.py``` script is structured to train a face recognition algorithm to recognize specific individuals by loading sample images, extracting face encodings, and then comparing these encodings against faces found in other images to identify them. The script defines a function recognize_faces(image) that takes an image as input, detects faces within it, and attempts to recognize these faces based on the known face encodings. This process involves loading and encoding sample images for known individuals (in this case, "Ronny" and "Obama") and then using these encodings to identify matches in the input image.

The ```camera_module.py``` script is responsible for capturing frames from the camera, processing them to detect and identify faces using the recognize_faces function imported from recognize_faces.py, and then displaying the video feed with boxes and names drawn around recognized faces. The script uses OpenCV for video capture and processing, including resizing frames for faster processing and toggling between processing frames to improve performance.

The ```main.py``` script is structured to import the camera module and then run a function from it (start()) to initiate the process of capturing video frames and recognizing faces.

## Dependancies

Some packages needed for the project to run:
* face_recognition_models
* Click>=6.0
* dlib>=19.3.0
* numpy
* Pillow
* scipy>=0.17.0

## Installation

*Note: For linux/MacOS be sure to use pip3/python3*

Before starting, make sure that your Python installation includes pip. You can ensure this by running:

```sh
python -m ensurepip --upgrade
```

This project uses an open-source facial recognition library. You can clone the repository with:

```sh
git clone https://github.com/ageitgey/face_recognition.git
```

Navigate to the cloned repository and install the necessary packages:

```sh
cd face_recognition
pip install -r requirements.txt
```

After that, install the face recognition library:

```sh
pip install face_recognition
```

This project also uses OpenCV for face tracking. You can install it with:

```sh
pip install opencv-python
```

For lock GPIO
```sh
sudo apt-get install python3-rpi.gpio
```

## Usage

After installing the necessary packages, you can start using the project.

```sh
python main.py
```

## Rasberry Pi (Linux)

Some things to consider.

1. When SSHing into the raspi consider using MobaXterm on your local machine so you can display graphical windows via SSH using X11 forwarding. This allows the graphical interface to be displayed on your local machine even though the program is running on the Raspberry Pi.

## Contributing

If you want to contribute to this project, please follow these steps:

- 1. Fork the project
- 2. Create your development branch (`git checkout -b development/feature`)
- 3. Commit your changes (`git commit -m 'Added some feature'`)
- 4. Push to the branch (`git push origin development/feature`)
- 5. Open a pull request

## Contact

- Ronny Ismael
- Cary Zheng
- Michael Zabaneh
- Mohammad Zaza
