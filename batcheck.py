import RPi.GPIO as GPIO
import argparse


__version__ = "P16.1.0"


class App:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.IN)
        print 'pin 16: ', str(GPIO.input(16))

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
            batlog = logging.getLogger('lowbatlog')
            hdlr = logging.FileHandler('log/lowbatlog.log')
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            batlog.addHandler(hdlr)
            batlog.setLevel(logging.INFO)
            batlog.info("battery_voltage_drop_detected")

            while True:
                batlog.info("they_say_I_got_a_low_battery_but_I_ain't_dead_yet!")
                time.sleep(60)
        else:
            print 'battery must be low (have a significant drop in voltage) to start log.\n' \
                  '\trun $:python batcheck.py --calib to check every 5 minutes and create log on detection' \


    def retlowbatcal(self):
        import numpy as np
        import time

        lowtimes = np.array([])
        deadtimes = np.array([])

        for line in open('log/lowbatlog.log'):
            timestamp = time.strptime(line.split(" ")[0])
            msg = line.split(" ")[2]

            if msg == 'battery_voltage_drop_detected':
                lowtimes = np.append(lowtimes,timestamp)
                try:
                    deadtimes = np.append(deadtimes,prevts)
                except:
                    pass
            elif msg == "they_say_I_got_a_low_battery_but_I_ain't_dead_yet!":
                pass

            prevts = timestamp

        lowtimes.sort()
        deadtimes.sort()
        print np.average(deadtimes - lowtimes)
        return np.average(deadtimes - lowtimes)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--calib", help="run batcheck with calibration on", action='store_true')
    ap.add_argument("-r", "--readcal", help="returns the average battery reserve calibration", action='store_true')
    args = vars(ap.parse_args())
    batapp = App()
    batapp.check()

    if args["calib"]:
        import time
        print 'monitoring battery for voltage drop.'
        while True:
            time.sleep(300)
            if batapp.check():
                print 'battery voltage OK!'
                continue
            else:
                batapp.loglowbat()

    if args["readcal"]:
        batapp.retlowbatcal()
