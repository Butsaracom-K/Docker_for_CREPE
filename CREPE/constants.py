### Constants for Model
import numpy as np
## Unit and Constants
from astropy import units as u
from astropy import constants as const

### End of Import 

## Pulsar Wind Nebula Parameters
c = const.c
b0 = 1.4e-16 * (u.GeV**-1 *u.second**-1)
delta = 0.45
d0 = (3.8*10**28 *u.centimeter**2*u.second**-1).to(u.meter**2 *u.second**-1)
e0 = 4 *u.GeV
B = 7.5* u.microGauss

## Loss Rate
b_Coul_norm = 1.2e-12 * u.centimeter**3
b_brem_norm = 1.51e-16* u.centimeter**3
b_ion_norm = 1.5e-20* 1e+6* u.centimeter**3

N_SL = 3.39e-14
N_IR = 4.5e-5
T_SL = 6150.4 *u.K
T_IR = 33.1 *u.K

################
