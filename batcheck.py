import RPi.GPIO as GPIO
__version__ = "P16.1.0"
class App:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN)
        print 'pin 16: ',str(GPIO.input(16))

    def check(self):
        if GPIO.input(16):
            return True
        elif:
            return False

if __name__ == '__main__':
    app = App()
    app.check()
