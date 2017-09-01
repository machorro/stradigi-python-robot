import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image


import sys
import time
import telepot
from telepot.loop import MessageLoop
import apiai
import json

CLIENT_ACCESS_TOKEN="083c4744cc654ecd937ca7912f81baf7"

look_obj=None

def handle(msg):
    print(msg)
    global look_obj
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    #if content_type == 'text':
        #bot.sendMessage(chat_id, msg['text'])
    msg_txt=msg['text']
    words=msg_txt.split(' ')
    #print(words[-1])

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.query = msg_txt
    response = request.getresponse()
    reply = response.read()
    reply = reply.decode("utf-8")
    print ('reply',reply)
    parsed_json = json.loads(reply)
    cmdLine = parsed_json['result']['resolvedQuery']
    print('cmdLine',cmdLine)
        
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
#     bot.sendMessage(chat_id, ("I'll look for a " + str(parameters['object']) + "!") )
    bot.sendMessage(chat_id, ("I'll look for a " + str(look_obj) + "!") )

#TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot("351373688:AAGVt6-abgby98JYSPuuNcl6axdOwrZggko")
print(bot.getMe())
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.


# This is needed to display the images.
#%matplotlib inline

while(1):
    try:
      #print("Waiting...")
      look_obj='person'
    except Exception as e:
      print(e)
