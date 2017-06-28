#!/usr/bin/python
import time

# Import the Robot.py file (must be in the same directory as this file!).
from Robot_Config import RobotConfig

robot_config = RobotConfig()

import Robot2
from Measure_dist import Measure_dist
import RPi.GPIO as GPIO
#from Measure_dist import Measure_init

LEFT_TRIM   = robot_config._left_trim
RIGHT_TRIM  = robot_config._right_trim

# Define GPIO to use on Pi
GPIO_TRIGECHO_RIGHT = robot_config._pin_sonar0
GPIO_TRIGECHO_FRONT = robot_config._pin_sonar1
GPIO_TRIGECHO_LEFT = robot_config._pin_sonar2

#dist = 40
dist_threshold = robot_config._dist 
did_turn_right = False
did_turn_left = False

turn_start_timer = None
turn_end_timer = None

def turn_logic(turn_distance):
    global turn_start_timer
    global turn_end_timer
    
    if (turn_start_timer == None and turn_distance > dist_threshold):
        turn_start_timer = time.time()
        print("start hole timer")
    pass

    if (turn_start_timer != None and turn_distance <= dist_threshold):
        turn_end_timer = time.time()
        diff = turn_end_timer - turn_start_timer
        distance = diff * 0.3 * 100 # cm
        print("stop hole timer")
        if (distance >= 20 + 6):
            print("backward on the hole")
            robot.backward(100, diff/1.5)
            return True  
            # after traversing the whole we should reset
        pass
    pass
    robot.forward(100, None)
    return False
pass

def resetGlobalVariables():
    global did_turn_left
    did_turn_left = False
    global did_turn_right
    did_turn_right = False
    global turn_start_timer
    turn_start_timer = None
    global turn_end_timer
    turn_end_timer = None
pass

try:
    #Measure_init(GPIO_TRIGECHO_RIGHT,GPIO_TRIGECHO_FRONT,GPIO_TRIGECHO_LEFT)
    print GPIO_TRIGECHO_RIGHT
    print GPIO_TRIGECHO_FRONT
    print GPIO_TRIGECHO_LEFT
    robot = Robot2.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)
    robot.set_robot(robot_config)
    while True:
        # robot moves formward only for 100 sec for now if no obstacle is on its way
        distance_right, distance_front, distance_left = Measure_dist(GPIO_TRIGECHO_RIGHT,GPIO_TRIGECHO_FRONT,GPIO_TRIGECHO_LEFT)

        # Always check front
        if (distance_front < dist_threshold):
            # stop and turn; mark the turn
            if (distance_right < distance_left):
                print("turned left")
                robot.left_ang_90()
                did_turn_left = True
            else:
                print("turned right")
                robot.right_ang_90()
                did_turn_right = True
            continue
        pass
        
        if (did_turn_left):
            reset = turn_logic(distance_left)
            if reset:
                print("reset turn left")
                resetGlobalVariables()
                robot.right_ang_90()
            pass  
        pass

        # Did we turn?
        if (did_turn_right):
            reset = turn_logic(distance_left)
            if reset:
                print("reset turn right")
                resetGlobalVariables()
                robot.left_ang_90()
            pass
        pass

        # Else go forward
        robot.forward(100, None)
        pass

        
except KeyboardInterrupt:
    GPIO.cleanup()
