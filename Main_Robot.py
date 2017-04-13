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
GPIO_TRIGECHO23 = robot_config._pin_sonar0
GPIO_TRIGECHO24 = robot_config._pin_sonar1
GPIO_TRIGECHO25 = robot_config._pin_sonar2

dist = 40 

try:
    Measure_init(GPIO_TRIGECHO23,GPIO_TRIGECHO24,GPIO_TRIGECHO25)
    robot = Robot2.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)
    while True:
        # robot moves formward only for 100 sec for now if no obstacle is on its way
        print "after"
        distance1, distance2, distance3 = Measure_dist(GPIO_TRIGECHO23,GPIO_TRIGECHO24,GPIO_TRIGECHO25)
        print distance1
        print distance2
        print distance3
        # when either of distances is less than 10 cm, robot stops
        if distance1<dist or distance2<dist or distance3<dist :
            robot.stop()
            print "I should stop!"
            break

        robot.forward(255, None)
        pass

        
except KeyboardInterrupt:
    GPIO.cleanup()

