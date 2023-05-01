# check howizontal coordinates of now, convert to galactic coordinates, and convert back to horizontal coordinates, check if above horizon. 
import matplotlib.pyplot as plt
import numpy as np
from src.Coordinate_transforms import coordinates
from astropy.time import Time
from datetime import datetime

import time



def sky_box(N, AZ, EL):
    sky_horizontal = np.zeros((N*N, 2))

    az = np.linspace(AZ[0], AZ[1], N)
    el = np.linspace(EL[0], EL[1], N)

    for idx1, val1 in enumerate(az):
        for idx2, val2 in enumerate(el):  
            sky_horizontal[idx1*N + idx2, :] = np.array([val1,val2])
    return sky_horizontal



N = 10
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

for idx, val in enumerate(sky_horizontal): 
    sky_horizontal_measured[idx,:] = np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, sky_galactic[idx,0], sky_galactic[idx,1], now = True))
    print(sky_horizontal_measured[idx,:])
    time.sleep(1)






















#galactic = np.transpose(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, sky_horizontal[:,0], sky_horizontal[:,1], now = True))

#horizontal = np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, galactic[:,0], galactic[:,1], now = True))

#galactic = np.transpose(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, 0.2, 90, now = True))

#print(galactic)
#print(np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, galactic[0], galactic[1], now = True)))
#print(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, 20, 0, now = True))

#print(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, sky_horizontal[0,0], sky_horizontal[0,1], now = True))
#print(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, sky_horizontal[1,0], sky_horizontal[1,1], now = True))
#print(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, sky_horizontal[2,0], sky_horizontal[2,1], now = True))


"""
galactic_l = coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, az, el, now = True)[0]
galactic_b = coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, az, el, now = True)[1]

horizontal_fixed_az = coordinates.Galactic_to_horizÆÆontal(year, month, day, hour, minute, second, lat, lon, alt, galactic_l, galactic_b, now = True)[0]
horizontal_fixed_el = coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, galactic_l, galactic_b, now = True)[1]


for idx, val in enumerate(horizontal_fixed_az):
    print(val, horizontal_fixed_el[idx])
    time.sleep(0.1)
"""
