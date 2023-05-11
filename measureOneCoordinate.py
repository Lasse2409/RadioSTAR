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

def measurements(coordinate, target):
    if coordinate == 0:
        measured_horizontal = target
        measured_galactic = np.transpose(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, target[0], target[1], now = True))
        measured_equatorial = np.transpose(coordinates.Horizontal_to_equatorial(year, month, day, hour, minute, second, lat, lon, alt, target[0], target[1], now = True))
        
    elif coordinate == 1:
        measured_horizontal = np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, target[0], target[1], now = True))
        measured_galactic = target
        measured_equatorial = np.transpose(coordinates.Galactic_to_equatorial(target[0], target[1]))
    elif coordinate == 2:
        measured_horizontal = np.transpose(coordinates.Equatorial_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, target[0], target[1], now = True))
        measured_galactic = np.transpose(coordinates.Equatorial_to_galactic(target[0], target[1]))
        measured_equatorial = target
    else:
        print('wrong coordinate sys')
        exit()
    
    return measured_horizontal, measured_galactic, measured_equatorial





azOffset = 222.8
elOffset = 1

alt = 17.
lat = 55.367511
lon = 10.431889

year = 2023
month = 5
day = 1
hour = 16
minute = 0
second = 0

filePathName = "data/single/singleData-"





coordinate = 1 #0-> horizontal, 1-> galactic(longitude,latitude), 2-> equatorial
target = np.array([124,27])

measured_horizontal = np.zeros(np.shape(target))
measured_equatorial = np.zeros(np.shape(target))
measured_galactic = np.zeros(np.shape(target))

R = rotor("192.168.1.104", 23)
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")


measured_horizontal, measured_galactic, measured_equatorial = measurements(coordinate, target)


header = []
header.append("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
header.append("#Latitude: " + str(lat) + "\n")
header.append("#Longitude: " + str(lon) + "\n")
header.append("#Altitude: " + str(alt) + "\n")
header.append("#Az: " + str(measured_horizontal[0]) + "\n")
header.append("#El: " + str(measured_horizontal[1]) + "\n")
header.append("#Galactic latitude: " + str(measured_galactic[0]) + "\n")
header.append("#Galactic longitude: " + str(measured_galactic[1]) + "\n")
header.append("#RA: " + str(measured_equatorial[0]) + "\n")
header.append("#Dec: " + str(measured_equatorial[1]) + "\n")

if measured_horizontal[1] < 10:
    print('Tool low elevation (<10)')
    os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
    exit()

print("Going to: (" + str(measured_horizontal[0]) + ", " + str(measured_horizontal[1]) + ")")
R.set(measured_horizontal[0] - azOffset, measured_horizontal[1] + elOffset)





utilities.rtlSample(256*1024*4, 2.4e6, 1420e6, 49.6, filePathName, 1, header)

R.status()
print("Measuring data...")

os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")

print("Done!")





