import RTIMU
import picamera, checkbattery, checkdisk, whereisthesun
import os
import math
import logging
import datetime
import time
import RPi.GPIO as GPIO
from compoundpi.client import CompoundPiClient


switchGPIO = 24
triggerGPIO = 23
network = '128.83.0.0/16' #IP range for pis connected to network
stacksize = 10 #number of images to grab in each stack
lat = "27:36:20.80:N" #approximate lattitude, you could have a gps output this directly, but this project is aimed for underwater use (no GPS)
lon = "95:45:20.00:W" #approximate longitude
memthreshold = 2000 #memmory threshold, in kbs

##trigger and switch inputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP) # interrupt
GPIO.setup(switchGPIO, GPIO.IN) # switch

##IMU data log
datlog = logging.getLogger('IMUlog')
hdlr = logging.FileHandler('../log/IMUlog.log')
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s', "%H-%M-%S-%f")
hdlr.setFormatter(formatter)
datlog.addHandler(hdlr)
datlog.setLevel(logging.INFO)

## imu data, be sure to calibrate properly before using this for data collection (see: github.com/Richards-Tech/RTIMULib)
SETTINGS_FILE = "../../RTIMULib/Linux/python/tests/RTIMULib"
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

## cameras
cameraclient = CompoundPiClient()
cameraclient.servers.network = network
cameraclient.servers.find(2) #should return 2 cameras
cameraclient.resolution(1920, 1080)
cameraclient.identify() #simultaneous blinking camera lights = ready to go


## disk check and sun data
sun = whereisthesun.App(lat, lon)
disk = checkdisk.App()
# check that there is enough disk space, compress data if space is low
# use IMU data to determine orientation relative to sun and send signal to indicator LEDS
#print sunalt
#print sunaz


while True:
    #availmem, usedmem, totatl = disk.checkds(memthreshold)
    try:
        GPIO.wait_for_edge(triggerGPIO, GPIO.FALLING)
        cameraclient.record(5) #record synchronized image stack
        cameraclient.record(10) #record synchronized video
        data = imu.getIMUData()
        intosun, awayfromsun, horizontal, sunalt, sunaz = sun.checkkeyaxes(data)
        sun.callleds(intosun, awayfromsun, horizontal)
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = temp.pressureRead()
        fusionPose = data["fusionPose"]
        logging.info('IMU:'+str(fusionPose))
        time.sleep(poll_interval*1.0/1000.0)

    except KeyboardInterrupt:
        cameraclient.list()
        cameraclient.close()
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit


cameraclient.close()
GPIO.cleanup()
