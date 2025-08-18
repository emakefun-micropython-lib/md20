import machine
import time
import md20

__version__ = "1.0.0"

print(f"example version: {__version__}")
print(f"md20 lib version: {md20.__version__}")

# setup
i2c = machine.I2C(0, sda=21, scl=22, freq=400000)
md20_obj = md20.Md20(i2c)
print(f"device id: {md20_obj.device_id:#04x}")
print(f"name: {md20_obj.name}")
print(f"firmware version: {md20_obj.firmware_version}")

# setup encoder motor
for i in range(md20.MOTOR_NUM):
    md20_obj[i].setup_encoder_mode(12, 90, md20.PHASE_RELATION_A_PHASE_LEADS)
    md20_obj[i].speed_pid_p = 1.5
    md20_obj[i].speed_pid_i = 1.5
    md20_obj[i].speed_pid_d = 1.0
    md20_obj[i].position_pid_p = 10.0
    md20_obj[i].position_pid_i = 1.0
    md20_obj[i].position_pid_d = 1.0
    print(
        f"motor {i} state: {md20_obj[i].state},",
        f"speed pid p: {md20_obj[i].speed_pid_p},",
        f"speed pid i: {md20_obj[i].speed_pid_i},",
        f"speed d: {md20_obj[i].speed_pid_d},",
        f"position p: {md20_obj[i].position_pid_p},",
        f"position i: {md20_obj[i].position_pid_i},",
        f"position d: {md20_obj[i].position_pid_d}",
    )

last_print_time = time.ticks_ms()
trigger_time = 0
pwm_duty = 1023

while True:
    if trigger_time == 0 or time.ticks_ms() - trigger_time > 2000:
        trigger_time = time.ticks_ms()
        for i in range(md20.MOTOR_NUM):
            print(f"motor {i} run pwm duty: {pwm_duty}")
            md20_obj[i].run_pwm_duty(pwm_duty)
        pwm_duty = -pwm_duty

    if time.ticks_ms() - last_print_time > 200:
        last_print_time = time.ticks_ms()
        print(
            f"speeds:{md20_obj[0].speed:4}, {md20_obj[1].speed:4}, {md20_obj[2].speed:4}, {md20_obj[3].speed:4},",
            f"pwm duties: {md20_obj[0].pwm_duty:5}, {md20_obj[1].pwm_duty:5}, {md20_obj[2].pwm_duty:5}, {md20_obj[3].pwm_duty:5},",
            f"positions: {md20_obj[0].position}, {md20_obj[1].position}, {md20_obj[2].position}, {md20_obj[3].position},",
            f"pulse counts: {md20_obj[0].pulse_count}, {md20_obj[1].pulse_count}, {md20_obj[2].pulse_count}, {md20_obj[3].pulse_count},",
            f"states: {md20_obj[0].state}, {md20_obj[1].state}, {md20_obj[2].state}, {md20_obj[3].state}",
        )
