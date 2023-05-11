import matplotlib.pyplot as plt
import numpy as np
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
        
        ps, freqs = psd(samples, NFFT=256, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

        for j in range(len(ps)):
            f.write(str(ps[j]) + ", " + str(freqs[j]) + "\n")

        f.close()

        R.status()
        print("Measuring data...")

    def psd():
        print('not finished function')
    
 