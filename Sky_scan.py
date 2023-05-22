# check howizontal coordinates of now, convert to galactic coordinates, and convert back to horizontal coordinates, check if above horizon. 
import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time
from datetime import datetime
import time
from rtlsdr import *
from pylab import *
import os

from src.Coordinate_transforms import coordinates
from src.rotor import rotor
from src.utilities import utilities



gridSize = 10
azLimits = [210, 220]
elLimits = [70, 80]

observer = [55.3959, 10.3883, 17] #define location of observer [altitude, latitude, longitude]
dateAndTime = [2023, 5, 1, 16, 0, 0] #defining date and time [year, month, day, hour, minute, second]
rtlSDRSetup = [256*1024*31, 2.4e6, 1420e6, 49.6, "data/maps/1/mapData"] #defining data collection parameters for rtlSDR [samples, sampleRate, centerFreq, gain, filePathtargetName] 


### Initializeing seriel connection to rotor and turning on bias tee
R = rotor("192.168.1.104", 23)
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")


### Initialize the self variables in utilities
u = utilities(rtlSDRSetup, dateAndTime, observer, R)


### make the grid by calling function in utilities then transforming to galactic coordinates as the pseudostationary coordinates 
gridHorizontal = u.skyBox(gridSize, azLimits, elLimits)
gridGalactic = np.transpose(coordinates.Horizontal_to_galactic(dateAndTime, observer, gridHorizontal[:,0], gridHorizontal[:,1], now = True))


### Start scanning the sky 
u.skyScan(gridGalactic)
    

os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
print("Done!")
