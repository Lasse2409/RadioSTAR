import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from rtlsdr import *
from pylab import *



class utilities:

    def skyBox(N, AZ, EL):
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
    
        
    def rtlSample(rtlSDRSetup, dataFileExtension, header): #(samples, sampleRate, centerFreq, gain, filePathName, header)
        sdr = RtlSdr()
	
	    #samples, sampleRate, centerFreq, gain, filePathName, dataFileExtension, header)
        sdr.sample_rate = rtlSDRSetup[1]
        sdr.center_freq = rtlSDRSetup[2]
        sdr.gain = rtlSDRSetup[3]

        samples = sdr.read_samples(rtlSDRSetup[0])
        sdr.close()

        f = open(rtlSDRSetup[4] + str(dataFileExtension) + ".dat", "w")
        
        for idx in range(len(header)):
            f.write(header[idx])
        
        ps, freqs = psd(samples, NFFT=256, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

        for j in range(len(ps)):
            f.write(str(ps[j]) + ", " + str(freqs[j]) + "\n")

        f.close()


    def getSun(dateAndTime, observer, now=True):
        # Define the location on Earth (latitude, longitude, elevation in meters)
        observer = EarthLocation(lat=observer[0]*u.deg, lon=observer[1]*u.deg, height=observer[2]*u.m)

        # Define the time, either now or given in dateAndTime list
        if now == True:
           time = datetime.utcnow()
        else:    
            time = str(dateAndTime[0]) + '-' + str(dateAndTime[1]) + '-' + str(dateAndTime[2]) + ' ' + str(hour) + ':' + str(dateAndTime[3]) + ':' + str(dateAndTime[4])
        time = Time(str(time)) 

        # Get the Sun's position in Altitude-Azimuth coordinates at the current time and location
        sunAzEl = get_moon(currentTime).transform_to(AltAz(obstime=currentTime, location=location))

        # Return the az end el of sun position 
        return sunAzEl.az.degree, sunAzEl.alt.degree



    def psd():
        print('not finished function')
    
 
