import ConfigParser
import argparse

class RobotConfig(object):    
    _pin_sonar0 = 23
    _pin_sonar1 = 24
    _pin_sonar2 = 25
    
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
            config = ConfigParser.ConfigParser()
            config.readfp(open(config_name))
            print "Using config file: '" + config_name + "'"
        
            self._pin_sonar0 = config.getint('SONAR', 'PinSonar0')
            self._pin_sonar1 = config.getint('SONAR', 'PinSonar1')
            self._pin_sonar2 = config.getint('SONAR', 'PinSonar2')
            
            self._left_trim = config.getint('MOTOR', 'LeftTrim')
            self._right_trim = config.getint('MOTOR', 'RightTrim')
            pass
        except:
            print "Not using a config file"
            pass
        pass

        