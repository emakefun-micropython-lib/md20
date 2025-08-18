import machine
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

for i in range(md20.MOTOR_NUM):
    print(f"motor {i} state: {md20_obj[i].state}")
    md20_obj[i].reset()
    print(f"after reset motor {i} state: {md20_obj[i].state}")
