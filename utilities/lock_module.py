# GPIO controls for rasberry pi. Module uses threading to run function in background, so we 
# can have a thread to handle the delayed re-lock and run the main program in parallel.

import RPi.GPIO as GPIO
import time
from threading import Timer

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

last_unlock_time = 0

def initialize_lock():
    print("Initializing lock...")
    GPIO.output(18, GPIO.HIGH) # Initiate unlock
    time.sleep(1)
    print("Initialization complete.\n")

def unlock_door():
    global last_unlock_time
    current_time = time.time()

    if current_time - last_unlock_time < 20:
        # print(f"Too many requests: {int(20 - (current_time - last_unlock_time))}s remaining.")
        return

    print(f"Detected: {detected_name}")
    print("Unlocking...")
    GPIO.output(18, GPIO.LOW)  # LOW signal unlocks the door
    Timer(10, lock_door).start()
    last_unlock_time = time.time()

def lock_door():
    print("Locking...")
    GPIO.output(18, GPIO.HIGH)  # HIGH signal locks the door
    print("Locking complete.\n")
