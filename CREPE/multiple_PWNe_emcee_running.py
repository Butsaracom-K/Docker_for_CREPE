#### Import Libraries for MCMC Fitting ########
import emcee
import corner
from multiprocessing import Pool
from equations import *
from ATNF_Pulsar_Catalogue_1kpc import *
from multiple_PWNe_setup import *

##########
# MCMC Running
##########

file_name_FittingParameters_MultiPWNe = f'FittingParameters_MultiPWNe.dat'
save_path_FittingParameters_MultiPWNe = os.path.join(save_dir_Multi +'/FittingParameters', file_name_FittingParameters_MultiPWNe)
file = open(save_path_FittingParameters_MultiPWNe, 'a+')

file.write(f'PSR \t gamma_Young \t E_cut_Young \t eta_Young \t gamma_Middle \t E_cut_Middle \t eta_Middle \t gamma_Old \t E_cut_Old \t eta_Old \t ReducedChi^2_MultiPWNe \t ReducedChi2_po_MultiPWNe \t ReducedChi2_Combine_MultiPWNe\n')
####

### SetFolders -- Do not Change
file_name_CornerPlots_Multi_PWNe = f'Cornerplot_All_ATNF_Multi_PWNe_CutMilli.png'
save_path_CornerPlots_Multi_PWNe = os.path.join(save_dir_Multi +'/CornerPlots', file_name_CornerPlots_Multi_PWNe)
###
file_name_WalkerSteps_Multi_PWNe = f'Walkerstep_All_ATNF_Multi_PWNe_CutMilli.png'
save_path_WalkerSteps_Multi_PWNe = os.path.join(save_dir_Multi +'/WalkerSteps', file_name_WalkerSteps_Multi_PWNe)
###
file_name_Plotting_Multi_PWNe = f'[All_ATNF_Multi_PWNe_CutMilliloglogplot_parameters.png'
save_path_Plotting_Multi_PWNe = os.path.join(save_dir_Multi + '/Plotting', file_name_Plotting_Multi_PWNe)
###
file_name_Plotting_Multi_PWNe2 = f'[All_ATNF_Multi_PWNe_CutMilliloglogplot_parameters_positrons.png'
save_path_Plotting_Multi_PWNe2 = os.path.join(save_dir_Multi + '/Plotting_Positrons', file_name_Plotting_Multi_PWNe2)
###
file_name_Plotting_Multi_PWNe3 = f'[All_ATNF_Multi_PWNe_CutMilliloglogplot_parameters_Combined.png'
save_path_Plotting_Multi_PWNe3 = os.path.join(save_dir_Multi + '/Plotting_Combined', file_name_Plotting_Multi_PWNe3)
###
print("Start Running MCMC -- Find a drink while waiting")

with Pool(processes=processes_cpu) as pool:
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, pool=pool)
    sampler.run_mcmc(p0, niter, progress=True);

################

sampler_burned_in = sampler.flatchain[len(sampler.flatchain)//2:, :]

samples = sampler.flatchain
samples[np.argmax(sampler.flatlnprobability)]

theta_max = samples[np.argmax(sampler.flatlnprobability)]

########
# Parameters Results
########
print("Done!")


gamma_Young, e_cut_Young, eta_Young = [round(x, 4) for x in theta_max[:3]]
gamma_Middle, e_cut_Middle, eta_Middle = [round(x, 4) for x in theta_max[3:6]]
gamma_Old, e_cut_Old, eta_Old = [round(x, 4) for x in theta_max[6:9]]

print('------------------------------')
print('gamma_Young = ', gamma_Young)
print('gamma_Middle = ', gamma_Middle)
print('gamma_Old = ', gamma_Old)
print('------------------------------')


print('------------------------------')
print('e_cut_Young = ', e_cut_Young)
print('e_cut_Middle = ', e_cut_Middle)
print('e_cut_Old = ', e_cut_Old)
print('------------------------------')


print('------------------------------')
print('eta_Young  = ', eta_Young)
print('eta_Middle  = ', eta_Middle)
print('eta_Old  = ', eta_Old)
print('------------------------------')

print('------------------------------')
reducedchi_2 = round(reducedchi2(theta_max), 4)
reducedchi_2_po = round(reducedchi2_po(theta_max), 4)
reducedchi_2_combines = round(reducedchi2_combine(theta_max), 4)
print('reducedchi_2 = ', reducedchi_2)
print('reducedchi_2_po = ', reducedchi_2_po)
print('reducedchi2_combined = ', reducedchi_2_combines)
print("Mean acceptance fraction: {0:.3f}".format(np.mean(sampler.acceptance_fraction)))
print('------------------------------')

##
file.write(f'MultiplePWNe \t {gamma_Young} \t {e_cut_Young} \t {eta_Young} \t {gamma_Middle} \t {e_cut_Middle} \t {eta_Middle} \t {gamma_Old} \t {e_cut_Old} \t {eta_Old} \t {reducedchi_2} \t {reducedchi_2_po} \t {reducedchi_2_combines}')
file.flush()
file.close()

#########
## corner plot
#########

flat_samples = sampler.get_chain(discard=discard_adjust(niter), thin=15, flat=True)
labels = ['$\gamma_{Young}$', '$E_{cut_Young}$', '$\eta_{Young}$', '$\gamma_{Middle}$', '$E_{cut_Middle}$', '$\eta_{Middle}$', '$\gamma_{Old}$', '$E_{cut_Old}$', '$\eta_{Old}$', '$\gamma_Milli_{Old}$', '$E_{cut_Milli_Old}$', '$\eta_Milli_{Old}$']

##
fig = corner.corner(flat_samples, labels=labels, show_titles=True, plot_datapoint=True, quantiles=[0.16, 0.5, 0.84], truths=theta_max)

plt.savefig(save_path_CornerPlots_Multi_PWNe, dpi=300)
plt.close()
print('Successfully save corner plot')

########
## Walkerstep
########

fig, axes = plt.subplots(len(initial), figsize=(15, 30), sharex=True)
sample = sampler.get_chain()
for i in range(ndim):
    ax = axes[i]
    ax.plot(sample[:, :, i], 'k', alpha=1.0)
    ax.set_xlim(0, len(sample))
    ax.set_ylabel(labels[i])
    ax.yaxis.set_label_coords(-0.1, 1.0)
    axes[-1].set_xlabel('step number');

plt.savefig(save_path_WalkerSteps_Multi_PWNe, dpi=300)
plt.close()

print('Successfully save walkerstep plot')
print("Eng Process -- Coffee Break again!!")

########
## Plotting Setup

##### Log-Log Scale Plots
## Plot with fitting parameters -- CRs data

phi_ams = 0.55
fig1, ax = plt.subplots( figsize=(13,9), edgecolor='blue', facecolor = 'w')

plt.yscale('log')
plt.xscale('log')

### Observational data
# AMS-02 (2021)
plt.errorbar(EnergyAMS02_2021_ElecPo.value, E3FluxElectronPositronAMS02_2021.value, yerr=(E3FluxStatElectronPositronAMS02_2021.value**2 + E3FluxSysElectronPositronAMS02_2021.value**2)**0.5, fmt='o', ecolor='r', ms=5, color='r', label=r"AMS-02 (2021) ($e^{-}+e^{+}$)")
# H.E.S.S (2008)
plot_crs_data(EmeanHE, fluxHE, EmeanHE_low, EmeanHE_up, fluxHE_low, fluxHE_up, 'co', r"HESS (2008)")
#ATIC (2008)
plot_crs_data(EmeaneA, fluxeA, EmeaneA_low, EmeaneA_up, fluxeA_low, fluxeA_up, 'mo', r"ATIC (2008)")
# CALET (2018)
plot_crs_data(EmeaneC, fluxeC, EmeaneC_low, EmeaneC_up, fluxeC_low, fluxeC_up, 'yo', r"CALET (2018)")
# DAMPE (2017)
plot_crs_data(EmeaneD, fluxeD, EmeaneD_low, EmeaneD_up, fluxeD_low, fluxeD_up, 'bo', r"DAMPE (2017)")
# Fermi-LAT (2017)
plot_crs_data(EmeaneF, fluxeF, EmeaneF_low, EmeaneF_up, fluxeF_low, fluxeF_up, 'go', r"FERMI (2017)")

######## DRAGON2 Background (Electron+Positron BG)

plt.plot(MockEnergy, MockDRAGON2, color="k", linestyle='dotted', label = "Background")

######## Single PWN model and the Total (BG+PWN)
plt.plot(MockEnergy, modelPWNe(theta_max, MockEnergy), color='g', linestyle='-', label='Multiple PWNe', markersize=0.01)
plt.plot(MockEnergy, modelPWNe(theta_max, MockEnergy) + MockDRAGON2, 'r', label='Total', markersize=0.01)

###
for i in range(0, 6, 1):
    plt.plot(MockEnergy, np.real(pulsar(MockEnergy, gamma_Young, e_cut_Young, eta_Young, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value), color='g', linestyle='-.', markersize=0.01)
for i in range(6, 91, 1):
    plt.plot(MockEnergy, np.real(pulsar(MockEnergy, gamma_Middle, e_cut_Middle, eta_Middle, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value), color='g', linestyle='-.', markersize=0.01)
for i in range(91, 154, 1):
    plt.plot(MockEnergy, np.real(pulsar(MockEnergy, gamma_Old, e_cut_Old, eta_Old, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value), color='g', linestyle='-.', markersize=0.01)

lg = ax.legend(fontsize = 15, loc = 'upper right', ncol = 2)
lg.get_title().set_fontsize(20)

ax.set_ylabel("$E^{3} \Phi_{e^{-}+e^{+}} \, (GeV^{2} \, s^{-1} \, m^{-2} \, sr^{-1})$", fontsize = 22, labelpad = 10)
ax.set_xlabel("Energy (GeV)", fontsize = 24)
ax.set_xlim(left = 10, right = 5000)
ax.set_ylim(bottom = 1e-2, top = 5000)
ax.grid(color = '0.9', linestyle='-.', linewidth=1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=18)
#### Save Figure in Folder
plt.savefig(save_path_Plotting_Multi_PWNe, dpi=300)
plt.close()

##### Log-Log Scale Plots
## Plot with fitting parameters -- CR Positron (AMS-02) data

fig1, ax = plt.subplots( figsize=(13,9), edgecolor='blue', facecolor = 'w')

plt.yscale('log')
plt.xscale('log')

#### AMS-02 Positron data
plt.errorbar(EnergyAMS02_2021.value, E3FluxPositronsAMS02_2021.value, yerr=(E3FluxStatPositronsAMS02_2021.value**2)**0.5, fmt='o', ecolor='r', ms=5, color='r', label=r"AMS-02 (2021) ($e^{+}$)")

######## DRAGON2 Background (Electron+Positron BG)
plt.plot(MockEnergy_5000, MockDRAGON2_po_5000, color="k", linestyle='dotted', label = "Background $e^{+}$")

######## Single PWN model and the Total (BG+PWN)
plt.plot(MockEnergy_5000, modelPWNe_po(theta_max, MockEnergy_5000), color='g', linestyle='-', label='Multiple PWNe', markersize=0.01)
plt.plot(MockEnergy_5000, modelPWNe_po(theta_max, MockEnergy_5000) + MockDRAGON2_po_5000, 'r', label='Total', markersize=0.01)

#legend_title = rf"$\gamma$ = {gamma:.2f} $E_{{cut}}$ = {e_cut:.2f} $\eta$ = {eta:.2f} $\chi^2$ = {reducedchi_2po:.2f}"

###
for i in range(0, 6, 1):
    plt.plot(MockEnergy_5000, 0.5* np.real(pulsar(MockEnergy_5000, gamma_Young, e_cut_Young, eta_Young, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value), color='g', linestyle='-.', markersize=0.01)
for i in range(6, 91, 1):
    plt.plot(MockEnergy_5000, 0.5* np.real(pulsar(MockEnergy_5000, gamma_Middle, e_cut_Middle, eta_Middle, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value), color='g', linestyle='-.', markersize=0.01)
for i in range(91, 154, 1):
    plt.plot(MockEnergy_5000, 0.5* np.real(pulsar(MockEnergy_5000, gamma_Old, e_cut_Old, eta_Old, ATNF_Edot_Cut_Milli[i], ATNF_Age_Cut_Milli[i], delta, d0, e0, ATNF_Dist_Cut_Milli[i]).value), color='g', linestyle='-.', markersize=0.01)
 

lg = ax.legend(fontsize = 15, loc = 'upper right', ncol = 2)
lg.get_title().set_fontsize(20)

ax.set_ylabel("$E^{3} \Phi_{e^{-}+e^{+}} \, (GeV^{2} \, s^{-1} \, m^{-2} \, sr^{-1})$", fontsize = 22, labelpad = 10)
ax.set_xlabel("Energy (GeV)", fontsize = 24)
ax.set_xlim(left = 10, right = 5000)
ax.set_ylim(bottom = 1e-2, top = 500)
ax.grid(color = '0.9', linestyle='-.', linewidth=1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=18)
#### Save Figure in Folder
plt.savefig(save_path_Plotting_Multi_PWNe2, dpi=300)
plt.close()

##### Log-Log Scale Plots
### Combined Plots

fig1, ax = plt.subplots( figsize=(13,9), edgecolor='blue', facecolor = 'w')

plt.yscale('log')
plt.xscale('log')

### Observational data
# AMS-02 (2021)
plt.errorbar(EnergyAMS02_2021_ElecPo.value, E3FluxElectronPositronAMS02_2021.value, yerr=(E3FluxStatElectronPositronAMS02_2021.value**2 + E3FluxSysElectronPositronAMS02_2021.value**2)**0.5, fmt='o', ecolor='r', ms=5, color='r', label=r"AMS-02 (2021) ($e^{-}+e^{+}$)")
# H.E.S.S (2008)
plot_crs_data(EmeanHE, fluxHE, EmeanHE_low, EmeanHE_up, fluxHE_low, fluxHE_up, 'co', r"HESS (2008)")
#ATIC (2008)
plot_crs_data(EmeaneA, fluxeA, EmeaneA_low, EmeaneA_up, fluxeA_low, fluxeA_up, 'mo', r"ATIC (2008)")
# CALET (2018)
plot_crs_data(EmeaneC, fluxeC, EmeaneC_low, EmeaneC_up, fluxeC_low, fluxeC_up, 'yo', r"CALET (2018)")
# DAMPE (2017)
plot_crs_data(EmeaneD, fluxeD, EmeaneD_low, EmeaneD_up, fluxeD_low, fluxeD_up, 'bo', r"DAMPE (2017)")
# Fermi-LAT (2017)
plot_crs_data(EmeaneF, fluxeF, EmeaneF_low, EmeaneF_up, fluxeF_low, fluxeF_up, 'go', r"FERMI (2017)")

# AMS-02 Positron data (2021)
plt.errorbar(EnergyAMS02_2021.value, E3FluxPositronsAMS02_2021.value, yerr=(E3FluxStatPositronsAMS02_2021.value**2)**0.5, fmt='o', ecolor='r', ms=5, color='r', label=r"AMS-02 (2021) ($e^{+}$)")

######## DRAGON2 Background (Electron+Positron BG)
plt.plot(MockEnergy, MockDRAGON2, color="k", linestyle='dotted', label = "Background")

######## DRAGON2 Background (Positron BG)
plt.plot(MockEnergy_5000, MockDRAGON2_po_5000, color="k", linestyle='dotted', label = "Background $e^{+}$")

######## Single PWN model and Total (PWN+BG)
#### CRs data
plt.plot(MockEnergy, modelPWNe(theta_max, MockEnergy), color='g', linestyle='-.', label='Multiple PWNe $(e^{-}+e^{+})$', markersize=0.01)
plt.plot(MockEnergy_5000, 0.5*modelPWNe(theta_max, MockEnergy_5000), color='b', linestyle='--', label='Multiple PWNe $(e^{+})$', markersize=0.01)

plt.plot(MockEnergy, modelPWNe(theta_max, MockEnergy) + MockDRAGON2, 'g', label='Total', markersize=0.01)

#### CR Positron data
plt.plot(MockEnergy_5000, 0.5*modelPWNe(theta_max, MockEnergy_5000) + MockDRAGON2_po_5000, 'b', label='Total $e^{+}$', markersize=0.01)    

lg = ax.legend(fontsize = 15, loc = 'upper right', ncol = 2)
lg.get_title().set_fontsize(20)

ax.set_ylabel("$E^{3} \Phi_{e^{-}+e^{+}} \, (GeV^{2} \, s^{-1} \, m^{-2} \, sr^{-1})$", fontsize = 22, labelpad = 10)
ax.set_xlabel("Energy (GeV)", fontsize = 24)
ax.set_xlim(left = 10, right = 5000)
ax.set_ylim(bottom = 1e0, top = 20000)
ax.grid(color = '0.9', linestyle='-.', linewidth=1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=18)
#### Save Figure in Folder
plt.savefig(save_path_Plotting_Multi_PWNe3, dpi=300)
plt.close()
