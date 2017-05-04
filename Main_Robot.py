import time

# Import the Robot.py file (must be in the same directory as this file!).
import Robot2
from Measure_dist import Measure_dist


LEFT_TRIM   = 0
RIGHT_TRIM  = 0

# Define GPIO to use on Pi
GPIO_TRIGECHO23 = 23
GPIO_TRIGECHO24 = 24
GPIO_TRIGECHO25 = 25



try:
    while True:
        robot = Robot2.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)
        # robot moves formward only for 100 sec for now if no obstacle is on its way
        robot.forward(150, 100)
        distance1, distance2, distance3 = Measure_dist(GPIO_TRIGECHO23,GPIO_TRIGECHO24,GPIO_TRIGECHO25)
        # when either of distances is less than 10 cm, robot stops
        if distance1<10 or distance2<10 or distance3<10 :
            robot.stop()


        
except KeyboardInterrupt:
    GPIO.cleanup()

