import time
import RPi.GPIO as GPIO

class SonarMeasure(object):

	# keep variables
	_pin = None
	_startTime = None
	_dinstance = None # store for the future

	# Initialize with a pin number
	def __init__(self, pin):
		self._pin = pin

 		GPIO.setup(self._pin,GPIO.OUT)
  		GPIO.output(self._pin, True)
  		time.sleep(0.00001)
  		GPIO.output(self._pin, False)

		#ensure start time is set in case of very quick return
		self._startTime = time.time()

		# set line to input to check for start of echo response
		GPIO.setup(self._pin, GPIO.IN)
		pass # end constructor
		
	def doWork():
		# check if it settled
		if GPIO.input(self._pin)==0:
			self._startTime = time.time()
			pass

		# check if it calcualted
		# if YES - return appropriate tuple
		# if NO - return a tuple marked as `not ready'
		if GPIO.input(self._pin)==1:
			stop = time.time()
			elapsed = stop - self._startTime
			self._distance = elapsed * 17150
			return (True, self._distance)
			pass
		else:
			return (False, -1)
			pass

		pass # end doWork
	
	pass # end SonarMeasure

