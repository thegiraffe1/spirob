from src.motors import Motors
import time
import numpy as np
import pytest
import asyncio

PUL = [17, 22, 25] 
DIR = [27, 23, 24] 
MOTOR_ORIENTATION = [True, False, True] # front left, front right, back

NUM_TRIALS = 100

async def asyncio_sleep(duration):
    await asyncio.sleep(duration)

async def delay_ns(duration):
    start_ns = time.perf_counter_ns()
    target_ns = start_ns + duration * 1e9
    while time.perf_counter_ns() < target_ns:
        pass

async def time_sleep(duration):
    time.sleep(duration)

motors = Motors(PUL, DIR, MOTOR_ORIENTATION, debug=True)
motors.set_motor_speed(0, 1)

def run_steps(sleep_func):
    async def run_trials(sleep_func):
        results = []
        for _ in range(NUM_TRIALS):
            start_time = time.perf_counter()

            motors._pul_motor_on(0)
            await sleep_func(motors.pulse_width)
            motors._pul_motor_off(0)
            delay = motors._get_pulse_low_time(1)
            await sleep_func(delay)

            end_time = time.perf_counter()
            time_elapsed = end_time - start_time

            results.append(time_elapsed)
        return np.array(results)

    return run_trials(sleep_func)
    

def test_step():
    expected_delay = motors._get_pulse_low_time(1) + motors.pulse_width
    for func in [asyncio_sleep, delay_ns, time_sleep]:
        print('Testing', func.__name__)
        results = asyncio.run(run_steps(func))
        average_length = sum(results) / len(results)
        print("expected", expected_delay)
        print("resultant average", average_length)
        print(results)

if __name__ == "__main__":
    test_step()