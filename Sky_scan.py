# check howizontal coordinates of now, convert to galactic coordinates, and convert back to horizontal coordinates, check if above horizon. 
import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time
from datetime import datetime
import time
from rtlsdr import *
from pylab import *
from datetime import datetime

from src.Coordinate_transforms import coordinates
from src.rotor import rotor

def sky_box(N, AZ, EL):
    sky_horizontal = np.zeros((N*N, 2))

    az = np.linspace(AZ[0], AZ[1], N)
    el = np.linspace(EL[0], EL[1], N)
    el_reversed = np.flip(el,0)

    for idx1 in range(len(az)):
        for idx2 in range(len(el)):  
            sky_horizontal[idx1*N + idx2, 0] = az[idx1]
            if idx1%2 == 0:
                sky_horizontal[idx1*N + idx2, 1] = el[idx2]
            else:
                sky_horizontal[idx1*N + idx2, 1] = el_reversed[idx2]

    return sky_horizontal

azOffset = 222.8
elOffset = 1

N = 4
az_start = 220
az_stop = 229

el_start = 50
el_stop = 59

alt = 17.
lat = 55.367511
lon = 10.431889

year = 2023
month = 5
day = 1
hour = 16
minute = 0
second = 0

sky_horizontal = sky_box(N, [az_start, az_stop],[el_start, el_stop])
sky_galactic = np.transpose(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, sky_horizontal[:,0], sky_horizontal[:,1], now = True))

sky_horizontal_measured = np.zeros((np.shape(sky_horizontal)))

print(np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, sky_galactic[0,0], sky_galactic[0,1], now = True)))

R = rotor("192.168.1.104", 23)

for idx in range(len(sky_galactic[:, 0])):
    sky_horizontal_measured[idx, :] = np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, sky_galactic[idx,0], sky_galactic[idx,1], now = True))
    print("Going to: (" + str(sky_horizontal_measured[idx, 0]) + ", " + str(sky_horizontal_measured[idx, 1]) + ")")
    R.set(sky_horizontal_measured[idx, 0] - azOffset, sky_horizontal_measured[idx, 1] - elOffset)

    sdr = RtlSdr()

    sdr.sample_rate = 2.4e6
    sdr.center_freq = 1420e6
    sdr.gain = 49.6

    samples = sdr.read_samples(256*1024)
    sdr.close()

    f = open("data/data-" + str(idx) + ".dat", "w")
    f.write("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    f.write("#Galactic latitude: " + str(sky_galactic[idx, 0]) + "\n")
    f.write("#Galactic longitude: " + str(sky_galactic[idx, 1]) + "\n")

    ps, freqs = psd(samples, NFFT=256, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

    for j in range(len(ps)):
        f.write(str(ps[j]) + ", " + str(freqs[j]) + "\n")

    f.close()

    R.status()
    print("Measuring data...")

print("Done!")