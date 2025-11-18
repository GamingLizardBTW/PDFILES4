import logging
log = logging.Logger('P212-robot')

import commands2
import phoenix6
from phoenix6.controls import VoltageOut, MotionMagicVoltage
from phoenix6 import configs
import wpilib

from constants import ELEC, SW, MECH


class SecondMotorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:
        super().__init__()

        self.second_motor = phoenix6.hardware.TalonFX(ELEC.second_motor_CAN_ID)
        self.limit_switch = wpilib.DigitalInput(ELEC.limit_switch_port)
        self.is_limit_pressed = lambda: self.limit_switch.get()

        self.request = VoltageOut(0)

        # Motion Magic control request
        self.motion_magic = MotionMagicVoltage(0)
        config = configs.TalonFXConfiguration()

        # Sensor-to-mechanism ratio
        config.feedback.sensor_to_mechanism_ratio = SW.Second_Gear_Ratio

        # Motion Magic parameters
        config.motion_magic.motion_magic_cruise_velocity = SW.Second_Cruise_Velocity
        config.motion_magic.motion_magic_acceleration = SW.Second_Acceleration
        config.motion_magic.motion_magic_jerk = SW.Second_Jerk

        slot0 = config.slot0
        slot0.k_s = SW.Second_ks
        slot0.k_v = SW.Second_kv
        slot0.k_a = SW.Second_ka
        slot0.k_p = SW.Second_kp
        slot0.k_i = SW.Second_ki
        slot0.k_d = SW.Second_kd

        self.second_motor.configurator.apply(config)


    def run(self, speed: float):

        if speed > 0 and self.is_limit_pressed():
            speed = 0.0

        self.second_motor.set_control(
            self.request.with_output(speed * 12.0)
        )

    def go_forward(self):
        self.run(1.0)

    def go_reverse(self):
        self.run(-1.0)

    def stop(self):
        self.run(0.0)

    def get_encoder_position(self) -> float:

        rotations = self.second_motor.get_rotor_position().value
        degrees = rotations * 360.0
        wrapped = degrees % 360.0
        return wrapped
    
    def secondmotorPID(self, target):

        self.second_motor.set_control(self.motion_magic.with_position(target).with_slot(0))


    def periodic(self):
        #Rotations
        position = self.second_motor.get_rotor_position().value

        #Position in degrees
        rotations = self.second_motor.get_rotor_position().value
        degrees = rotations * 360.0
        wrapped = degrees % 360.0

        #Where it is trying to go
        #setpoint = self.second_motor.get_differential_closed_loop_reference().value

        #speed
        velocity = self.second_motor.get_velocity().value

        wpilib.SmartDashboard.putNumber("SecondMotor Rotations", position)
        wpilib.SmartDashboard.putNumber("SecondMotor Position Degrees", wrapped)
        #wpilib.SmartDashboard.putNumber("SecondMotor Setpoint", setpoint)
        wpilib.SmartDashboard.putNumber("SecondMotor Velocity", velocity)
        wpilib.SmartDashboard.putBoolean("SecondMotor Limit Switch", self.is_limit_pressed())
