import RTIMU
import picamera, checkbattery, checkdisk
import os
import math
import logging
import datetime
import time


lat = "27:36:20.80:N" #approximate lattitude, you could have a gps output this directly, but this project is aimed for underwater use (no GPS)
lon = "95:45:20.00:W" #approximate longitude
memthreshold = 2000 #memmory threshold, in kbs

## initialize imu data be sure to calibrate properly before using this for data collection (see: github.com/Richards-Tech/RTIMULib)
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

## initialize camera, battery check, disk check and sun data
camera = picamera.PiCamera()
battery = checkbattery.App()
sun = whereisthesun.App(lat, lon)
disk = checkdisk()

while True:
    availmem, usedmem, totatl = checkdisk.chkdsk(memthreshold) # check that there is enough disk space, compress data if space is low
    if battery.check(): # check battery level
        pass
    if imu.IMURead(): # read from calibrated IMU
        data = imu.getIMUData()
    intosun, awayfromsun, horizontal, sunalt, sunaz = sun.checkkeyaxes(data) # use IMU data to determine orientation relative to sun and send signal to indicator LEDS

    for i in range (1,10): # record data
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = temp.pressureRead()
        fusionPose = data["fusionPose"]
        camera.capture('../data/'+str(datetime.datetime.now().strftime('%H-%M-%S-%f'))+str("_%f" % data["temperature"])+str("_%f-%f-%f_%s_%f_%f" % (math.degrees(fusionPose[0]), math.degrees(fusionPose[1]),
                                        math.degrees(fusionPose[2])), ('I' if intosunx==True else 'A' if awayfromsun==True else 'P'), sunalt, sunaz)+'.jpg' , format='jpeg', bayer=True)
        time.sleep(poll_interval*1.0/1000.0)
