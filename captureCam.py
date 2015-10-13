__author__ = 'ian'

import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1920,1080)
    camera.exposure_mode = 'sports'
    start = time.time()
    camera.capture_sequence((
        'img%04d.jpg' % i
        for i in range(10)
    ), use_video_port=False)

