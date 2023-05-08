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
        measured_horizontal[idx, :] = target[idx,:]
        measured_galactic[idx,:] = np.transpose(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, target[idx,0], target[idx,1], now = True))
        measured_equatorial[idx,:] = np.transpose(coordinates.Horizontal_to_equatorial(year, month, day, hour, minute, second, lat, lon, alt, target[idx,0], target[idx,1], now = True))
        
    elif coordinate == 1:
        measured_horizontal[idx, :] = np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, target[idx,0], target[idx,1], now = True))
        measured_galactic[idx,:] = target[idx,:]
        measured_equatorial[idx,:] = np.transpose(coordinates.Galactic_to_equatorial(target[idx,0], target[idx,1]))
    elif coordinate == 2:
        measured_horizontal[idx, :] = np.transpose(coordinates.Equatorial_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, target[idx,0], target[idx,1], now = True))
        measured_galactic[idx,:] = np.transpose(coordinates.Equatorial_to_galactic(target[idx,0], target[idx,1]))
        measured_equatorial[idx,:] = target[idx,:]
    else:
        exit()
    
    return measured_horizontal, measured_galactic, measured_equatorial

def rtlSample(samples, sampleRate, centerFreq, gain, dataFileExtension):
    sdr = RtlSdr()

    sdr.sample_rate = sampleRate
    sdr.center_freq = centerFreq
    sdr.gain = gain

    samples = sdr.read_samples(samples)
    sdr.close()

    f = open("data/single/singleData-" + str(dataFileExtension) + ".dat", "w")
    
    f.write("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    f.write("#Latitude: " + str(lat))
    f.write("#Longitude: " + str(lon))
    f.write("#Altitude: " + str(alt))
    f.write("#Az: " + str(measured_horizontal[idx, 0]) + "\n")
    f.write("#El: " + str(measured_horizontal[idx, 1]) + "\n")
    f.write("#Galactic latitude: " + str(measured_galactic[idx, 0]) + "\n")
    f.write("#Galactic longitude: " + str(measured_galactic[idx, 1]) + "\n")
    f.write("#RA: " + str(measured_equatorial[idx, 0]) + "\n")
    f.write("#Dec: " + str(measured_equatorial[idx, 1]) + "\n")

    ps, freqs = psd(samples, NFFT=256, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

    for j in range(len(ps)):
        f.write(str(ps[j]) + ", " + str(freqs[j]) + "\n")

    f.close()

    R.status()
    print("Measuring data...")







#azOffset = 222.8
#elOffset = 1

azOffset = 0
elOffset  = 0

coordinate = 0 #0-> horizontal, 1-> galactic, 2-> equatorial
target = np.array([[220,50], [220,50], [220,50], [220,50]])


alt = 17.
lat = 55.367511
lon = 10.431889

year = 2023
month = 5
day = 1
hour = 16
minute = 0
second = 0


measurement_horizontal = np.zeros((np.shape(target)))
measurement_galactic = np.zeros((np.shape(target)))
measurement_equatorial = np.zeros((np.shape(target)))

R = rotor("192.168.1.104", 23)
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")


for idx in range(len(target[:, 0])):
    
    measured_horizontal, measured_galactic, measured_equatorial = measurements(coordinate, target)

    print("Going to: (" + str(measured_horizontal[idx, 0]) + ", " + str(measured_horizontal[idx, 1]) + ")")
    R.set(measured_horizontal[idx, 0] - azOffset, measured_horizontal[idx, 1] - elOffset)

    rtlSample(256*1024*4, 2.4e6, 1420e6, 49.6, idx)

os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")

print("Done!")





