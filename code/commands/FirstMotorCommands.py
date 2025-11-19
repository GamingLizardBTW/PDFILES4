import logging
logger = logging.getLogger("firstmotorsubsystemlogger")



import commands2
import constants
from constants import OP, SW



from subsystems.FirstMotorSubsystem import FirstMotorSubsystemClass


class  ForwardSpin(commands2.Command):

    def __init__(self, firstmotorsubsystem: FirstMotorSubsystemClass) -> None:

        
        self.firstmotorsub = firstmotorsubsystem
        self.addRequirements(self.firstmotorsub)

    def initialize(self):
        self.firstmotorsub.go_forward()
        logger.info("Forward Command Initialized")  

    #def execute(self):
        
        #self.motorsub.go_forward
        #logger.info("Forward Command Running")

    def isFinished(self):

        return True

    #def end(self, interrupted: bool):

        #self.motorsub.stop()

class  ReverseSpin(commands2.Command):

    def __init__(self, firstmotorsubsystem: FirstMotorSubsystemClass) -> None:

        
        self.firstmotorsub = firstmotorsubsystem
        self.addRequirements(self.firstmotorsub)

    def initialize(self):
        self.firstmotorsub.go_reverse()
        logger.info("Reverse Command Initialized")

    #def execute(self):

        #self.motorsub.go_reverse
        #logger.info("Reverse Command Initialized")

    def isFinished(self):

        return True

    #def end(self, interrupted: bool):

        #self.motorsub.stop()

class  StopSpin(commands2.Command):

    def __init__(self, firstmotorsubsystem: FirstMotorSubsystemClass) -> None:

        self.firstmotorsub = firstmotorsubsystem
        self.addRequirements(self.firstmotorsub)

    def initialize(self):
        self.firstmotorsub.stop()
        logger.info("Stop Command Initialized")

    #def execute(self):
        #self.motorsub.stop
        #logger.info("Stop Command Running")



    def isFinished(self):

        return True

    #def end(self, interrupted: bool):

        #self.motorsub.stop()

class MoveToPosition(commands2.Command):

    def __init__(self, firstmotorsubsytem: FirstMotorSubsystemClass) -> None:
        self.firstmotorsubs = firstmotorsubsytem
        self.addRequirements(self.firstmotorsubs)

    def initialize(self):
        logger.info("MoveToPosition Command Initialized")
        

    def execute(self):
        self.firstmotorsubs.firstmotorPID(SW.FirstMotorSetpoint)

    def isFinished(self):
        return False
    
    def end(self, interrupted):
        logger.info("MoveToPosition Command ended")
        print("Motion Magic Preset 1 Ended")
        self.firstmotorsubs.stop()