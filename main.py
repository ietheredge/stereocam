import camera, checkdisk, checkbattery, RTIMU
import multiprocessing
import math

logging.basicConfig(filename='../log/divelog.log', level=logging.DEBUG)



logging.info('IMU Name: ' + imu.IMUName())

SETTINGS_FILE = "RTIMULib"
if not os.path.exists(SETTINGS_FILE + ".ini"):
    logging.debug('Settings file does not exist, will be created')

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
if (not imu.IMUInit()):
    logging.warning('IMU Init Failed')
else:
    logging.info('IMU Init Succeeded')
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)


kamera = camera.App('yuv', 'yuv' '1920x1080', 'sports', '30', '1', 'outfile')


if imu.IMURead():
# x, y, z = imu.getFusionData()
# print("%f %f %f" % (x,y,z))
data = imu.getIMUData()
logging.info(data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure$
fusionPose = data["fusionPose"]
print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),
    math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
if (data["pressureValid"]):
    print("Pressure: %f, height above sea level: %f" % (data["pressure"], computeHeight(data["press$
if (data["temperatureValid"]):
    print("Temperature: %f" % (data["temperature"]))

queue = multiprocessing.Queue()

