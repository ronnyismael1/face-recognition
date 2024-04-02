import camera.camera_module as camera # Capture video frames to pass to the face recognition algoritm
#from utilities.lock_module import initialize_lock

if __name__ == "__main__":
    #initialize_lock()
    camera.start()
    #initialize_lock() # If camera closes during lock, reinitialize lock to prevent deadlock
