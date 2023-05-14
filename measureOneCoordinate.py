# check howizontal coordinates of now, convert to galactic coordinates, and convert back to horizontal coordinates, check if above horizon. 
import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time
from datetime import datetime
import time
from rtlsdr import *
from pylab import *
from datetime import datetime
import os

from src.Coordinate_transforms import coordinates
from src.rotor import rotor

from src.utilities import utilities



### Given target coordinates (in given coordinate system targetCoordinateSystem 0-> horizontal, 1-> galactic(longitude,latitude), 2-> equatorial) provide coordinates in other coordinate systems as np.array
def measurementCoordinates(targetCoordinateSystem, target):

    measuredCoordinateHorizontal = np.zeros(np.shape(target))
    measuredCoordinateEquatorial = np.zeros(np.shape(target))
    measuredCoordinateGalactic = np.zeros(np.shape(target))
 
    if targetCoordinateSystem == 0:
        measuredCoordinateHorizontal = np.asarray(target)
        measuredCoordinateGalactic = np.transpose(coordinates.Horizontal_to_galactic(dateAndTime, observer, target[0], target[1], now = True))
        measuredCoordinateEquatorial = np.transpose(coordinates.Horizontal_to_equatorial(dateAndTime, observer, target[0], target[1], now = True))
        
    elif targetCoordinateSystem == 1:
        measuredCoordinateHorizontal = np.transpose(coordinates.Galactic_to_horizontal(dateAndTime, observer, target[0], target[1], now = True))
        measuredCoordinateGalactic = np.asarray(target)
        measuredCoordinateEquatorial = np.transpose(coordinates.Galactic_to_equatorial(target[0], target[1]))
    
    elif targetCoordinateSystem == 2:
        measuredCoordinateHorizontal = np.transpose(coordinates.Equatorial_to_horizontal(dateAndTime, observer, target[0], target[1], now = True))
        measuredCoordinateGalactic = np.transpose(coordinates.Equatorial_to_galactic(target[0], target[1]))
        measuredCoordinateEquatorial = np.asarray(target)
    
    else:
        print('wrong coordinate system specified')
        exit()
    
    return measuredCoordinateHorizontal, measuredCoordinateGalactic, measuredCoordinateEquatorial



def makeHeader():
    header = []
    header.append("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    header.append("#Latitude: " + str(lat) + "\n")
    header.append("#Longitude: " + str(lon) + "\n")
    header.append("#Altitude: " + str(alt) + "\n")
    header.append("#Az: " + str(measuredCoordinateHorizontal[0]) + "\n")
    header.append("#El: " + str(measuredCoordinateHorizontal[1]) + "\n")
    header.append("#Galactic latitude: " + str(measuredCoordinateGalactic[0]) + "\n")
    header.append("#Galactic longitude: " + str(measuredCoordinateGalactic[1]) + "\n")
    header.append("#RA: " + str(measuredCoordinateEquatorial[0]) + "\n")
    header.append("#Dec: " + str(measuredCoordinateEquatorial[1]) + "\n")
    header.append("#rtl_samples: " + str(samples) + "\n")
    header.append("#rtl_sampleRate: " + str(sampleRate) + "\n")
    header.append("#rtl_centerFreq: " + str(centerFreq) + "\n")
    header.append("#rtl_gain: " + str(gain) + "\n")    


### Global setup
azElOffset = [231.4, -1] #offset for Az and El calibration 
observer = [55.3959, 10.3883, 17] #define location of observer [altitude, latitude, longitude]
dateAndTime = [2023, 5, 1, 16, 0, 0] #defining date and time [year, month, day, hour, minute, second]
rtlSDRSetup = [256*1024*31, 2.4e6, 1420e6, 49.6, "data/single/singleData-", 1] #defining data collection parameters for rtlSDR [samples, sampleRate, centerFreq, gain, filePathName, dataFileExtension] 


### Defining coordinates to be tracked
targetCoordinateSystem = 0 #declaring which coordinate system is used in taget coordinates (0-> horizontal, 1-> galactic(longitude,latitude), 2-> equatorial)
target = np.array([0 + 0/60, 90 + 0/60]) #setting target coordinates 


### Initializeing seriel connection to rotor and turning on bias tee
R = rotor("192.168.1.104", 23)
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")


### Store the measured coordinates in all coordinate systems (horizontal, galactic and equatorial)
measuredCoordinateHorizontal = measurementCoordinates(targetCoordinateSystem, target)[0]
measuredCoordinateGalactic = measurementCoordinates(targetCoordinateSystem, target)[1]
measuredCoordinateEquatorial = measurementCoordinates(targetCoordinateSystem, target)[2]

### Create header for data file (time, coordinates and sdr settings)
makeHeader()



### Make sure that we dont go below elevation limit
if measuredCoordinateHorizontal[1] < 0:
    print('Tool low elevation (<0)')
    os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
    exit()



### Go to target 
print("Going to: (" + str(measuredCoordinateHorizontal[0]) + ", " + str(measuredCoordinateHorizontal[1]) + ")")
R.set(measuredCoordinateHorizontal[0] + azElOffset[0], measuredCoordinateHorizontal[1] + azElOffset[1])


### Collect data
utilities.rtlSample(rtlSDRSetup, header) #samples, sampleRate, centerFreq, gain, filePathName, dataFileExtension, header) #max samples is 256*1024*31


### Get coordinate status, turn pff bias tee and finish
R.status()
print("Measuring data...")
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
print("Done!")





