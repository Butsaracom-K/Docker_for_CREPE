### Pulsar Wind Nebula (PWN) Equations
import numpy as np
import scipy
import scipy.integrate as integrate
## Unit and Constants
from astropy import units as u
from astropy import constants as const
from constants import *

## Equations
def e_max(td):
    return (b0 * (td*u.year).to(u.second))**-1


def d11(en, d0, e0, delta):
    return (d0) * ((en *u.GeV)/e0)**delta

## Diffution length
def rdiff(en, delta, d0, e0, td):
    return 2 * (d11(en, d0, e0, delta) * ((td*u.year).to(u.second)) * ((1 -(1 - ((en *u.GeV)/e_max(td))**(1-delta))) / ((1-delta) * ((en *u.GeV)/e_max(td)))))**0.5


def Q0(gamma, e_cut, eta, edot, td):
    return ((eta*(edot*u.erg*u.second**-1).to(u.GeV*u.second**-1))* ((td*u.year).to(u.second)) * (1+ (((td*u.year).to(u.second))/(((1e4 *u.year).to(u.second))))) / (integrate.quad(lambda x: x*(x**-gamma)* np.exp(-x/e_cut), 0.1, np.inf)[0])) *u.GeV**-2


def etaW0(eta, edot, td):
    return (eta*(edot*u.erg*u.second**-1).to(u.GeV*u.second**-1))* ((td*u.year).to(u.second)) * (1+ (((td*u.year).to(u.second))/((1e4 *u.year).to(u.second))))

## Spectrum
def pulsar(en, gamma, e_cut, eta, edot, td, delta, d0, e0, d):
    model = (Q0(gamma, e_cut, eta, edot, td) / ((np.pi**(3/2))* (rdiff(en, delta, d0, e0, td)**3) ))* ((1 - ((en *u.GeV)/e_max(td)))**(gamma-2)) * (((en *u.GeV) * (u.GeV**-1))**(-gamma)) * np.exp(-(en/ ((1- (en/e_max(td).value)) *e_cut))) * np.exp(- ((d*u.kpc).to(u.meter)).value**2/ (rdiff(en, delta, d0, e0, td).value)**2 ) * (c/(4*np.pi))*(u.sr**-1) * np.heaviside([e_max(td).value - en], 1)[0] *(en *u.GeV)**3
    return np.real(np.where(np.isnan(model), 0, model))
