# GPIO controls for rasberry pi

import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

last_unlock_time = 0

def initialize_lock():
    print("Initializing lock...")
    GPIO.output(18, GPIO.HIGH) # Initiate unlock
    sleep(1)
    print("Initialization complete.\n")

def unlock_door():
    global last_unlock_time
    current_time = time.time()

    if current_time - last_unlock_time < 20:
        print(f"Too many requests: {int(20 - (current_time - last_unlock_time))}s remaining.")
        return

    print("Unlocking...")
    GPIO.output(18, GPIO.LOW)  # LOW signal unlocks the door
    sleep(10)  # Keep unlocked for 10 seconds
    print("Unlocking complete.\n")
    lock_door()  # Re-lock the door automatically after 5 seconds
    last_unlock_time = time.time()

def lock_door():
    print("Locking...")
    GPIO.output(18, GPIO.HIGH)  # HIGH signal locks the door
    print("Locking complete.\n")
