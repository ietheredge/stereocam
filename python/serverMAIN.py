import RTIMU
import checkbattery, checkdisk, whereisthesun, softreset
import os
import math
import logging
import datetime
import time
import RPi.GPIO as GPIO
import io

# waitfor pi function
def sendpisignal(GPIOPINNo, wait):
    GPIO.setup(GPIOPINNo, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

## variables defined
wait = True
GPIO.setmode(GPIO.BCM)
pi2piGPIO = 24
lat = "27:36:20.80:N" #approximate lattitude, you could have a gps output this directly, but this project is aimed for underwater use (no GPS)
lon = "95:45:20.00:W" #approximate longitude
memthreshold = 2000 #memmory threshold, in kbs

sendpisignal(pi2piGPIO, wait)
os.chdir('/')
## data log
datlog = logging.getLogger('IMUlog')
hdlr = logging.FileHandler('home/pi/imageIMUSync/log/IMUlog.log')
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s', "%H-%M-%S-%f")
hdlr.setFormatter(formatter)
datlog.addHandler(hdlr)
datlog.setLevel(logging.INFO)

## imu set up, be sure to calibrate properly before using this for data collection (see: github.com/Richards-Tech/RTIMULib)
SETTINGS_FILE = "home/pi/RTIMULib/Linux/python/tests/RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
if not os.path.exists(SETTINGS_FILE + ".ini"):
    print('Settings file does not exist, will be created')
imu = RTIMU.RTIMU(s)
temp = RTIMU.RTPressure(s)
if (not imu.IMUInit()):
    exit()
else:
    pass
imu.setSlerpPower(0.02) # set weighting of predicted vs. measured states
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
poll_interval = imu.IMUGetPollInterval()

## disk check and 0sun data
sun = whereisthesun.App(lat, lon)
disk = checkdisk.App()

## shutdown switch
down = softreset.App()
# check that there is enough disk space, compress data if space is low
# use IMU data to determine orientation relative to sun and send signal to indicator LEDS
#print sunalt
#print sunaz


while True:
        down.listen()
    #availmem, usedmem, totatl = disk.checkds(memthreshold)
        data = imu.getIMUData()
        intosun, awayfromsun, horizontal, sunalt, sunaz = sun.checkkeyaxes(data)
        sun.callleds(intosun, awayfromsun, horizontal)
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = temp.pressureRead()
        fusionPose = data["fusionPose"]
        datlog.info("r: %f p: %f y: %f quadrant: %s solarangle: %f, %f" % (math.degrees(fusionPose[0]), math.degrees(fusionPose[1]),
                                        math.degrees(fusionPose[2]), ('into sun' if intosun==True else 'away from sun' if awayfromsun==True else 'perpendicular to sun'), sunalt, sunaz))

GPIO.cleanup()
exit()
