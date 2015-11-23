import ephem
import math

class App:

    def __init__(self, lat, long)
        self.ll =  [lat,  long]
        self.rig = ephem.Observer()
        if isinstance(ll[0], float):
            self.latitudeD = ll[0]
            self.longitudeD = ll[1]
        #print('Latitude: %f Longitude: %f'%(latitudeD, longitudeD))

        else:
            self.latitudeD, self.longitudeD = converttodecimal(ll)
        rig.lon = str(longitudeD)
        rig.lat = str(latitudeD)
        rig.elevation = 0
        #imutestdata = [(2*math.pi/180), (1*math.pi/180), ((240.48248682+180)*math.pi/180)]

    def converttodecimal(self, latlong):
        ltdeg, ltmin, ltsec, lthem = latlong[0].split(":")
        lndeg, lnmin, lnsec, lnhem = latlong[1].split(":")
        latitudeD = (1 if lthem=="N" else -1)*(float(ltdeg)+(float(ltmin)/60)+(float(ltsec)/3600))
        longitudeD = (1 if lnhem=="E" else -1)*(float(lndeg)+(float(lnmin)/60)+(float(lnsec)/3600))
        print('Latitude: %f Longitude: %f'%(latitudeD, longitudeD))
        return self.latitudeD, self.longitudeD

    def checkkeyaxes(self, imuread, rig=rig, precision=22.5):
        # precision in degrees,
        #i.e. +/- degrees from direction
        # roll, pitch, yaw should be adjusted to account for the orientation of the IMU
        s=ephem.Sun(rig)
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
        return intosun, awayfromsun, horizontal

    def callleds(self, f, a, h):
        if f:
            print True
        if a:
            print True
        if h:
            print True
