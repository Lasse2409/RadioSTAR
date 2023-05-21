import os
from src.rotor import rotor
from src.utilities import utilities


azElOffset = [231.4, -1] #[231.4 + 12, -1+2] #offset for Az and El calibration 

### Initializeing seriel connection to rotor and turning on bias tee
R = rotor("192.168.1.104", 23)


### Go to target this one we want to loop over and repeatedly update while data is being collected
print("Going to stow position: Az = 0 , El = 90")

target = [0, 90]

R.set(utilities.fullRotationLimit(target)[0] + utilities.azElOffset()[0], utilities.fullRotationLimit(target)[1] + utilities.azElOffset()[1])

print('In stow position: Az = 0 , El = 90')

R.status()
os.system("./../rtl-sdr-blog/build/src/rtl_biast -b 0")

print("Done!")

