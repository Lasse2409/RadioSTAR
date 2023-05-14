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
    
        
    def rtlSample(rtlSDRSetup, header): #(samples, sampleRate, centerFreq, gain, filePathName, dataFileExtension, header)
        sdr = RtlSdr()
	
	#samples, sampleRate, centerFreq, gain, filePathName, dataFileExtension, header)
        sdr.sample_rate = rtlSDRSetup[1]
        sdr.center_freq = rtlSDRSetup[2]
        sdr.gain = rtlSDRSetup[3]

        samples = sdr.read_samples(rtlSDRSetup[0])
        sdr.close()

        f = open(rtlSDRSetup[4] + str(rtlSDRSetup[5]) + ".dat", "w")
        
        for idx in range(len(header)):
            f.write(header[idx])
        
        ps, freqs = psd(samples, NFFT=256, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

        for j in range(len(ps)):
            f.write(str(ps[j]) + ", " + str(freqs[j]) + "\n")

        f.close()


    ### Function that returns a list with all header content
    def makeHeader():
        header = []
        header.append("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
        header.append("#Latitude: " + str(observer[0]) + "\n")
        header.append("#Longitude: " + str(observer[1]) + "\n")
        header.append("#Altitude: " + str(observer[2]) + "\n")
        header.append("#Az: " + str(measuredCoordinateHorizontal[0]) + "\n")
        header.append("#El: " + str(measuredCoordinateHorizontal[1]) + "\n")
        header.append("#Galactic latitude: " + str(measuredCoordinateGalactic[0]) + "\n")
        header.append("#Galactic longitude: " + str(measuredCoordinateGalactic[1]) + "\n")
        header.append("#RA: " + str(measuredCoordinateEquatorial[0]) + "\n")
        header.append("#Dec: " + str(measuredCoordinateEquatorial[1]) + "\n")
        header.append("#rtl_samples: " + str(rtlSDRSetup[0]) + "\n")
        header.append("#rtl_sampleRate: " + str(rtlSDRSetup[1]) + "\n")
        header.append("#rtl_centerFreq: " + str(rtlSDRSetup[2]) + "\n")
        header.append("#rtl_gain: " + str(rtlSDRSetup[3]) + "\n")    
        
        return header

    def psd():
        print('not finished function')
    
 
