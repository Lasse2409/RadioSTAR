# check howizontal coordinates of now, convert to galactic coordinates, and convert back to horizontal coordinates, check if above horizon. 
import os
from src.rotor import rotor



### Initializeing seriel connection to rotor and turning on bias tee
R = rotor("192.168.1.104", 23)


### Go to target this one we want to loop over and repeatedly update while data is being collected
print("Going to stow work position")



R.set(266, 0)

R.overwrite = True
R.set(275,-15)
R.overwrite = False

print('In work position: ')

R.status()
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")

print("Done!")

