import RPi.GPIO as GPIO
import time
import ConfigParser
import argparse
from SonarMeasure import SonarMeasure

class TheBrain(object):
    # vars
    _sonar = None
    
    _pinSonar0 = 23
    _pinSonar1 = 24
    _pinSonar2 = 25
    
    def __init__(self):
        print "Initializing"
        
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
        
            self._pinSonar0 = config.getint('SONAR', 'PinSonar0')
            self._pinSonar1 = config.getint('SONAR', 'PinSonar1')
            self._pinSonar2 = config.getint('SONAR', 'PinSonar2')
            pass
        except:
            print "Not using a config file"
            pass
        
        self._sonar = SonarMeasure(self._pinSonar0, self._pinSonar1, self._pinSonar2)
        pass
        
    def run(self):
        print "Staring"
        
        try:
            while (True):
                print self._sonar.get_measures()
                time.sleep(2)
                
                pass # end loop
            pass # end run  
        except KeyboardInterrupt:
            # User pressed CTRL-C
            # Reset GPIO settings
            GPIO.cleanup()
            pass
    pass # end class

brain = TheBrain()
brain.run()
