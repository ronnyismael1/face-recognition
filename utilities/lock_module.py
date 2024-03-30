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
    last_unlock_time = current_time

def lock_door():
    global last_unlock_time
    current_time = time.time()

    if current_time - last_unlock_time >= 10:  # 10 seconds have passed
        print("Locking...")
        GPIO.output(18, GPIO.HIGH)  # HIGH signal locks the door
        print("Locking complete.\n")
