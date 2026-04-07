## Single_PWN_setup

# [DRAGON2 code] Partially based on Fornieri et al (2020) JCAP 02 009- doi:10.1088/1475-7516/2020/02/009
import numpy as np
import scipy
from scipy import constants as const
import scipy.integrate as integrate
from scipy import interpolate
import matplotlib.pyplot as plt
## DRAGON2 CR ---- From utils_CR.py --- ISAPP2021
from utils_CR import CR
## ATNF Pulsar Catalogue in 1 kpc
from ATNF_Pulsar_Catalogue_1kpc import *
## PWN Eq
from equations import *
## MCMC Boundaries Setup
from boundaries_setup import *
## Energy All
from spectrum import *
from CRs_data import *
from mockdata import *
## Import data Libraries
import pandas as pd
from pandas import DataFrame
from astropy.io import fits as pyfits
## Unit and Constants
from astropy import units as u
from astropy import constants as const
##
import sys
##### End of Import Libraries Part ######

initial1 = [1.8, 950, 0.05] #Young
initial2 = [1.8, 200, 0.5] #Middle
initial3 = [1.8, 50, 0.8] #Old

yerr = errorCombineALL.value
data = (EnergyCombineALL.value, FluxE3CombineALL.value, yerr)

yerr_po = (E3FluxStatPositronsAMS02_2021.value**2 + E3FluxSysPositronsAMS02_2021.value**2)**0.5

en=EnergyCombineALL.value
energy = EnergyCombineALL.value

nwalkers = int(sys.argv[2])
niter = int(sys.argv[3])
processes_cpu = int(sys.argv[4])

ndim = len(initial1)

p01 = [initial1 + 1e-2* np.random.randn(ndim) for i in range(nwalkers)]
p02 = [initial2 + 1e-2* np.random.randn(ndim) for i in range(nwalkers)]
p03 = [initial3 + 1e-2* np.random.randn(ndim) for i in range(nwalkers)]

print('--------------------')
print('Degree of Freedom = ', ndim)
print('Energy All = ', len(EnergyCombineALL.value))
print('Datapotint - df = ', len(EnergyCombineALL.value) - ndim)
print('--------------------')
