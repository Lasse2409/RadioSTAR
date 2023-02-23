from pylab import *
from rtlsdr import *
import numpy as np

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1420e6
sdr.gain = 49.6

N = 1

samples = sdr.read_samples(256*1024)

for i in range(N-1):
    print(i)
    np.append(samples, sdr.read_samples(256*1024))

sdr.close()

# use matplotlib to estimate and plot the PSD
psd(samples, NFFT=256*N, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

show()
