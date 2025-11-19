import logging
log = logging.Logger('P212-robot')
import wpilib
import commands2
import phoenix6
import wpimath.controller
import wpimath.trajectory
from phoenix6.controls import VoltageOut, MotionMagicVoltage
from phoenix6 import configs


from constants import ELEC, SW


class FirstMotorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:


        self.first_motor = phoenix6.hardware.TalonFX(ELEC.first_motor_CAN_ID)
        #self.my_motor.setNeutralMode(self.brakemode)

        # Motion Magic control request
        self.motion_magic = MotionMagicVoltage(0)
        config = configs.TalonFXConfiguration()

        # Sensor-to-mechanism ratio
        #config.feedback.sensor_to_mechanism_ratio = SW.Second_Gear_Ratio

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

        self.first_motor.configurator.apply(config)
        

    def go_forward(self):
        self.first_motor.set(ELEC.first_motor_forward)

    def go_reverse(self):
        self.first_motor.set(ELEC.first_motor_reverse)

    def stop(self):
 
        self.first_motor.set(ELEC.first_motor_stop)

    def firstmotorPID(self, target):

        self.first_motor.set_control(self.motion_magic.with_position(target).with_slot(0))


    def periodic(self):
        #Rotations
        position = self.first_motor.get_rotor_position().value

        #Position in degrees
        rotations = self.first_motor.get_rotor_position().value
        degrees = rotations * 360.0
        wrapped = degrees % 360.0

        #Where it is trying to go
        #setpoint = self.second_motor.get_differential_closed_loop_reference().value

        #speed
        velocity = self.first_motor.get_velocity().value

        wpilib.SmartDashboard.putNumber("SecondMotor Rotations", position)
        wpilib.SmartDashboard.putNumber("SecondMotor Position Degrees", wrapped)
        #wpilib.SmartDashboard.putNumber("SecondMotor Setpoint", setpoint)
        wpilib.SmartDashboard.putNumber("SecondMotor Velocity", velocity)
        #wpilib.SmartDashboard.putBoolean("SecondMotor Limit Switch", self.is_limit_pressed())
