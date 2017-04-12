import RPi.GPIO as GPIO
from SonarMeasure import SonarMeasure

class TheBrain(object):
	# vars
	_sonar1 = None

	def __init__(self):
		GPIO.setmode(GPIO.BCM)

		self._sonar1 = SonarMeasure(23)
		pass # end constructor

	def run(self):
		print "Starting"
		while (True):
			print "Loop"
			sonar1Result = self._sonar1.doWork()
			if sonar1Result[0] == True:
				print sonar1Result[1]
				pass
			else:
				print "Waiting to settle"
				pass
			pass # end loop
		pass # end run	

	pass # end class

brain = TheBrain()
brain.run()
