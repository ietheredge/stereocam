import picamera
import logging

class App:

    def __init__(self):
        batlog = logging.getLogger('lowbatlog')
        hdlr = logging.FileHandler('log/lowbatlog.log')
        formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s', "%m/%d/%Y:%H:%M:%S")
        hdlr.setFormatter(formatter)
        batlog.addHandler(hdlr)
        batlog.setLevel(logging.INFO)
        batlog.info("battery voltage drop detected")


    def capimagestack(self, format):
        camera.exposure_mode = 'sports'
            logging.info('camera exposure setting:'+str(camera.exposure_mode))
            logging.info('camera shutter speed:'+str(camera.shutter_speed))
            start = time.time()
            camera.capture_sequence((
                'img%04d.jpg' % i
                for i in range(30)
            ), use_video_port=False)


if __name__=='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--stack", help="capture image stack, takes no input", action='store_true')
    ap.add_argument("-v", "--video", help="capture video, takes no input", action='store_true')
    ap.add_argument("-i", "--image", help="capture single image, takes no input", action='store_true')
    ap.add_argument("-f", "--format", help="pass output file format")
    ap.add_argument("-n", "--number", help="pass number of output objects")
    ap.add_argument("-l", "--lenght", help="pass video length")
    ap.add_argument("-o", "--output", help="output file name")
    args = vars(ap.parse_args())
    kamera = App()
