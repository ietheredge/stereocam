import picamera
import logging
import argparse
import time
import io


class App:

    def __init__(self, imformat, itterations, outputfile):
        # setup log
        datlog = logging.getLogger('datalog')
        hdlr = logging.FileHandler('log/datalog.log')
        formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s', "%m/%d/%Y:%H:%M:%S.%f")
        hdlr.setFormatter(formatter)
        datlog.addHandler(hdlr)
        datlog.setLevel(logging.INFO)
        datlog.info("camera initiated stack n= ",str(itterations)," format= ",str(imformat)," output to=",str(outputfile))
        self.imformat = imformat
        self.n = itterations
        self.out = outputfile


    def capimage(self):
        pass

    def capimagestack(self):
        with picamera.PiCamera() as camera:
            time.sleep(2)
            camera.exposure_mode = 'sports'
            logging.info('camera exposure setting:'+str(camera.exposure_mode))
            logging.info('camera shutter speed:'+str(camera.shutter_speed))
            camera.capture_sequence((str(self.out),'_%04d.jpg' % i for i in range(self.n)), use_video_port=False)

    def capvideo(self):
        pass

    def capRAW(self):
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            time.sleep(2)
            camera.capture(stream, format='jpeg', bayer=True)

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

    kamera = App(args["format"],args["number"],args["output"])

    if args["image"]:
        if args["format"]=='RAW':
            kamera.capRAW()
        else:
            kamera.capimage()
    if args["video"]:
        kamera.capvideo()
    if args["stack"]:
        kamera.capimagestack()


