import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def unlock_door():
    GPIO.output(18, GPIO.HIGH)  # Assume HIGH signal unlocks the door
    sleep(5)  # Keep unlocked for 5 seconds
    lock_door()  # Re-lock the door automatically after 5 seconds

def lock_door():
    GPIO.output(18, GPIO.LOW)  # Assume LOW signal locks the door
