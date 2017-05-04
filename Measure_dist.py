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


def Measure_dist(GPIO_TRIGECHO23,GPIO_TRIGECHO24,GPIO_TRIGECHO25):

    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)
    
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

    distance1 = measure(GPIO_TRIGECHO23)
    distance2 = measure(GPIO_TRIGECHO24)
    distance3 = measure(GPIO_TRIGECHO25)
    return(distance1,distance2,distance3)

