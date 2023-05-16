"""
from datetime import datetime
from astropy.time import Time
from astropy.coordinates import get_sun
from astropy.coordinates import EarthLocation, AltAz
import astropy.units as u

# Define the location on Earth (latitude, longitude, elevation in meters)
location = EarthLocation(lat=55.3959*u.deg, lon=-10.3883*u.deg, height=0*u.m)

while True:
    # Get the current time
    current_time = Time(datetime.utcnow())

    # Get the Sun's position in Altitude-Azimuth coordinates at the current time and location
    sun_altaz = get_sun(current_time).transform_to(AltAz(obstime=current_time, location=location))

    # Print the Sun's horizontal coordinates (altitude and azimuth) at the current time
    print(f"At {current_time}, the Sun's horizontal coordinates are: Altitude = {sun_altaz.alt}, Azimuth = {sun_altaz.az}")

    # Wait for one second before repeating
    time.sleep(1)











"""
from datetime import datetime
import time
from astropy.time import Time
from astropy.coordinates import get_sun
from astropy.coordinates import get_moon
from astropy.coordinates import get_icrs_coordinates
from astropy.coordinates import EarthLocation, AltAz
import astropy.units as u

from src.Coordinate_transforms import coordinates


observer = [55.3959, 10.3883, 17] #define location of observer [altitude, latitude, longitude]
dateAndTime = [2023, 5, 16, 18, 43, 0] #defining date and time [year, month, day, hour, minute, second]



objecta = coordinates.getObject('venus', dateAndTime, observer, now=True)
print(objecta)

