import time

# Import the Robot.py file (must be in the same directory as this file!).
from Robot_Config import RobotConfig
import Robot2
from Measure_dist import Measure_dist
from Measure_dist import Measure_init

robot_config = RobotConfig()

LEFT_TRIM   = robot_config._left_trim
RIGHT_TRIM  = robot_config._right_trim

# Define GPIO to use on Pi
GPIO_TRIGECHO_RIGHT = robot_config._pin_sonar0
GPIO_TRIGECHO_FRONT = robot_config._pin_sonar1
GPIO_TRIGECHO_LEFT = robot_config._pin_sonar2

#dist = 40
dist = robot_config._dist 
did_turn = False

try:
    Measure_init(GPIO_TRIGECHO_RIGHT,GPIO_TRIGECHO_FRONT,GPIO_TRIGECHO_LEFT)
    robot = Robot2.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)
    while True:
        # robot moves formward only for 100 sec for now if no obstacle is on its way
        print "after"
        distance_right, distance_front, distance_left = Measure_dist(GPIO_TRIGECHO_RIGHT,GPIO_TRIGECHO_FRONT,GPIO_TRIGECHO_LEFT)
        print distance1
        print distance2
        print distance3

        # first obstacle
        if (distance_front < dist):
            # stop and turn
            robot.right(200, 0.5)
            did_turn = True
            pass

        robot.forward(255, None)
        pass

        
except KeyboardInterrupt:
    GPIO.cleanup()

