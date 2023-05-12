# https://docs.astropy.org/en/stable/generated/examples/coordinates/plot_obs-planning.html#sphx-glr-generated-examples-coordinates-plot-obs-planning-py
# https://docs.astropy.org/en/stable/coordinates/index.html
# https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord
# https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord
# https://docs.astropy.org/en/stable/coordinates/index.html
# https://learn.astropy.org/tutorials/2-Coordinates-Transforms  


from astropy import units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


class coordinates:

    def Equatorial_degrees(RA, DEC):
        ## Convert RA DEC to radians
        ra = (RA[0]*15 + RA[1]/4 + RA[2]/240)

        if DEC[0] > 0:
            dec = (DEC[0] + DEC[1]/60 + DEC[2]/3600)
        else:
            dec = (DEC[0] - DEC[1]/60 - DEC[2]/3600)
        return ra, dec


    def Equatorial_to_galactic(RA, DEC): # input RA, DEC

        c_icrs = SkyCoord(ra=RA*u.degree, dec=DEC*u.degree, frame='icrs') #International Celestial Reference System (ICRS) 
        c_galactic = c_icrs.galactic

        return c_galactic.l.degree, c_galactic.b.degree


    def Galactic_to_equatorial(L, B): # input galactic longitude l, galactic latitude b

        c_galactic = SkyCoord(frame="galactic", l=L*u.degree, b=B*u.degree)
        c_equatorial = c_galactic.transform_to('icrs')

        return c_equatorial.ra.degree, c_equatorial.dec.degree


    def Equatorial_to_horizontal(dateAndTime, observer, RA, DEC, now=True): #Time (manually or now=True gives current time) gps coordinates, altitude and equitorial coordinates
        observer = EarthLocation.from_geodetic(lat=observer[0]*u.deg, lon=observer[1]*u.deg, height=observer[2]*u.m) #Location converted to cartesian coordinates
        
        if now == True:
           time = datetime.utcnow()
        else:    
            time = str(dateAndTime[0]) + '-' + str(dateAndTime[1]) + '-' + str(dateAndTime[2]) + ' ' + str(hour) + ':' + str(dateAndTime[3]) + ':' + str(dateAndTime[4])
        time = Time(str(time)) 
        
        c_icrs = SkyCoord(ra=RA*u.degree, dec=DEC*u.degree, frame='icrs') #International Celestial Reference System (ICRS) 
        c_horizontal = c_icrs.transform_to(AltAz(obstime=time,location=observer))
        
        return c_horizontal.az.degree, c_horizontal.observer[2].degree


    def Horizontal_to_equatorial(dateAndTime, observer, AZ, EL, now=True): #Time (manually or now=True gives current time) gps coordinates, altitude and horizontal coordinates
        observer = EarthLocation.from_geodetic(lat=observer[0]*u.deg, lon=observer[1]*u.deg, height=observer[2]*u.m) 
        
        if now == True:
           time = datetime.utcnow()
        else:    
            time = str(dateAndTime[0]) + '-' + str(dateAndTime[1]) + '-' + str(dateAndTime[2]) + ' ' + str(hour) + ':' + str(dateAndTime[3]) + ':' + str(dateAndTime[4])
        time = Time(str(time))
        
        c_horizontal = SkyCoord(alt=EL*u.degree, az=AZ*u.degree, frame='altaz', obstime=time, location=observer)
        c_equatorial = c_horizontal.transform_to('icrs')
        
        return c_equatorial.ra.degree, c_equatorial.dec.degree


    def Galactic_to_horizontal(dateAndTime, observer, L, B, now=True):  #Time (manually or now=True gives current time) gps coordinates, altitude and galactic coordinates coordinates
        observer = EarthLocation.from_geodetic(lat=observer[0]*u.deg, lon=observer[1]*u.deg, height=observer[2]*u.m) 
        
        if now == True:
           time = datetime.utcnow()
        else:    
            time = str(dateAndTime[0]) + '-' + str(dateAndTime[1]) + '-' + str(dateAndTime[2]) + ' ' + str(hour) + ':' + str(dateAndTime[3]) + ':' + str(dateAndTime[4])
        time = Time(str(time))

        c_galactic = SkyCoord(frame="galactic", l=L*u.degree, b=B*u.degree)
        c_horizontal = c_galactic.transform_to(AltAz(obstime=time,location=observer))
        
        return c_horizontal.az.degree, c_horizontal.alt.degree


    def Horizontal_to_galactic(dateAndTime, observer, AZ, EL, now=True): #Time (manually or now=True gives current time) gps coordinates, altitude and horizontal coordinates
        observer = EarthLocation.from_geodetic(lat=observer[0]*u.deg, lon=observer[1]*u.deg, height=observer[2]*u.m) 
        
        if now == True:
           time = datetime.utcnow()
        else:    
            time = str(dateAndTime[0]) + '-' + str(dateAndTime[1]) + '-' + str(dateAndTime[2]) + ' ' + str(hour) + ':' + str(dateAndTime[3]) + ':' + str(dateAndTime[4])
        time = Time(str(time))

        c_horizontal = SkyCoord(alt=EL*u.degree, az=AZ*u.degree, frame='altaz', obstime=time, location=observer)
        c_galactic = c_horizontal.galactic

        return c_galactic.l.degree, c_galactic.b.degree