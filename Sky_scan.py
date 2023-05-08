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


#azOffset = 222.8
#elOffset = 1

azOffset = 0
elOffset  = 0

N = 20
az_start = 160
az_stop = 250

el_start = 10
el_stop = 50

alt = 17.
lat = 55.367511
lon = 10.431889

year = 2023
month = 5
day = 1
hour = 16
minute = 0
second = 0

sky_horizontal = utilities.skyBox(N, [az_start, az_stop],[el_start, el_stop])
sky_galactic = np.transpose(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, sky_horizontal[:,0], sky_horizontal[:,1], now = True))

sky_horizontal_measured = np.zeros((np.shape(sky_horizontal)))

print(np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, sky_galactic[0,0], sky_galactic[0,1], now = True)))

R = rotor("192.168.1.104", 23)

os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 1")

for idx in range(len(sky_galactic[:, 0])):
    sky_horizontal_measured[idx, :] = np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, sky_galactic[idx,0], sky_galactic[idx,1], now = True))
    print("Going to: (" + str(sky_horizontal_measured[idx, 0]) + ", " + str(sky_horizontal_measured[idx, 1]) + ")")
    R.set(sky_horizontal_measured[idx, 0] - azOffset, sky_horizontal_measured[idx, 1] - elOffset)


    header = []
    header.append("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    header.append("#Latitude: " + str(lat) + "\n")
    header.append("#Longitude: " + str(lon) + "\n")
    header.append("#Altitude: " + str(alt) + "\n")
    header.append("#Az: " + str(measured_horizontal[idx, 0]) + "\n")
    header.append("#El: " + str(measured_horizontal[idx, 1]) + "\n")
    header.append("#Galactic latitude: " + str(measured_galactic[idx, 0]) + "\n")
    header.append("#Galactic longitude: " + str(measured_galactic[idx, 1]) + "\n")
    header.append("#RA: " + str(measured_equatorial[idx, 0]) + "\n")
    header.append("#Dec: " + str(measured_equatorial[idx, 1]) + "\n")

    utilities.rtlSample(256*1024*4, 2.4e6, 1420e6, 123, header)

    """
    sdr = RtlSdr()

    sdr.sample_rate = 2.4e6
    sdr.center_freq = 1420e6
    sdr.gain = 49.6

    samples = sdr.read_samples(256*1024*4)
    sdr.close()

    f = open("data/data-" + str(idx) + ".dat", "w")
    f.write("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    f.write("#Latitude: " + str(lat) + "\n")
    f.write("#Longitude: " + str(lon) + "\n")
    f.write("#Altitude: " + str(alt) + "\n")
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
    """

os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")

print("Done!")