# coding=utf-8
import os
import re
import geo
#path to epw data
#default = ~/epw/
path = os.environ['HOME'] + "/epw/"

try:
    os.listdir(os.environ['HOME'] + '/epw')
except OSError:
    try:
        os.mkdir(os.environ['HOME'] + '/epw')
    except IOError:
        pass

def basename(USAF):
    files = os.listdir(path)
    for f in files:
        if f.find(USAF) is not -1:
            return f[0:f.rfind('.')]
def epwbasename(USAF):
    f = open('epwurls.csv')
    for line in f.readlines():
        if line.find(USAF) is not -1:
            return line.rstrip()

def downloadEPW(USAF):
    import os
    url = "http://apps1.eere.energy.gov/buildings/energyplus/weatherdata/4_north_and_central_america_wmo_region_4/1_usa/"
    import urllib2
    import zipfile
    epwfile = epwbasename(USAF)
    u = urllib2.urlopen(url + epwfile)
    localFile = open(path + epwfile, 'w')
    localFile.write(u.read())
    localFile.close()
    epw = zipfile.ZipFile(path + epwfile, 'r')
    epw.extractall(path)
    os.remove(path + epwfile)

def twopercent(USAF):
    #(DB=>MWB) 2%, MaxDB=
    temp = None
    try:
        fin = open('%s/%s.ddy' % (path,basename(USAF)))
        for line in fin:
            m = re.search('2%, MaxDB=(\d+\.\d*)',line)
            if m:
                temp = float(m.groups()[0])
    except:
        pass
    if not temp:
        #(DB=>MWB) 2%, MaxDB=
        try:
            fin = open('%s/%s.stat' % (path,basename(USAF)))
            flag = 0
            data = []
            for line in fin:
                if line.find('2%') is not -1:
                    flag = 3
                if flag > 0:
                    data.append(line.split('\t'))
                    flag -= 1
            temp = float(data[2][5].strip())
        except:
            pass
    return temp

def minimum(USAF):
    #(DB=>MWB) 2%, MaxDB=
    temp = None
    fin = None
    try:
        fin = open('%s/%s.ddy' % (path,basename(USAF)))
    except:
        print "File not found"
        print "Downloading ..."
        downloadEPW(USAF)
        fin = open('%s/%s.ddy' % (path,basename(USAF)))
    for line in fin:
        m = re.search('Max Drybulb=(-?\d+\.\d*)',line)
        if m:
            temp = float(m.groups()[0])
    if not temp:
        try:
            fin = open('%s/%s.stat' % (path,basename(USAF)))
            for line in fin:
                if line.find('Minimum Dry Bulb') is not -1:
                    return float(line[37:-1].split('\xb0')[0])
        except:
            pass
    return temp



if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description='Model a PV system. Currently displays annual output and graph')
    #import sys
    #opts, args = getopt.getopt(sys.argv[1:], 'f:h')
    parser.add_argument('-z', '--zipcode',type=int,required=True)
    parser.add_argument('-m', '--mname')
    parser.add_argument('-v', '--voltage',type=int,default=600)
    args = vars(parser.parse_args())
    #print args

    try:
        #start program
        zip = args['zipcode']
        maxVoltage = args['voltage']
        stationClass = 1
        name, usaf = geo.closestUSAF( geo.zipToCoordinates(zip), stationClass)
        print "%s USAF: %s" %  (name, usaf)
        print "Minimum Temperature: %s C" % minimum(usaf)
        print "2%% Max: %s C" % twopercent(usaf)
        import modules
        m = getattr(modules,args['mname'])()
        print "Minimum: %sV" % m.Vmin(twopercent(usaf))
        print "Maximum: %sV" % m.Vmax(minimum(usaf))
        print "Max in series", int(maxVoltage/m.Vmax(minimum(usaf)))


    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    except:
        raise