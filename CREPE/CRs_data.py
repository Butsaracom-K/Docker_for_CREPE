import numpy as np
import matplotlib.pyplot as plt

### Some part of the code will be hidden

datafolder = '/CREPE_Dir/CREPE/data/'

# All-lepton (e^{+} + e^{-}) data
data = datafolder + 'e+e-_AMS_PRL2019.txt'
Emeane, Emeane_low, Emeane_up = np.loadtxt(data,skiprows=0,usecols=(0,1, 2), unpack = True)
fluxe, fluxe_low, fluxe_up = np.loadtxt(data,skiprows=0,usecols=(3, 4, 5), unpack=True)    
errfluxe = (fluxe_low + fluxe_up)/2


# All-lepton (e^{+} + e^{-}) data
data = datafolder + 'e+e-_AMS_PRL2019.txt'
Emeane, Emeane_low, Emeane_up = np.loadtxt(data,skiprows=0,usecols=(0,1, 2), unpack = True)
fluxe, fluxe_low, fluxe_up = np.loadtxt(data,skiprows=0,usecols=(3, 4, 5), unpack=True)    
errfluxe = (fluxe_low + fluxe_up)/2

data = datafolder + 'e+e-_HESS_PRL2008_HE.txt'
EmeanHE, EmeanHE_low, EmeanHE_up = np.loadtxt(data,skiprows=0,usecols=(0,1, 2), unpack = True)
fluxHE, fluxHE_low, fluxHE_up = np.loadtxt(data,skiprows=0,usecols=(3, 4, 5), unpack=True)    
errfluxHE = (fluxHE_low + fluxHE_up)/2

data = datafolder + 'e+e-_ATIC_Nature2008.txt'
EmeaneA, EmeaneA_low, EmeaneA_up = np.loadtxt(data,skiprows=0,usecols=(0,1, 2), unpack = True)
fluxeA, fluxeA_low, fluxeA_up = np.loadtxt(data,skiprows=0,usecols=(3, 4, 5), unpack=True)    
errfluxeA = (fluxeA_low + fluxeA_up)/2


### Create Function for Plotting in Results
def plot_crs_data(E, flux, E_low, E_up, flux_low, flux_up, fmt, label, slope=3):
    x_err = [np.absolute((E - E_low) / E), np.absolute((E_up - E) / E)]
    y_err = [flux_low * np.power(E, slope), flux_up * np.power(E, slope)]
    y_val = flux * np.power(E, slope)
    return plt.errorbar(E, y_val, xerr=x_err, yerr=y_err, ms=5, fmt=fmt, label=label)
