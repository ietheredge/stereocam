import ephem
import math

class App:

    def __init__(self, lat, lon)
        #self.ll =  [lat,  lon]
        self.rig = ephem.Observer()

        if isinstance(lat, float):
            self.latitudeD = lat
            self.longitudeD = lon
        else:
            self.latitudeD, self.longitudeD = converttodecimal(lat, lon)
        self.rig.lon = str(self.longitudeD)
        self.rig.lat = str(self.latitudeD)
        self.rig.elevation = 0
        #imutestdata = [(2*math.pi/180), (1*math.pi/180), ((240.48248682+180)*math.pi/180)]

    def converttodecimal(self, lat, lon):
        ltdeg, ltmin, ltsec, lthem = lat.split(":")
        lndeg, lnmin, lnsec, lnhem = lon.split(":")
        self.latitudeD = (1 if lthem=="N" else -1)*(float(ltdeg)+(float(ltmin)/60)+(float(ltsec)/3600))
        self.longitudeD = (1 if lnhem=="E" else -1)*(float(lndeg)+(float(lnmin)/60)+(float(lnsec)/3600))

    def checkkeyaxes(self, imuread, precision=22.5):
        # precision in degrees,
        #i.e. +/- degrees from direction
        # roll, pitch, yaw should be adjusted to account for the orientation of the IMU
        s=ephem.Sun(self.rig)
        sunalt = str(s.alt)
        sunaz = str(s.az)

        imuroll, imupitch, imuyaw = math.degrees(imuread[0]), math.degrees(imuread[1]),math.degrees(imuread[2]) # x, y, z
        altdeg, altmin, altsec = sunalt.split(":")
        azdeg, azmin, azsec = sunaz.split(":")
        azimuth = float(azdeg)+(float(azmin)/60)+(float(azsec)/3600)
        altitude = float(altdeg)+(float(altmin)/60)+(float(altsec)/3600)
        intosun = (True if (azimuth-precision)<=imuyaw<=(azimuth+precision) else False)
        awayfromsun = (True if ((azimuth-precision)+180)<=imuyaw<=((azimuth+precision)+180) or
                       ((azimuth-precision)-180)<=imuyaw<=((azimuth+precision)-180) else False)
        horizontal = (True if (-1*precision)<=imuroll<=precision and (-1*precision)<=imupitch<=precision else False)
        inlinewithsun = (True if (altitude-precision)<=imupitch<=(altitude+precision) else False)
        callleds(intosun, awayfromsun, horizontal)
        return intosun, awayfromsun, horizontal

    def callleds(self, its, afs, h):
        if its:
            print True
        if afs:
            print True
        if h:
            print True

if '__name__' == '__main__':
    lat = "27:36:20.80:N"
    lon = "95:45:20.00:W"
    sunloc = App(lat, lon)
