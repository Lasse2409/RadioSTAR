# check howizontal coordinates of now, convert to galactic coordinates, and convert back to horizontal coordinates, check if above horizon. 
#import matplotlib.pyplot as plt
#import numpy as np
#from astropy.time import Time
#from datetime import datetime
import time
from rtlsdr import *
from pylab import *
from datetime import datetime
import os

from src.Coordinate_transforms import coordinates
from src.rotor import rotor
from src.utilities import utilities




### Global setup
observer = [55.3959, 10.3883, 17] #define location of observer [altitude, latitude, longitude]
dateAndTime = [2023, 5, 1, 16, 0, 0] #defining date and time [year, month, day, hour, minute, second]
rtlSDRSetup = [256*1024*31, 2.4e6, 1420e6, 49.6, "data/single/singleData-"] #defining data collection parameters for rtlSDR [samples, sampleRate, centerFreq, gain, filePathName] 


### Defining coordinates to be tracked
targetCoordinateSystem = 0 #declaring which coordinate system is used in taget coordinates (0-> horizontal, 1-> galactic(longitude,latitude), 2-> equatorial)
target = np.array([240 + 0/60, 50 + 0/60]) #setting target coordinates 


### Initializeing seriel connection to rotor and turning on bias tee
R = rotor("192.168.1.104", 23)
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")


### Initialize the self variables in utilities
u = utilities(rtlSDRSetup, dateAndTime, observer, R)


### Store the measured coordinates in all coordinate systems (horizontal, galactic and equatorial)
measuredCoordinates = u.measurementCoordinates(targetCoordinateSystem, target)


### Create header for data file (time, coordinates and sdr settings)
header = u.makeHeader(measuredCoordinates)


### Make sure that we dont go below elevation limit
if measuredCoordinates[0][1] < 0:
    os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
    print("Tool low elevation (<0)")
    exit()


### Go to target this one we want to loop over and repeatedly update while data is being collected
print(f"Going to: {measuredCoordinates[0]}")
R.set(utilities.fullRotationLimit(target)[0] + utilities.azElOffset()[0], utilities.fullRotationLimit(target)[1] + utilities.azElOffset()[1])


### Collect data run all the time, the slow one governing how long to loop the tracking
u.rtlSample(1, header) #max samples is 256*1024*31


### Get coordinate status, turn pff bias tee and finish
R.status()
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
print("Done!")





