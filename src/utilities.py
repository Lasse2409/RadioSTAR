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

    ### If Az is more than 180 degrees, then go all the way around to 360-180 instead
    def fullRotationLimit(target):    
        setEl = target[1]

        if target[0] > 180:
            setAz = -(360-target[0])
        else:
            setAz = target[0]
        
        return setAz, setEl


    def azElOffset():
        azElOffset = [231.4 + 12, -1+2]
        return azElOffset[0], azElOffset[1]
    
 
