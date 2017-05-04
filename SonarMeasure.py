import time
import RPi.GPIO as GPIO

class SonarMeasure(object):

    # Vars
    _pins = None
    
    # Constructor
    def __init__(self, *pins):
        self._pins = pins
        self.init()
        pass
        
    def init(self):
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Set pins as output and input
        for pin in self._pins:
            GPIO.setup(pin,GPIO.OUT)  # Initial state as output
            pass
        
        # Set trigger to False (Low)
        for pin in self._pins:
           GPIO.output(pin, False)
            pass

        print "Waiting For Sensor To Settle"
        time.sleep(2)
        pass
        
    def get_measures(self):
        array = []
        for pin in self._pins:
            GPIO.output(pin, False)
            array.append(pin)
            pass
        return tuple(array)
        
    def get_measure_single(PIN):
    
        # This function measures a distance
        # Pulse the trigger/echo line to initiate a measurement
        GPIO.setup(PIN,GPIO.OUT)  # Initial state as output
        GPIO.output(PIN, True)
        time.sleep(0.00001)
        GPIO.output(PIN, False)
        #ensure start time is set in case of very quick return
        start = time.time()

        # set line to input to check for start of echo response
        GPIO.setup(PIN, GPIO.IN)
        while GPIO.input(PIN)==0:
            start = time.time()
            
        # Wait for end of echo response
        while GPIO.input(PIN)==1:
            stop = time.time()
  
        elapsed = stop-start
        distance = elapsed * 17150
        return distance
        pass

