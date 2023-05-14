# check howizontal coordinates of now, convert to galactic coordinates, and convert back to horizontal coordinates, check if above horizon. 
import os
from src.rotor import rotor


azElOffset = [231.4, -1] #offset for Az and El calibration 

### Initializeing seriel connection to rotor and turning on bias tee
R = rotor("192.168.1.104", 23)


### Go to target this one we want to loop over and repeatedly update while data is being collected
print("Going to stow position: (0, 90)")

R.set(0 + azElOffset[0], 90 + azElOffset[1])

print('In stow position: ')

R.status()
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")

print("Done!")

