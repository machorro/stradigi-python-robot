#!/usr/bin/python
import time

# Import the Robot.py file (must be in the same directory as this file!).
from Robot_Config import RobotConfig

robot_config = RobotConfig()

import Robot
from Measure_dist import Measure_dist
import RPi.GPIO as GPIO

# Telegram
import sys
import time
import telepot
from telepot.loop import MessageLoop
import apiai
import json

#from Measure_dist import Measure_init

from recognize_obstacle import *

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

##
## Telegram configs
CLIENT_ACCESS_TOKEN="083c4744cc654ecd937ca7912f81baf7"

look_obj = None

def telegram_handle(msg):
    print(msg)
    global look_obj
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    # if content_type == 'text':
    # bot.sendMessage(chat_id, msg['text'])
    msg_txt = msg['text']
    words = msg_txt.split(' ')
    # print(words[-1])

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.query = msg_txt
    response = request.getresponse()
    reply = response.read()
    reply = reply.decode("utf-8")
    print ('reply', reply)
    parsed_json = json.loads(reply)
    cmdLine = parsed_json['result']['resolvedQuery']
    print('cmdLine', cmdLine)

    args = cmdLine.split()
    print('args', args)

    if len(args) >= 2:
        if '/go_to' == args[0]:
            print('cmd=', 'go to')
            print('arg=', args[1])
            look_obj = args[1]
            pass
    print ('here')
    print(look_obj)
    bot.sendMessage(chat_id, ("I'll look for a " + str(look_obj) + "!"))
    pass # telegram_handle

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

# Main func
# Telegram init
bot = telepot.Bot("351373688:AAGVt6-abgby98JYSPuuNcl6axdOwrZggko")
print(bot.getMe())
MessageLoop(bot, telegram_handle).run_as_thread()
print ('Listening ...')

# The robot main function
try:
    #Measure_init(GPIO_TRIGECHO_RIGHT,GPIO_TRIGECHO_FRONT,GPIO_TRIGECHO_LEFT)
    print GPIO_TRIGECHO_RIGHT
    print GPIO_TRIGECHO_FRONT
    print GPIO_TRIGECHO_LEFT
    robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)
    robot.set_robot(robot_config)
    
    # initialize recognize_obstacle module
    recognize_obstacle_init()

    shouldStop = False

    print ("Main loop active")
    while True:
        if look_obj == None:
            # Do nothing
            continue;

        # robot moves formward only for 100 sec for now if no obstacle is on its way
        print("Get distance");
        distance_right, distance_front, distance_left = Measure_dist(GPIO_TRIGECHO_RIGHT,GPIO_TRIGECHO_FRONT,GPIO_TRIGECHO_LEFT)
        print("Done getting distance");
        
        # Always check front
        if (distance_front < dist_threshold):
            print ("Stopping and checking")
            robot.stop()
            
            # stop and turn; mark the turn
            # go to deeplearning function 
            #if the top prediction is X do the rest
            results=look_obj
            print("Looking around for " + results)
            for name in recognize_obstacle_process():
                print("Name = " + name)
                if results in name:
                    print("Will stop")
                    shouldStop= True
                    break
            if (shouldStop):
                break
            #else don't move
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
    
print("End of program")

