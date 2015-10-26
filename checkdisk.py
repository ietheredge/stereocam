import argparse
import os
import time

class App():

    def __init__(self, thresh):
        self.thresh  = thresh
        pass

    def checkds(self):
        stats = os.statvfs('/')
        avail = stats.f_bavail * stats.f_frsize
        total = stats.f_blocks * stats.f_frsize
        used = (stats.f_blocks - stats.f_bfree) * stats.f_frsize
        if avail <= self.thresh:
            App.compressdir(self)
            return avail, used, total
        else:
            return avail, used, total

    def compressdir(self):
        import zipfile
        zipf = zipfile.ZipFile('/tmp/%s.zip' % str(time.asctime(time.localtime(time.time()))))
        for root, dirs in os.walk('/data'):
            for dirs in root:
                zipf.write(os.path.join(root,dirs))


if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-ct", "--critthresh", help="critical threshold in MBs")
    args = vars(ap.parse_args())

    chkdsk = App(args["critthresh"])
    availds = chkdsk.checkds()


