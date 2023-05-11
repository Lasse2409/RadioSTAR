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




def rtlSample(samples, sampleRate, centerFreq, gain, filePathName, dataFileExtension, header):
        sdr = RtlSdr()

        sdr.sample_rate = sampleRate
        sdr.center_freq = centerFreq
        sdr.gain = gain

        samples = sdr.read_samples(samples)
        sdr.close()

        f = open(filePathName + str(dataFileExtension) + ".dat", "w")
        
        for idx in range(len(header)):
            f.write(header[idx])

        """
        #makes header an input in function 
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
        """
        
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

target = [220,50]

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

header = []
header.append("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
header.append("#Latitude: " + str(lat) + "\n")
header.append("#Longitude: " + str(lon) + "\n")
header.append("#Altitude: " + str(alt) + "\n")
header.append("#Az: " + str(target[0]) + "\n")
header.append("#El: " + str(target[1]) + "\n")
#header.append("#Galactic latitude: " + str(measured_galactic[idx, 0]) + "\n")
#header.append("#Galactic longitude: " + str(measured_galactic[idx, 1]) + "\n")
#header.append("#RA: " + str(measured_equatorial[idx, 0]) + "\n")
#header.append("#Dec: " + str(measured_equatorial[idx, 1]) + "\n")

idx = 1

R = rotor("192.168.1.104", 23)
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")



print("Going to: (" + str(target[0]) + ", " + str(target[1]) + ")")
R.set(target[0] - azOffset, target[1] - elOffset)

rtlSample(256*1024*4, 2.4e6, 1420e6, 49.6, filePathName, idx, header)




os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")

print("Done!")





