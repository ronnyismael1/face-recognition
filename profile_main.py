import cProfile
import main

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    
    main.camera.start()

    profiler.disable()
    profiler.dump_stats("main_profile.prof")
