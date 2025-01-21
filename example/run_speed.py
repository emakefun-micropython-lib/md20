from md20 import Md20
import machine
import time

# setup
i2c = machine.I2C(0, sda=21, scl=22)

motor_driver = Md20(i2c)

for i in range(4):
    motor_driver[i].init(12, 90, Md20.PHASE_RELATION_A_PHASE_LEADS)

# loop
last_print_time = time.ticks_ms()
trigger_time = time.ticks_ms()
forward = True

while True:
    if forward:
        for i in range(4):
            motor_driver[i].run_speed(90)
    else:
        for i in range(4):
            motor_driver[i].run_speed(-90)

    if time.ticks_ms() - trigger_time > 2000:
        trigger_time = time.ticks_ms()
        forward = not forward

    if time.ticks_ms() - last_print_time > 200:
        last_print_time = time.ticks_ms()
        print(
            f"speeds:{motor_driver[0].speed:4}, {motor_driver[1].speed:4}, {motor_driver[2].speed:4}, {motor_driver[3].speed:4}",
            f", pwm duties: {motor_driver[0].pwm_duty:5}, {motor_driver[1].pwm_duty:5}, {motor_driver[2].pwm_duty:5}, {motor_driver[3].pwm_duty:5}",
            f", positions: {motor_driver[0].position}, {motor_driver[1].position}, {motor_driver[2].position}, {motor_driver[3].position}",
            f", pulse counts: {motor_driver[0].pulse_count}, {motor_driver[1].pulse_count}, {motor_driver[2].pulse_count}, {motor_driver[3].pulse_count}",
            f", states: {motor_driver[0].state}, {motor_driver[1].state}, {motor_driver[2].state}, {motor_driver[3].state}",
        )
