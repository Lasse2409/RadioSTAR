import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from rtlsdr import *
from pylab import *
from astropy.time import Time

from src.Coordinate_transforms import coordinates



class utilities:
    def __init__(self, rtlSDRSetup, dateAndTime, observer):
        self.rtlSDRSetup = rtlSDRSetup
        self.dateAndTime = dateAndTime
        self.observer = observer
        #self.target = target

        #self.measurementCoordinates(self, targetCoordinateSystem)


    def skyBox(self, N, AZ, EL):
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


    ### If Az is more than 180 degrees, then go all the way around to 360-180 instead
    def fullRotationLimit(target):    
        setEl = target[1]

        if target[0] > 180:
            setAz = -(360-target[0])
        else:
            setAz = target[0]

        return setAz, setEl


    def azElOffset():
        azOffset = 231.4 + 12
	    elOffset = -1 + 2

        return azOffset, elOffset
        

    def rtlSample(self, dataFileExtension, header): 
        sdr = RtlSdr()
	
        sdr.sample_rate = self.rtlSDRSetup[1]
        sdr.center_freq = self.rtlSDRSetup[2]
        sdr.gain = self.rtlSDRSetup[3]

        samples = sdr.read_samples(self.rtlSDRSetup[0])
        sdr.close()

        f = open(self.rtlSDRSetup[4] + str(dataFileExtension) + ".dat", "w")
        
        for idx in range(len(header)):
            f.write(header[idx])
        
        ps, freqs = psd(samples, NFFT=256, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

        for j in range(len(ps)):
            f.write(str(ps[j]) + ", " + str(freqs[j]) + "\n")

        f.close()

    ### Given target coordinates (in given coordinate system targetCoordinateSystem 0-> horizontal, 1-> galactic(longitude,latitude), 2-> equatorial) provide coordinates in other coordinate systems as np.array
    def measurementCoordinates(self, targetCoordinateSystem, target):
        measuredCoordinateHorizontal = np.zeros(np.shape(target))
        measuredCoordinateEquatorial = np.zeros(np.shape(target))
        measuredCoordinateGalactic = np.zeros(np.shape(target))
    
        if targetCoordinateSystem == 0:
            measuredCoordinateHorizontal = np.asarray(target)
            measuredCoordinateGalactic = np.transpose(coordinates.Horizontal_to_galactic(self.dateAndTime, self.observer, target[0], target[1], now = True))
            measuredCoordinateEquatorial = np.transpose(coordinates.Horizontal_to_equatorial(self.dateAndTime, self.observer, target[0], target[1], now = True))
            
        elif targetCoordinateSystem == 1:
            measuredCoordinateHorizontal = np.transpose(coordinates.Galactic_to_horizontal(self.dateAndTime, self.observer, target[0], target[1], now = True))
            measuredCoordinateGalactic = np.asarray(target)
            measuredCoordinateEquatorial = np.transpose(coordinates.Galactic_to_equatorial(target[0], target[1]))
        
        elif targetCoordinateSystem == 2:
            measuredCoordinateHorizontal = np.transpose(coordinates.Equatorial_to_horizontal(self.dateAndTime, self.observer, target[0], target[1], now = True))
            measuredCoordinateGalactic = np.transpose(coordinates.Equatorial_to_galactic(target[0], target[1]))
            measuredCoordinateEquatorial = np.asarray(target)
        
        else:
            print('wrong coordinate system specified')
            exit()
        
        return measuredCoordinateHorizontal, measuredCoordinateGalactic, measuredCoordinateEquatorial


    ### Function that returns a list with all header content
    def makeHeader(self, measuredCoordinates):
        header = []
        header.append("#Local time: " + Time.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
        header.append("#Latitude: " + str(self.observer[0]) + "\n")
        header.append("#Longitude: " + str(self.observer[1]) + "\n")
        header.append("#Altitude: " + str(self.observer[2]) + "\n")
        header.append("#Az: " + str(measuredCoordinates[0][0]) + "\n")
        header.append("#El: " + str(measuredCoordinates[0][1]) + "\n")
        header.append("#Galactic latitude: " + str(measuredCoordinates[1][0]) + "\n")
        header.append("#Galactic longitude: " + str(measuredCoordinates[1][1]) + "\n")
        header.append("#RA: " + str(measuredCoordinates[2][0]) + "\n")
        header.append("#Dec: " + str(measuredCoordinates[2][1]) + "\n")
        header.append("#rtl_samples: " + str(self.rtlSDRSetup[0]) + "\n")
        header.append("#rtl_sampleRate: " + str(self.rtlSDRSetup[1]) + "\n")
        header.append("#rtl_centerFreq: " + str(self.rtlSDRSetup[2]) + "\n")
        header.append("#rtl_gain: " + str(self.rtlSDRSetup[3]) + "\n")    
        
        return header

    def lineScan(self, AzElScan, targetName, numMeasurements, angIncroment): #, targetName, numMeasurements,angIncroment, self.rtlSDRSetup, targetName, dateAndTime, observer):
        for idx in range(numMeasurements):

            #file = self.rtlSDRSetup[4] + "Az-"
            self.rtlSDRSetup[4] = self.rtlSDRSetup[4] + str(AzElScan) + "-"
            obj = coordinates.getObject(targetName, self.dateAndTime, self.observer, now=True)

            ### Make target azimuth offset
            target = [(obj[0]-0.5*(numMeasurements-1)*angIncroment) + idx*angIncroment, obj[1]]

            ### Store the measured coordinates in all coordinate systems (horizontal, galactic and equatorial)
            measuredCoordinates = utilities.measurementCoordinates(self, 0, target)

            ### Make sure that we dont go below elevation limit
            if measuredCoordinates[0][1] < 0:
                print('Tool low elevation (<0)')
                os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")
                exit()


            ### Create header for data file (time, coordinates and sdr settings)
            header = utilities.makeHeader(self, measuredCoordinates)

            ### Go to target this one we want to loop over and repeatedly update while data is being collected
            print("Going to: (" + str(measuredCoordinates[0][0]) + ", " + str(measuredCoordinates[0][1]) + ")")

            R.set(utilities.fullRotationLimit(target) + utilities.azElOffset[0], utilities.fullRotationLimit[1] + utilities.azElOffset[1])
            R.status()

            ### Collect data 
            time.sleep(2)
            print("Measuring data...")
            utilities.rtlSample(self, idx, header) #max samples is 256*1024*31



    
