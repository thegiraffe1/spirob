from motors import Motors
import time

PUL = [17, 22, 25] 
DIR = [27, 23, 24] 
MOTOR_ORIENTATION = [True, False, True]
    
def test_set_speed():
    motors = Motors(PUL, DIR, MOTOR_ORIENTATION, debug=True)
    motors.set_motor_speed(0, 0.5)
    assert motors._motor_speeds[0] == 0.5
    motors.set_motor_speed([0, 1, 2], 1)
    assert all([s == 1 for s in motors._motor_speeds])

def test_pulse_low_time():
    motors = Motors(PUL, DIR, MOTOR_ORIENTATION, steps_per_rev=400, max_rpm=30, pulse_width=10 * 1e-6, debug=True)
    assert abs(motors._get_pulse_low_time(1) - 4990 * 1e-6) < 1e-9

def test_pul_on_off():
    motors = Motors(PUL, DIR, MOTOR_ORIENTATION, steps_per_rev=400, max_rpm=30, pulse_width=10 * 1e-6, debug=True)
    
    motors._pul_motor_on(0)
    assert motors._PUL_devices[0].value == 1
    motors._pul_motor_off(0)
    assert motors._PUL_devices[0].value == 0
    
    motors._pul_motor_on([0, 1, 2])
    for d in motors._PUL_devices:
        assert d.value == 1
    motors._pul_motor_off([0, 1, 2])
    for d in motors._PUL_devices:
        assert d.value == 0

def test_dir_on_off():
    motors = Motors(PUL, DIR, MOTOR_ORIENTATION, steps_per_rev=400, max_rpm=30, pulse_width=10 * 1e-6, debug=True)
    
    motors.dir_motor_forward(0)
    assert motors._DIR_devices[0].value == MOTOR_ORIENTATION[0]
    motors.dir_motor_backward(0)
    assert motors._DIR_devices[0].value != MOTOR_ORIENTATION[0]

    motors.dir_motor_forward([0, 1, 2])
    for i in range(len(MOTOR_ORIENTATION)):
        assert motors._DIR_devices[i].value == MOTOR_ORIENTATION[i]
    motors.dir_motor_backward([0, 1, 2])
    for i in range(len(MOTOR_ORIENTATION)):
        assert motors._DIR_devices[i].value != MOTOR_ORIENTATION[i]

def test_start_stop_motor():
    motors = Motors(PUL, DIR, MOTOR_ORIENTATION, steps_per_rev=400, max_rpm=30, pulse_width=10 * 1e-6, debug=True)
    
    motors.start_motor(0)
    assert motors._motor_running[0]
    motors.stop_motor(0)
    assert not motors._motor_running[0]

    motors.start_motor([0, 1, 2])
    assert all(motors._motor_running)

    motors.stop_motor([0, 1, 2])
    assert not any(motors._motor_running)

def test_update_step():
    my_motor = Motors(
        PUL, 
        DIR, 
        MOTOR_ORIENTATION, 
        steps_per_rev=400, 
        max_rpm=30, 
        pulse_width=10 * 1e-6, 
        debug=True)
    my_motor.set_motor_speed(0, 1)
    assert my_motor.update(0) == 0, "updated when running=False"
    my_motor.start_motor(0)
    assert my_motor.update(0) == 1, "did not pulse high on start"
    assert my_motor.update(0) == 0, "counter triggered early"
    time.sleep(my_motor.pulse_width)
    assert my_motor.update(0) == -1, "did not pulse low after pulse width"
    assert my_motor.update(0) == 0, "counter triggered early"
    time.sleep(my_motor._get_pulse_low_time(1))
    assert my_motor.update(0) == 1, "did not pulse high after pulse low"
    assert my_motor.update(0) == 0, "counter triggered early"
    my_motor.stop_motor(0)
    time.sleep(my_motor.pulse_width)
    assert my_motor.update(0) == 0, "updated when running=False"