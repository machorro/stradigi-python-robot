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

import picamera
import time
import io
from PIL import Image
import picamera.array

# from models import *
# import models
# from models import

from object_detection.utils import label_map_util
# from models.object_detection.builders


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



sys.path.append("..")


# from utils import visualization_utils as vis_util

# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.

#
#take a picture with the camera and save it in PATH_TO_TEST_IMAGES_DIR with image{}.jpg format
PATH_TO_TEST_IMAGES_DIR = 'test_images'
def get_camera_image():
    print("Taking picture")
    image_name = PATH_TO_TEST_IMAGES_DIR+"/image1.jpeg"

    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        # camera.exposure_mode = 'off'
        # camera.awb_mode = 'off'
        camera.start_preview()
        time.sleep(1)
        camera.capture(stream, format='jpeg')
        pass

    stream.seek(0)
    image = Image.open(stream)
    image.save(image_name, "JPEG")

    # img = skimage.img_as_float(image).astype(np.float32)
    print("Done taking picture")

#

get_camera_image()
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpeg'.format(i)) for i in range(1, 2) ]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


def learn_infrence(image_path):
    try:
        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:
              for _ in range(2):
                image = Image.open(image_path)
                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                image_np = load_image_into_numpy_array(image)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                print ('classes',classes)

        for i in range(len(scores[0])):
            print ('category', category_index[classes[0][i]]['name'])
            print ('score',scores[0][i])
            if category_index[classes[0][i]]['name'] == str(look_obj):
                print("looking for " + str(look_obj))
                sys.exit()

    except Exception as e:
      print(e)

    pass

while(1):
    try:
      print("Waiting...")
      #input()
      with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
          for _ in range(2):
            image_path=TEST_IMAGE_PATHS[0] #"/Users/normand/Documents/Processing/communicate/color.jpg"
            image = Image.open(image_path)
            # the array based representation of the image will be used later in order to prepare the
            # result image with boxes and labels on it.
            image_np = load_image_into_numpy_array(image)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            print ('classes',classes)

            # Visualization of the results of a detection.
            # vis_util.visualize_boxes_and_labels_on_image_array(
            #     image_np,
            #     np.squeeze(boxes),
            #     np.squeeze(classes).astype(np.int32),
            #     np.squeeze(scores),
            #     category_index,
            #     use_normalized_coordinates=True,
            #     line_thickness=8)
            # plt.figure(figsize=IMAGE_SIZE)
            # plt.imshow(image_np)
            #print(boxes)
            # imag = Image.fromarray(image_np, 'RGB')
           # imag.save('my.png')
           #  imag.show()
            #print(classes)
            #print(scores)
      middle_x=0
      for i in range(len(scores[0])):
          # if scores[0][i]>0.70:
            #  print(scores[0][i])
            #  print(category_index[classes[0][i]]['name'])
            #  print(boxes[0][i])
            print ('category', category_index[classes[0][i]]['name'])
            print ('score',scores[0][i])
            if category_index[classes[0][i]]['name'] == str(look_obj):
                print("looking for " + str(look_obj))
                sys.exit()

      #boxes= y,x normalized del top left, y,x del bottom right

      #middle_x=(boxes[0][i][1]*640+boxes[0][i][3]*640)/2

      #Write on file the x center of the box of the object you need
      # with open("/Users/normand/Desktop/center.txt", 'w') as file:
      #   file.write(str(int((middle_x-320)*0.8)))
    except Exception as e:
      print(e)

