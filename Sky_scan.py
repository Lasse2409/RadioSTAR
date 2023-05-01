# check howizontal coordinates of now, convert to galactic coordinates, and convert back to horizontal coordinates, check if above horizon. 
import matplotlib.pyplot as plt
import numpy as np
from src.Coordinate_transforms import coordinates
from astropy.time import Time
from datetime import datetime

import time



N = 10


alt = 17.
lat = 55.367511
lon = 10.431889

year = 2023
month = 3
day = 2
hour = 19
minute = 5
second = 15

sky = np.zeros((N*N, 2))

az = np.linspace(0, 360, N)
el = np.linspace(0, 90, N)

for idx1, val1 in enumerate(az):
    for idx2, val2 in enumerate(el):  
        Sky[idx1*N + idx2, :] = np.array([val1,val2])


galactic = np.transpose(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, Sky[:,0], Sky[:,1], now = True))

#horizontal = np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, galactic[:,0], galactic[:,1], now = True))

#galactic = np.transpose(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, 0.2, 90, now = True))

#print(galactic)
#print(np.transpose(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, galactic[0], galactic[1], now = True)))
#print(coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, 20, 0, now = True))

#print(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, Sky[0,0], Sky[0,1], now = True))
#print(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, Sky[1,0], Sky[1,1], now = True))
#print(coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, Sky[2,0], Sky[2,1], now = True))


"""
galactic_l = coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, az, el, now = True)[0]
galactic_b = coordinates.Horizontal_to_galactic(year, month, day, hour, minute, second, lat, lon, alt, az, el, now = True)[1]

horizontal_fixed_az = coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, galactic_l, galactic_b, now = True)[0]
horizontal_fixed_el = coordinates.Galactic_to_horizontal(year, month, day, hour, minute, second, lat, lon, alt, galactic_l, galactic_b, now = True)[1]


for idx, val in enumerate(horizontal_fixed_az):
    print(val, horizontal_fixed_el[idx])
    time.sleep(0.1)
"""
