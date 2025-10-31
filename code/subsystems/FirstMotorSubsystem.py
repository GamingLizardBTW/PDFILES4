import logging
log = logging.Logger('P212-robot')
import wpilib
import commands2
import phoenix6
import wpimath.controller
import wpimath.trajectory

from constants import ELEC


class FirstMotorSubsystemClass(commands2.Subsystem):

    def __init__(self) -> None:


        self.first_motor = phoenix6.hardware.TalonFX(ELEC.first_motor_CAN_ID)
        #self.my_motor.setNeutralMode(self.brakemode)
        

    def go_forward(self):
        self.first_motor.set(ELEC.first_motor_forward)

    def go_reverse(self):
        self.first_motor.set(ELEC.first_motor_reverse)

    def stop(self):
 
        self.first_motor.set(ELEC.first_motor_stop)
