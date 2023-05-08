import matplotlib.pyplot as plt
import numpy as np
from rtlsdr import *
from datetime import datetime

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
    
        
    def rtlSample(samples, sampleRate, centerFreq, gain, dataFileExtension):
        sdr = RtlSdr()

        sdr.sample_rate = sampleRate
        sdr.center_freq = centerFreq
        sdr.gain = gain

        samples = sdr.read_samples(samples)
        sdr.close()

        f = open("data/2data-" + str(dataFileExtension) + ".dat", "w")
        
        f.write("#Local time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
        f.write("#Latitude: " + str(lat))
        f.write("#Longitude: " + str(lon))
        f.write("#Altitude: " + str(alt))
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

    def psd():
        print('not finished function')
