#[DRAGON2 code] Partially based on Fornieri et al (2020) JCAP 02 009- doi:10.1088/1475-7516/2020/02/009
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
## Energy All
from spectrum import *
from CRs_data import *
from mockdata import *
## Import data Libraries
import pandas as pd
from pandas import DataFrame
from astropy.io import fits as pyfits
## Import Directory Setup
from directory_setup import *
## Unit and Constants
from astropy import units as u
from astropy import constants as const
## MCMC Boundaries Setup -- Used the same bounds. with Single PWN Model
from boundaries_setup import *
##
import sys
####### End of Import Libraries Part ######

yerr = errorCombineALL.value
data = (EnergyCombineALL.value, FluxE3CombineALL.value, yerr)

###### initial gamma, e_cut, eta --> Young, Middle, Old, Old_Milli
initial = [2.1064, 1012.0937, 0.2899, 2.2007, 101.0114, 0.6999, 1.8024, 339.9098, 0.7994]

## Define MCMC initial Parameters
ndim = len(initial)

niter = int(sys.argv[2])
nwalkers = int(sys.argv[3])
processes_cpu = int(sys.argv[4])
print('----------------------------')
print('nwalkers = ', nwalkers)
print('niter = ', niter)
p0 = [initial + 1e-2* np.random.randn(ndim) for i in range(nwalkers)]

## Error for Positron AMS-02 Spectrum
yerr_po = (E3FluxStatPositronsAMS02_2021.value**2 + E3FluxSysPositronsAMS02_2021.value**2)**0.5
print('----------------------------')
print('Degree of Freedom = ', ndim)
print('Energy All = ', len(EnergyCombineALL.value))
print('Datapotint - df = ', len(EnergyCombineALL.value) - ndim)
print('----------------------------')

## Define Ranges for PWNe Loops
Range_Young = range(Young_Aged_PWNe_Cut_Milli.index[0], Young_Aged_PWNe_Cut_Milli.index[-1] + 1, 1)
Range_Middle = range(Middle_Aged_PWNe_Cut_Milli.index[0], Middle_Aged_PWNe_Cut_Milli.index[-1] + 1, 1)
Range_Old = range(Old_Aged_PWNe_Cut_Milli.index[0], Old_Aged_PWNe_Cut_Milli.index[-1] + 1, 1)

### Define Functions for MCMC and Multiple PWNe Model
def discard_adjust(niter):
    if niter >= 1000:
        return int(1000/2)
    elif niter <= 100:
        return int(100/2)
    else:
        return int(50/2)

def modelPWNe(theta, en):
    gamma_Young, e_cut_Young, eta_Young, gamma_Middle, e_cut_Middle, eta_Middle, gamma_Old, e_cut_Old, eta_Old  = theta
    model_Young = 0
    model_Middle = 0
    model_Old = 0

    for i in Range_Young:
        model_Young += np.real(pulsar(en, gamma_Young, e_cut_Young, eta_Young, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value)
    for i in Range_Middle:
        model_Middle += np.real(pulsar(en, gamma_Middle, e_cut_Middle, eta_Middle, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value)
    for i in Range_Old:
        model_Old += np.real(pulsar(en, gamma_Old, e_cut_Old, eta_Old, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value)
 
    model = (model_Young + model_Middle + model_Old)
    return model

def modelPWNe_po(theta, en):
    gamma_Young, e_cut_Young, eta_Young, gamma_Middle, e_cut_Middle, eta_Middle, gamma_Old, e_cut_Old, eta_Old  = theta
    model_Young_po = 0
    model_Middle_po = 0
    model_Old_po = 0

    for i in Range_Young:
        model_Young_po += 0.5* np.real(pulsar(en, gamma_Young, e_cut_Young, eta_Young, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value)
    for i in Range_Middle:
        model_Middle_po += 0.5* np.real(pulsar(en, gamma_Middle, e_cut_Middle, eta_Middle, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value)
    for i in Range_Old:
        model_Old_po += 0.5* np.real(pulsar(en, gamma_Old, e_cut_Old, eta_Old, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value)
 
    model_po = (model_Young_po + model_Middle_po + model_Old_po)
    return model_po

def lnlike(theta):
    model_all_po = modelPWNe_po(theta, EnergyAMS02_2021.value) + DRAGON_Pri_po_AMS02
    lnlike_po = -0.5 * np.sum(((E3FluxPositronsAMS02_2021.value - model_all_po)/yerr_po)**2)
 
    model_all = modelPWNe(theta, EnergyCombineALL.value) + DRAGON_Pri_ele
    lnlike_ele = -0.5 * np.sum(((FluxE3CombineALL.value - model_all)/yerr)**2)
    return lnlike_po + lnlike_ele

def lnprior(theta):
    [gamma_Young, e_cut_Young, eta_Young, gamma_Middle, e_cut_Middle, eta_Middle, gamma_Old, e_cut_Old, eta_Old] = theta
    if gamma_Young_LB <= gamma_Young <= gamma_Young_UB and e_cut_Young_LB <= e_cut_Young <= e_cut_Young_UB and eta_Young_LB <= eta_Young <= eta_Young_UB and gamma_Middle_LB <= gamma_Middle <= gamma_Middle_UB and e_cut_Middle_LB <= e_cut_Middle <= e_cut_Middle_UB and eta_Middle_LB <= eta_Middle <= eta_Middle_UB and gamma_Old_LB <= gamma_Old <= gamma_Old_UB and e_cut_Old_LB <= e_cut_Old <= e_cut_Old_UB and eta_Old_LB <= eta_Old <= eta_Old_UB:
        return 0.0
    return -np.inf

def lnprob(theta):
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta)

def reducedchi2(theta):
    model_all = modelPWNe(theta, EnergyCombineALL.value) + DRAGON_Pri_ele
    model = model_all
    return np.sum((((FluxE3CombineALL.value - model)/yerr)**2)/(len(FluxE3CombineALL.value)-len(theta)))

def reducedchi2_po(theta):
    model = modelPWNe_po(theta, EnergyAMS02_2021.value) + DRAGON_Pri_po_AMS02
    return np.sum((((E3FluxStatPositronsAMS02_2021.value - model)/yerr_po)**2)/(len(E3FluxPositronsAMS02_2021.value)-len(theta)))

def reducedchi2_combine(theta):
    model_po = modelPWNe_po(theta, EnergyAMS02_2021.value) + DRAGON_Pri_po_AMS02
    modelpo = np.where(np.isnan(model_po), 0, model_po)
    reduce_po = np.sum((((E3FluxPositronsAMS02_2021.value - modelpo)/yerr_po)**2))
    ## All Electron+Positron data
    model_all = modelPWNe(theta, EnergyCombineALL.value) + DRAGON_Pri_ele
    model = np.where(np.isnan(model_all), 0, model_all)
    reduce_all = np.sum((((FluxE3CombineALL.value - model)/yerr)**2))
    return (reduce_all+reduce_po)/((len(FluxE3CombineALL.value)+len(E3FluxPositronsAMS02_2021.value))-len(theta))
