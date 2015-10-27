import python.checkdisk
import python.checkbattery
import RTIMU
from python import camera, checkbattery, checkdisk
import os
import math
import logging
import time



# '''
divelog = logging.getLogger('divelog')
hdlr = logging.FileHandler('../log/divelog.log')
formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s', "%H-%M-%S.%f")
hdlr.setFormatter(formatter)
divelog.addHandler(hdlr)
divelog.setLevel(logging.INFO)
# '''

SETTINGS_FILE = "../RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
if not os.path.exists(SETTINGS_FILE + ".ini"):
    divelog.info('Settings file does not exist, will be created')
imu = RTIMU.RTIMU(s)
temp = RTIMU.RTPressure(s)

logging.info('IMU Name: %s' % imu.IMUName())
if (not imu.IMUInit()):
    divelog.info('IMU Init Failed')
else:
    divelog.info('IMU Init Succeeded')
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
poll_interval = imu.IMUGetPollInterval()

kamera = camera.App('yuv', 'yuv', '1920x1080', 'sports', '30', '1', 'outfile')

for i in range (1,10):
    if imu.IMURead():
        kamera.capraw()
        data = imu.getIMUData()
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = temp.pressureRead()
        fusionPose = data["fusionPose"]
        divelog.info("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), math.degrees(fusionPose[1]),
                                        math.degrees(fusionPose[2])))
        if (data["temperatureValid"]):
            divelog.info("Temperature: %f" % (data["temperature"]))

    time.sleep(poll_interval*1.0/1000.0)
