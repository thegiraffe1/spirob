import time
from motors import Motors

def main_loop():
    PUL = [17, 22, 25] 
    DIR = [27, 23, 24] 
    MOTOR_ORIENTATION = [True, False, True]

    motors = Motors(
        PUL, 
        DIR, 
        MOTOR_ORIENTATION, 
        steps_per_rev=400, 
        max_rpm=30, 
        pulse_width=10 * 1e-6,
        debug=True)
    
    motors.set_motor_speed([0, 1, 2], 0.5)
    motors.start_motor([0, 1, 2])

    print("Starting main loop.")

    try:
        while True:
            motors.update([0, 1, 2])
    except KeyboardInterrupt:
        print("\nMain loop interrupted by Ctrl+C.")
    finally:
        motors.stop_motor([0, 1, 2])


if __name__ == "__main__":
    main_loop()