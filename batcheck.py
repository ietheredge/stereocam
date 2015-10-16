import RPi.GPIO as GPIO
import argparse

__version__ = "P16.1.0"

class App:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.IN)
        print 'pin 16: ',str(GPIO.input(16))

    def check(self):
        if GPIO.input(16):
            print True
            return True
        else:
            print False
            return False

    def loglowbat(self):
        if not GPIO.input(16):
            import logging
            print 'battery voltage drop detected, starting log.'
            while True:
                batlog = logging.getLogger('%slowbatstillon.log' % time.strftime('%m%d%Y'))
                batlog.info("they say I got a low battery but I ain't dead yet!")
                time.sleep(60)
        else:
            print 'battery must be low (have a significant drop in voltage) to start log.\n' \
                  '\trun $:python batcheck.py --calib to check every 5 minutes and create log on detection'

    def retlowbatcal(self):
        pass #come back to this, parse log file(s) to find average time left when low battery

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c","--calib", help="run batcheck with calibration on", action='store_true')
    ap.add_argument("-r","--readcal", help="returns the average battery reserve calibration", action='store_true')
    args = vars(ap.parse_args())
    batapp = App()
    batapp.check()
    if args["calib"]:
        import time
        while True:
	    time.sleep(300)
            if batapp.check():
                print 'battery voltage OK'
                continue
            else:
                batapp.loglowbat()

    if args["readcal"]:
        batapp.retlowbatcal()
