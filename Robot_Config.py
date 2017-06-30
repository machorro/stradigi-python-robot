import ConfigParser
import argparse

class RobotConfig(object):    
    _env = "CARPET"
    _rotationSpeed = 170
    _rotationDuration = 0.7
    _pin_sonar0 = 23 # RIGHT
    _pin_sonar1 = 24 # FRONT
    _pin_sonar2 = 25 # LEFT
    _dist = 40
    
    _left_trim = 0
    _right_trim = 0
    
    def __init__(self):
        config_name = None
        
        # parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', metavar='-C', default='config.robot', type=str, help='point to a config file')
        args = parser.parse_args()
        config_name = args.config
        
        # parse config file
        try:
            print config_name
            config = ConfigParser.ConfigParser()
            config.readfp(open(config_name))
            print "Using config file: '" + config_name + "'"
        
            self._env = config.get('DEFAULT', 'Environment')
            
            self._rotationSpeed = config.getint(self._env, 'RotationSpeed')
            self._rotationDuration = config.getfloat(self._env, 'RotationDuration')
            
            print "Rotation Speed = " + str(self._rotationSpeed)
            print "Rotation Duration = " + str(self._rotationDuration)
            
            self._pin_sonar0 = config.getint('SONAR', 'PinSonar0')
            self._pin_sonar1 = config.getint('SONAR', 'PinSonar1')
            self._pin_sonar2 = config.getint('SONAR', 'PinSonar2')
            
            self._left_trim = config.getint('MOTOR', 'LeftTrim')
            self._right_trim = config.getint('MOTOR', 'RightTrim')
            self._dist = config.getint('SONAR', 'Distance')
            pass
        except (RuntimeError, TypeError, NameError):
            print NameError
            print "Not using a config file "
            pass
        pass

        
