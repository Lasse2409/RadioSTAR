from rtlsdr import RtlSdr

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 92e6     # Hz
sdr.gain = 49.6

data = sdr.read_samples(256*1024)

f = open("pydata.dat", "w")

for i in range(len(data)):
    if data[i].imag > 0:
        f.write(str(data[i].real) + "+" + str(data[i].imag) + "i, ")
    else:
        f.write(str(data[i].real) + "" + str(data[i].imag) + "i, ")

f.close()
