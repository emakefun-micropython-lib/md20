import struct


class Md20:
    STATE_IDLE: int = 0
    STATE_RUNNING_WITH_PWM_DUTY: int = 1
    STATE_RUNNING_WITH_SPEED: int = 2
    STATE_RUNNING_TO_POSITION: int = 3
    STATE_REACHED_POSITION: int = 4

    PHASE_RELATION_A_PHASE_LEADS: int = 0
    PHASE_RELATION_B_PHASE_LEADS: int = 1

    _CMD_RESET: int = 1
    _CMD_INIT: int = 2
    _CMD_SET_SPEED_P: int = 3
    _CMD_SET_SPEED_I: int = 4
    _CMD_SET_SPEED_D: int = 5
    _CMD_SET_POSITION_P: int = 6
    _CMD_SET_POSITION_I: int = 7
    _CMD_SET_POSITION_D: int = 8
    _CMD_SET_POSITION: int = 9
    _CMD_SET_PULSE_COUNT: int = 10
    _CMD_STOP: int = 11
    _CMD_RUN_PWM_DUTY: int = 12
    _CMD_RUN_SPEED: int = 13
    _CMD_MOVE_TO: int = 14
    _CMD_MOVE: int = 15

    _MEM_ADDR_MAJOR_VERSION: int = 0x01
    _MEM_ADDR_MINOR_VERSION: int = 0x00
    _MEM_ADDR_PATCH_VERSION: int = 0x00

    _MEM_ADDR_CMD_TYPE_BEGIN: int = 0x10
    _CMD_OFFSET: int = 0x11

    _MEM_ADDR_STATE: int = 0x60
    _MEM_ADDR_SPEED_P: int = 0x62
    _MEM_ADDR_SPEED_I: int = 0x64
    _MEM_ADDR_SPEED_D: int = 0x66
    _MEM_ADDR_POSITION_P: int = 0x68
    _MEM_ADDR_POSITION_I: int = 0x6A
    _MEM_ADDR_POSITION_D: int = 0x6C
    _MEM_ADDR_SPEED: int = 0x70
    _MEM_ADDR_POSITION: int = 0x74
    _MEM_ADDR_PULSE_COUNT: int = 0x78
    _MEM_ADDR_PWM_DUTY: int = 0x7C

    _MOTOR_INFO_OFFSET: int = 0x20

    class Motor:

        def __init__(self, index, i2c, i2c_address):
            self._index = index
            self._i2c = i2c
            self._i2c_address = i2c_address
            self.reset()

        def _wait_command_emptied(self):
            while (
                self._i2c.readfrom_mem(
                    self._i2c_address,
                    Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                    1,
                )[0]
                != 0
            ):
                pass

        def reset(self):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                bytes([Md20._CMD_RESET]),
            )

        def init(self, ppr, reduction_ration, phase_relation):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BHHB", Md20._CMD_INIT, ppr, reduction_ration, phase_relation
                ),
            )

        @property
        def speed_p(self):
            return (
                struct.unpack(
                    "<H",
                    self._i2c.readfrom_mem(
                        self._i2c_address,
                        Md20._MEM_ADDR_SPEED_P + self._index * Md20._MOTOR_INFO_OFFSET,
                        2,
                    ),
                )[0]
                / 100
            )

        @speed_p.setter
        def speed_p(self, value):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BH",
                    Md20._CMD_SET_SPEED_P,
                    int(value * 100),
                ),
            )
            self._wait_command_emptied()

        @property
        def speed_i(self):
            return (
                struct.unpack(
                    "<H",
                    self._i2c.readfrom_mem(
                        self._i2c_address,
                        Md20._MEM_ADDR_SPEED_I + self._index * Md20._MOTOR_INFO_OFFSET,
                        2,
                    ),
                )[0]
                / 100
            )

        @speed_i.setter
        def speed_i(self, value):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BH",
                    Md20._CMD_SET_SPEED_I,
                    int(value * 100),
                ),
            )
            self._wait_command_emptied()

        @property
        def speed_d(self):
            return (
                struct.unpack(
                    "<H",
                    self._i2c.readfrom_mem(
                        self._i2c_address,
                        Md20._MEM_ADDR_SPEED_D + self._index * Md20._MOTOR_INFO_OFFSET,
                        2,
                    ),
                )[0]
                / 100
            )

        @speed_d.setter
        def speed_d(self, value):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BH",
                    Md20._CMD_SET_SPEED_D,
                    int(value * 100),
                ),
            )
            self._wait_command_emptied()

        @property
        def position_p(self):
            return (
                struct.unpack(
                    "<H",
                    self._i2c.readfrom_mem(
                        self._i2c_address,
                        Md20._MEM_ADDR_POSITION_P
                        + self._index * Md20._MOTOR_INFO_OFFSET,
                        2,
                    ),
                )[0]
                / 100
            )

        @position_p.setter
        def position_p(self, value):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BH",
                    Md20._CMD_SET_POSITION_P,
                    int(value * 100),
                ),
            )
            self._wait_command_emptied()

        @property
        def position_i(self):
            return (
                struct.unpack(
                    "<H",
                    self._i2c.readfrom_mem(
                        self._i2c_address,
                        Md20._MEM_ADDR_POSITION_I
                        + self._index * Md20._MOTOR_INFO_OFFSET,
                        2,
                    ),
                )[0]
                / 100
            )

        @position_i.setter
        def position_i(self, value):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BH",
                    Md20._CMD_SET_POSITION_I,
                    int(value * 100),
                ),
            )
            self._wait_command_emptied()

        @property
        def position_d(self):
            return (
                struct.unpack(
                    "<H",
                    self._i2c.readfrom_mem(
                        self._i2c_address,
                        Md20._MEM_ADDR_POSITION_D
                        + self._index * Md20._MOTOR_INFO_OFFSET,
                        2,
                    ),
                )[0]
                / 100
            )

        @position_d.setter
        def position_d(self, value):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BH",
                    Md20._CMD_SET_POSITION_D,
                    int(value * 100),
                ),
            )
            self._wait_command_emptied()

        def set_current_position(self, position):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BI",
                    Md20._CMD_SET_POSITION,
                    position,
                ),
            )

        def set_pulse_count(self, pulse_count):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack(
                    "<BI",
                    Md20._CMD_SET_PULSE_COUNT,
                    pulse_count,
                ),
            )

        def stop(self):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                bytes([Md20._CMD_STOP]),
            )
            self._wait_command_emptied()

        def run_speed(self, rpm):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack("<Bi", Md20._CMD_RUN_SPEED, rpm),
            )
            self._wait_command_emptied()

        def run_pwm_duty(self, pwm_duty):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack("<Bh", Md20._CMD_RUN_PWM_DUTY, pwm_duty),
            )
            self._wait_command_emptied()

        def move_to(self, position, speed):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack("<Bii", Md20._CMD_MOVE_TO, position, speed),
            )
            self._wait_command_emptied()

        def move(self, position, speed):
            self._wait_command_emptied()
            self._i2c.writeto_mem(
                self._i2c_address,
                Md20._MEM_ADDR_CMD_TYPE_BEGIN + self._index * Md20._CMD_OFFSET,
                struct.pack("<Bii", Md20._CMD_MOVE, position, speed),
            )
            self._wait_command_emptied()

        @property
        def state(self):
            return self._i2c.readfrom_mem(
                self._i2c_address,
                Md20._MEM_ADDR_STATE + self._index * Md20._MOTOR_INFO_OFFSET,
                1,
            )[0]

        @property
        def speed(self):
            return struct.unpack(
                "<i",
                self._i2c.readfrom_mem(
                    self._i2c_address,
                    Md20._MEM_ADDR_SPEED + self._index * Md20._MOTOR_INFO_OFFSET,
                    4,
                ),
            )[0]

        @property
        def position(self):
            return struct.unpack(
                "<i",
                self._i2c.readfrom_mem(
                    self._i2c_address,
                    Md20._MEM_ADDR_POSITION + self._index * Md20._MOTOR_INFO_OFFSET,
                    4,
                ),
            )[0]

        @property
        def pulse_count(self):
            return struct.unpack(
                "<i",
                self._i2c.readfrom_mem(
                    self._i2c_address,
                    Md20._MEM_ADDR_PULSE_COUNT + self._index * Md20._MOTOR_INFO_OFFSET,
                    4,
                ),
            )[0]

        @property
        def pwm_duty(self):
            return struct.unpack(
                "<h",
                self._i2c.readfrom_mem(
                    self._i2c_address,
                    Md20._MEM_ADDR_PWM_DUTY + self._index * Md20._MOTOR_INFO_OFFSET,
                    2,
                ),
            )[0]

    def __init__(self, i2c, i2c_address=0x16):
        self._i2c = i2c
        self._i2c_address = i2c_address
        self._motors = []
        for i in range(4):
            self._motors.append(Md20.Motor(i, i2c, i2c_address))

    def __getitem__(self, index):
        return self._motors[index]

    def device_version(self):
        version = self._i2c.readfrom_mem(
            self._i2c_address, Md20._MEM_ADDR_MAJOR_VERSION, 3
        )
        return f"{version[0]}.{version[1]}.{version[2]}"
