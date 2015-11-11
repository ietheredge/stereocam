import RTIMU
import picamera, checkbattery, checkdisk
import os
import math
import logging
import datetime
import time

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
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
poll_interval = imu.IMUGetPollInterval()

camera = picamera.PiCamera()

for i in range (1,10):
    if imu.IMURead():
        data = imu.getIMUData()
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = temp.pressureRead()
        fusionPose = data["fusionPose"]
        camera.capture('../data/'+str(datetime.datetime.now().strftime('%H-%M-%S-%f'))+str("_%f" % data["temperature"])+str("_%f-%f-%f" % (math.degrees(fusionPose[0]), math.degrees(fusionPose[1]),
                                        math.degrees(fusionPose[2])))+'.jpg' , format='jpeg', bayer=True)
    time.sleep(poll_interval*1.0/1000.0)
