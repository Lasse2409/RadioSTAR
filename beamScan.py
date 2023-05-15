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

### Function that returns a list with all header content
def makeHeader():
    header = []
    header.append("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    header.append("#Latitude: " + str(observer[0]) + "\n")
    header.append("#Longitude: " + str(observer[1]) + "\n")
    header.append("#Altitude: " + str(observer[2]) + "\n")
    header.append("#Az: " + str(measuredCoordinateHorizontal[0]) + "\n")
    header.append("#El: " + str(measuredCoordinateHorizontal[1]) + "\n")
    header.append("#Galactic latitude: " + str(measuredCoordinateGalactic[0]) + "\n")
    header.append("#Galactic longitude: " + str(measuredCoordinateGalactic[1]) + "\n")
    header.append("#RA: " + str(measuredCoordinateEquatorial[0]) + "\n")
    header.append("#Dec: " + str(measuredCoordinateEquatorial[1]) + "\n")
    header.append("#rtl_samples: " + str(rtlSDRSetup[0]) + "\n")
    header.append("#rtl_sampleRate: " + str(rtlSDRSetup[1]) + "\n")
    header.append("#rtl_centerFreq: " + str(rtlSDRSetup[2]) + "\n")
    header.append("#rtl_gain: " + str(rtlSDRSetup[3]) + "\n")    
    
    return header




### Global setup
numMeasurements = 15
angIncroment = 1
azElOffset = [231.4 + 10, -1 + 5] #offset for Az and El calibration 
observer = [55.3959, 10.3883, 17] #define location of observer [altitude, latitude, longitude]
dateAndTime = [2023, 5, 1, 16, 0, 0] #defining date and time [year, month, day, hour, minute, second]
rtlSDRSetup = [256*1024*31, 2.4e6, 1420e6, 49.6, "data/pointing/pointingData-"] #defining data collection parameters for rtlSDR [samples, sampleRate, centerFreq, gain, filePathName] 


### Initializeing seriel connection to rotor and turning on bias tee
R = rotor("192.168.1.104", 23)
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")



sun = coordinates.getSun(dateAndTime, observer, now=True)

print("Going to target: " + str(sun))

if sun[0] > 180:
    setAz = -(360-sun[0])
else:
    setAz = sun[0]

R.set(setAz + azElOffset[0], sun[1] + azElOffset[1])
R.status()

time.sleep(2)

### scanning azimuth
for idx in range(numMeasurements):
    rtlSDRSetup[4] = "data/pointing/pointingDataAz-"
    sun = coordinates.getSun(dateAndTime, observer, now=True)

    ### Make target azimuth offset
    target = [(sun[0]-0.5*(numMeasurements-1)*angIncroment) + idx*angIncroment, sun[1]]

    ### Store the measured coordinates in all coordinate systems (horizontal, galactic and equatorial)
    measuredCoordinateHorizontal = measurementCoordinates(0, target)[0]
    measuredCoordinateGalactic = measurementCoordinates(0, target)[1]
    measuredCoordinateEquatorial = measurementCoordinates(0, target)[2]

    ### Make sure that we dont go below elevation limit
    if measuredCoordinateHorizontal[1] < 0:
        print('Tool low elevation (<0)')
        os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
        exit()


    ### Create header for data file (time, coordinates and sdr settings)
    header = makeHeader()

    ### Go to target this one we want to loop over and repeatedly update while data is being collected
    print("Going to: (" + str(measuredCoordinateHorizontal[0]) + ", " + str(measuredCoordinateHorizontal[1]) + ")")

    if measuredCoordinateHorizontal[0] > 180:
        setAz = -(360-measuredCoordinateHorizontal[0])
    else:
        setAz = measuredCoordinateHorizontal[0]

    R.set(setAz + azElOffset[0], measuredCoordinateHorizontal[1] + azElOffset[1])
    R.status()

    ### Collect data 
    time.sleep(2)
    print("Measuring data...")
    utilities.rtlSample(rtlSDRSetup, idx, header) #max samples is 256*1024*31



### scanning azimuth
for idx in range(numMeasurements):
    rtlSDRSetup[4] = "data/pointing/pointingDataEl-"
    sun = coordinates.getSun(dateAndTime, observer, now=True)

    ### Make target azimuth offset
    target = [sun[0], (sun[1]-0.5*(numMeasurements-1)*angIncroment) + idx*angIncroment]

    ### Store the measured coordinates in all coordinate systems (horizontal, galactic and equatorial)
    measuredCoordinateHorizontal = measurementCoordinates(0, target)[0]
    measuredCoordinateGalactic = measurementCoordinates(0, target)[1]
    measuredCoordinateEquatorial = measurementCoordinates(0, target)[2]

    ### Make sure that we dont go below elevation limit
    if measuredCoordinateHorizontal[1] < 0:
        print('Tool low elevation (<0)')
        os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
        exit()


    ### Create header for data file (time, coordinates and sdr settings)
    header = makeHeader()

    ### Go to target this one we want to loop over and repeatedly update while data is being collected
    print("Going to: (" + str(measuredCoordinateHorizontal[0]) + ", " + str(measuredCoordinateHorizontal[1]) + ")")

    if measuredCoordinateHorizontal[0] > 180:
        setAz = -(360-measuredCoordinateHorizontal[0])
    else:
        setAz = measuredCoordinateHorizontal[0]

    R.set(setAz + azElOffset[0], measuredCoordinateHorizontal[1] + azElOffset[1])
    R.status()
    


    ### Collect data 
    time.sleep(2)
    print("Measuring data...")
    utilities.rtlSample(rtlSDRSetup, idx, header) #max samples is 256*1024*31




R.status()
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
print("Done!")




    


    


