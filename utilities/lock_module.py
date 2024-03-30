#GPIO controls for rasberry pi

import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def initialize_lock():
    GPIO.output(18, GPIO.LOW) # initially unlocked
    sleep(5)

def unlock_door():
    GPIO.output(18, GPIO.HIGH)  # Assume HIGH signal unlocks the door
    sleep(10)  # Keep unlocked for 10 seconds
    lock_door()  # Re-lock the door automatically after 5 seconds

def lock_door():
    GPIO.output(18, GPIO.LOW)  # Assume LOW signal locks the door
