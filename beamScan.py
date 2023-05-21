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



### Global setup
targetName = 'sun'
numMeasurements = 21
angIncroment = 1
observer = [55.3959, 10.3883, 17] #define location of observer [altitude, latitude, longitude]
dateAndTime = [2023, 5, 1, 16, 0, 0] #defining date and time [year, month, day, hour, minute, second]
rtlSDRSetup = [256*1024*31, 2.4e6, 1420e6, 49.6, "data/pointing/pointingData"] #defining data collection parameters for rtlSDR [samples, sampleRate, centerFreq, gain, filePathtargetName] 


### Initializeing seriel connection to rotor and turning on bias tee
R = rotor("192.168.1.104", 23)
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")


### Start by going to the center point of the object targetName given 
target = coordinates.getObject(targetName, dateAndTime, observer, now=True)
print("Going to target: " + str(target))
R.set(utilities.fullRotationLimit(target)[0] + utilities.azElOffset()[0], utilities.fullRotationLimit(target)[1] + utilities.azElOffset()[1])
R.status()
time.sleep(3)

### Initialize the self variables in utilities
u = utilities(rtlSDRSetup, dateAndTime, observer, R)


### scanning azimuth
u.lineScan("Az", targetName, numMeasurements, angIncroment)


### scanning azimuth
u.lineScan("El", targetName, numMeasurements, angIncroment)


### Check status and turn off bias tee
R.status()
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
print("Done!")




    


    

