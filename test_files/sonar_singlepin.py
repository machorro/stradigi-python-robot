#!/usr/bin/python

# -----------------------
# Import required Python libraries
# -----------------------
import time
import RPi.GPIO as GPIO

# -----------------------
# Define some functions
# -----------------------

def measure(PIN):
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
GPIO_TRIGECHO23 = 23
GPIO_TRIGECHO24 = 24
GPIO_TRIGECHO25 = 25


# Set pins as output and input
GPIO.setup(GPIO_TRIGECHO23,GPIO.OUT)  # Initial state as output
GPIO.setup(GPIO_TRIGECHO24,GPIO.OUT)  # Initial state as output
GPIO.setup(GPIO_TRIGECHO25,GPIO.OUT)  # Initial state as output

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGECHO23, False)
GPIO.output(GPIO_TRIGECHO24, False)
GPIO.output(GPIO_TRIGECHO25, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
try:

  while True:

    distance1 = measure(GPIO_TRIGECHO23)
    #distance2 = measure(GPIO_TRIGECHO24)
    #distance3 = measure(GPIO_TRIGECHO25)
    print "  Distance1 : %.1f cm" % distance1
    #print "  Distance2 : %.1f cm" % distance2
    #print "  Distance3 : %.1f cm" % distance3
    time.sleep(1)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()
