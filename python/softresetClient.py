import RPi.GPIO as GPIO
import time, sys
from subprocess import call

class App():
    def __call__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=App.shutitdown(self))

    def shutitdown(self):
        time.sleep(1.75)
        # send to halt state
        call(["sudo", "halt"])
        GPIO.cleanup()
        sys.exit()


if __name__ == '__main__':
    sudohalt = App()
    while True:
        sudohalt()
