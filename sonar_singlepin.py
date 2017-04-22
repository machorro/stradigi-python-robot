#!/usr/bin/python

# -----------------------
# Import required Python libraries
# -----------------------
import time
import RPi.GPIO as GPIO

# -----------------------
# Define some functions
# -----------------------

def measure():
  # This function measures a distance
  # Pulse the trigger/echo line to initiate a measurement
  GPIO.output(GPIO_TRIGECHO, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGECHO, False)
  #ensure start time is set in case of very quick return
  start = time.time()

  # set line to input to check for start of echo response
  GPIO.setup(GPIO_TRIGECHO, GPIO.IN)
  while GPIO.input(GPIO_TRIGECHO)==0:
    start = time.time()

  # Wait for end of echo response
  while GPIO.input(GPIO_TRIGECHO)==1:
    stop = time.time()
  
  #GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
  #GPIO.output(GPIO_TRIGECHO, False)

  elapsed = stop-start
  distance = elapsed * 17150
  return distance


# -----------------------
# Main Script
# -----------------------

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGECHO = 23


# Set pins as output and input
GPIO.setup(GPIO_TRIGECHO,GPIO.OUT)  # Initial state as output

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGECHO, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
try:

  while True:

    distance = measure()
    print "  Distance : %.1f cm" % distance
    time.sleep(1)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()