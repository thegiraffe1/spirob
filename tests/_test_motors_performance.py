from motors import Motors
import pytest
import time

PUL = [17, 22, 25] 
DIR = [27, 23, 24] 
MOTOR_ORIENTATION = [True, False, True]

# @pytest.fixture
# def my_motor():
#     return Motors(
#         PUL, 
#         DIR, 
#         MOTOR_ORIENTATION, 
#         steps_per_rev=400, 
#         max_rpm=30, 
#         pulse_width=10 * 1e-6, 
#         debug=True)

def test_update_10s():
    my_motor = Motors(
        PUL, 
        DIR, 
        MOTOR_ORIENTATION, 
        steps_per_rev=400, 
        max_rpm=30, 
        pulse_width=10 * 1e-6, 
        debug=True)
    # run at 30 rpm -> .5 rps, 400 steps/rev -> 200 steps in 1s
    my_motor.set_motor_speed(0, 1)
    my_motor.start_motor(0)
    start_time = time.perf_counter_ns()
    num_pulses = 0
    num_loops = 0
    while time.perf_counter_ns() < start_time + 10e9:
        status = my_motor.update(0)
        if status > 0: 
            num_pulses += 1
        num_loops += 1
    print(num_pulses, num_loops)
    # assert False
    assert abs(num_pulses - 2000) <= 3
    