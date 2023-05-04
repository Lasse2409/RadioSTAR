import matplotlib.pyplot as plt
import numpy as np



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
    
    def psd():
        print('not finished function')