#!/usr/bin/python
import time

from Robot_Config import RobotConfig
robot_config = RobotConfig()

import Robot
from Measure_dist import Measure_dist
import RPi.GPIO as GPIO

# Stup
LEFT_TRIM   = robot_config._left_trim
RIGHT_TRIM  = robot_config._right_trim
GPIO_TRIGECHO_RIGHT = robot_config._pin_sonar0
GPIO_TRIGECHO_FRONT = robot_config._pin_sonar1
GPIO_TRIGECHO_LEFT = robot_config._pin_sonar2


learn_rate = 0.0001
weights = [0.0018, 0.0017, 0.0019, 0.0011, 0.0013, 0.0012, 0.0011]

fr_p = 0.0
fc_p = 0.0
fl_p = 0.0

actual_reward = 0.0
predicted_reward = 0.0


def prediction_reward(array_x):
    total = 0.0

    for i in range(0, 7):
        total = total + array_x[i] * weights[i]
    pass

    return total
pass

def update_weights(actual_reward, predicted_reward, array_x):
    for i in range(0, 7):
        pDelta = (predicted_reward - actual_reward) * array_x[i]
        weights[i] = weights[i] - (learn_rate * pDelta)
    pass
pass

def receive_reward(right, left, center, isGoingForward):
    reward = 0.0
    if right < 12.0 and left < 12.0 and center < 12.0:
        reward -= 3.0
    elif right < 6.0 or left < 6.0 or center < 6.0:
        reward -= 2.0

    if isGoingForward:
        reward += 1
    else:
        reward += 0.65

    return reward
pass

# setup


# loop

def loop():
    global fr_p
    global fc_p
    global fl_p
    global learn_rate
    global weights
    global actual_reward
    global predicted_reward

    # Scale Distances
    # Use previous distances
    fr_s = fr_p / 10.0
    fc_s = fc_p / 10.0
    fl_s = fl_p / 10.0

    # Create Current State Representation
    # using prevoius loops distances
    # Notice indices 3,4 and 5 are left, forward, right.
    # final index is the bias unit.
    array_x = [fr_s, fc_s, fl_s, 1, 0, 0, 1]

    # what is predicted for left?
    left_prediction = prediction_reward(array_x)
    # re-encode state for forward
    array_x[3] = 0
    array_x[4] = 1

    # what is forward reward prediction?
    forward_prediction = prediction_reward(array_x)

    # re-encode state for right
    array_x[4] = 0
    array_x[5] = 1

    # what is right prediction?
    right_prediction =  prediction_reward(array_x)

    distance_right, distance_front, distance_left = Measure_dist(GPIO_TRIGECHO_RIGHT,GPIO_TRIGECHO_FRONT,GPIO_TRIGECHO_LEFT)
    fr_d = distance_right
    fm_d = distance_front
    fl_d = distance_left

    print("dist: right=" + str(fr_d) + ", front=" + str(fm_d) + ", left=" + str(fl_d))

    if predicted_reward > 1000  or  predicted_reward < -1000:
        print("Update rewards")
        for i in range(0,7):
            weights[i] = 0.0001 * 1
        pass
    pass

    print("Pred_reward = " + str(predicted_reward) + ", FP = " + str(forward_prediction) + ", LP = " + str(left_prediction) + ", RP = " + str(right_prediction))

    if forward_prediction > left_prediction  and  forward_prediction > right_prediction:
        #go forward
        robot.forward(100, None)

        predicted_reward = forward_prediction
        actual_reward = receive_reward(fr_d, fl_d, fm_d, True)
        array_x[3] = 0
        array_x[4] = 1
        array_x[5] = 0
    elif left_prediction > right_prediction:
        #go left
        print "Turn left"
        # robot.left_ang_90()
        robot.left(100, 1.2)

        predicted_reward = left_prediction
        actual_reward = receive_reward(fr_d, fl_d, fm_d, False)
        array_x[3] = 1
        array_x[4] = 0
        array_x[5] = 0
    elif forward_prediction == right_prediction  and  forward_prediction == left_prediction:
        #go forward
        robot.forward(100, None)

        predicted_reward = forward_prediction
        actual_reward = receive_reward(fr_d, fl_d, fm_d, True)
        array_x[3] = 0
        array_x[4] = 1
        array_x[5] = 0
    else:
        #go right
        print "Turn right"
        robot.right_ang_90()

        predicted_reward = right_prediction
        actual_reward = receive_reward(fr_d, fl_d, fm_d, False)
        array_x[3] = 0
        array_x[4] = 0
        array_x[5] = 1
    pass

    update_weights(actual_reward, predicted_reward, array_x)

    fr_p = fr_d
    fc_p = fm_d
    fl_p = fl_d
pass



# Main loop
try:
    #Measure_init(GPIO_TRIGECHO_RIGHT,GPIO_TRIGECHO_FRONT,GPIO_TRIGECHO_LEFT)
    print GPIO_TRIGECHO_RIGHT
    print GPIO_TRIGECHO_FRONT
    print GPIO_TRIGECHO_LEFT
    robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)
    robot.set_robot(robot_config)

    while True:
        loop()
        pass

except KeyboardInterrupt:
    GPIO.cleanup()

print("End of program")
