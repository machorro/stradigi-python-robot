import picamera
import time

camera = picamera.PiCamera()
#camera.capture('image.jpg')

camera.start_recording("video.h264")
time.sleep(10)
camera.stop_recording()

