__author__ = 'ian'
#draws from example in RTIMULIB (Richards tech)

import sys, getopt
sys.path.append('.')

import logging
import os.path
import time
import math
import RTIMU



SETTINGS_FILE = "RTIMULib"


print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  logging.debug('Settings file does not exist, will be created')

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
pressure = RTIMU.RTPressure(s)

logging.info('IMU Name: ' + imu.IMUName())

if (not imu.IMUInit()):
    logging.warning('IMU Init Failed')
    sys.exit(1)
else:
    logging.info('IMU Init Succeeded')

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
logging.info('Recommended Poll Interval: %dmS' % poll_interval)

while True:
  if imu.IMURead():
    # x, y, z = imu.getFusionData()
    # print("%f %f %f" % (x,y,z))
    data = imu.getIMUData()
    (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure$
    fusionPose = data["fusionPose"]
    print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),
        math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
    if (data["pressureValid"]):
        print("Pressure: %f, height above sea level: %f" % (data["pressure"], computeHeight(data["press$
    if (data["temperatureValid"]):
        print("Temperature: %f" % (data["temperature"]))
    time.sleep(poll_interval*1.0/1000.0)
