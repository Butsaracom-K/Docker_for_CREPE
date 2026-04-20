#### Middle-Ages PWN

import emcee
import corner
from multiprocessing import Pool
from equations import *

from spectrum import *
from ATNF_Pulsar_Catalogue_1kpc import *
from single_PWN_setup import *
## Call for Directory
from directory_setup import *

####
# MCMC Running Loop

def discard_adjust(niter):
    if niter >= 1000:
        return int(1000/2)
    elif niter <= 100:
        return int(100/2)
    else:
        return int(50/2)

def model(theta, en):
    gamma, e_cut, eta = theta
    model = pulsar(en, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value + DRAGON_Pri_ele 
    return model
###
def lnlike(theta):
    en = energy
    gamma, e_cut, eta = theta
    modelpo = (0.5*pulsar(EnergyAMS02_2021.value, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value) + DRAGON_Pri_po_AMS02
    lnlike1po = -0.5 * np.sum(((E3FluxPositronsAMS02_2021.value - modelpo)/yerr_po)**2)

    model = pulsar(EnergyCombineALL.value, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value + DRAGON_Pri_ele
    lnlike1 = -0.5 * np.sum(((FluxE3CombineALL.value - model)/yerr)**2)
    return lnlike1 + lnlike1po
###
def lnprior(theta):
    [gamma, e_cut, eta] = theta
    if gamma_Middle_LB <= gamma <= gamma_Middle_UB and e_cut_Middle_LB <= e_cut <= e_cut_Middle_UB and eta_Middle_LB <= eta <= eta_Middle_UB:
        return 0.0
    return -np.inf
####
def lnprob(theta):
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta)
####
def reducedchi2(theta):
    en = energy
    [gamma, e_cut, eta] = theta
    model = pulsar(EnergyCombineALL.value, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value + DRAGON_Pri_ele
    return np.sum((((FluxE3CombineALL.value - model)/yerr)**2)/(len(FluxE3CombineALL.value)-len(theta)))
##########
def reducedchi2po(theta):
    en = energy
    [gamma, e_cut, eta] = theta
    model = (0.5*pulsar(EnergyAMS02_2021.value, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value) + DRAGON_Pri_po_AMS02
    return np.sum((((E3FluxPositronsAMS02_2021.value - model)/yerr_po)**2)/(len(E3FluxPositronsAMS02_2021.value)-len(theta)))

#####
def reducedchi2_combine(theta):
    en = energy
    [gamma, e_cut, eta] = theta
    model1 = np.real(pulsar(EnergyCombineALL.value, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value) + DRAGON_Pri_ele
    model = np.where(np.isnan(model1), 0, model1)
    reduce_all = np.sum((((FluxE3CombineALL.value - model)/yerr)**2))

    model1po = (0.5*np.real(pulsar(EnergyAMS02_2021.value, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value)) + DRAGON_Pri_po_AMS02
    modelpo = np.where(np.isnan(model1po), 0, model1po)
    reduce_po = np.sum((((E3FluxPositronsAMS02_2021.value - modelpo)/yerr_po)**2))
    return (reduce_all+reduce_po)/((len(FluxE3CombineALL.value)+len(E3FluxPositronsAMS02_2021.value))-len(theta))

file_name_FittingParameters_Middle_PWN = f'FittingParameters_Middle_SinglePWN.dat'
save_path_FittingParameters_Middle_PWN = os.path.join(save_dir +'/FittingParameters/Middle_PWN', file_name_FittingParameters_Middle_PWN)
file = open(save_path_FittingParameters_Middle_PWN, 'a+')
file.write(f'PSR \t Edot (erg/s) \t Age (year) \t d (kpc) \t gamma \t E_cut \t eta \t etaEdot \t E_max (GeV) \t ReducedChi^2_Middle \t ReducedChi2_po_Middle \t reducedchi_2_combine_Middle\n')

#index = np.arange(0, len(ATNF_NamePSR_Cut_Milli), 1):
for i in np.arange(6, 91, 1):
        k = i
        edot = ATNF_Edot_Cut_Milli[i]
        PSR = ATNF_NamePSR_Cut_Milli[i]
        td = ATNF_Age_Cut_Milli[i]
        d = ATNF_Dist_Cut_Milli[i]
        ### SetFolders -- Do not Change
        file_name_CornerPlots_Middle_PWN = f'Cornerplot_{[i]}_{ATNF_NamePSR_Cut_Milli[i]}.png'
        save_path_CornerPlots_Middle_PWN = os.path.join(save_dir +'/CornerPlots/Middle_PWN', file_name_CornerPlots_Middle_PWN)
        ###
        file_name_WalkerSteps_Middle_PWN = f'Walkerstep_{[i]}_{ATNF_NamePSR_Cut_Milli[i]}.png'
        save_path_WalkerSteps_Middle_PWN = os.path.join(save_dir +'/WalkerSteps/Middle_PWN', file_name_WalkerSteps_Middle_PWN)
        ###
        file_name_Plotting_Middle_PWN = f'[{i}]_{PSR}_loglogplot_parameters.png'
        save_path_Plotting_Middle_PWN = os.path.join(save_dir + '/Plotting/Middle_PWN', file_name_Plotting_Middle_PWN)
        ###
        file_name_Plotting_Middle_PWN2 = f'[{i}]_{PSR}_loglogplot_parameters_positrons.png'
        save_path_Plotting_Middle_PWN2 = os.path.join(save_dir + '/Plotting_Positrons/Middle_PWN', file_name_Plotting_Middle_PWN2)
        ###
        file_name_Plotting_Middle_PWN3 = f'[{i}]_{PSR}_loglogplot_parameters_Combined.png'
        save_path_Plotting_Middle_PWN3 = os.path.join(save_dir + '/Plotting_Combined/Middle_PWN', file_name_Plotting_Middle_PWN3)
        ###

        print('PSR = ', PSR, 'Age = ', td, 'Dist = ', d, 'Edot = ', edot)

##########
        print("Start Running MCMC for Middle PWN Case -- Find a drink while waiting")
        print("Test", i, ATNF_NamePSR_Cut_Milli[i], ATNF_Age_Cut_Milli[i], ATNF_Dist_Cut_Milli[i], ATNF_Edot_Cut_Milli[i])
        ##### The Emcee Fitting
        with Pool(processes=processes_cpu) as pool:
            sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, pool=pool)
            sampler.run_mcmc(p01, niter, progress=True);
        sampler_burned_in = sampler.flatchain[len(sampler.flatchain)//2:, :]
        samples = sampler.flatchain
        samples[np.argmax(sampler.flatlnprobability)]
        #####
        theta_max = samples[np.argmax(sampler.flatlnprobability)]
        gamma, e_cut, eta = [round(x, 4) for x in theta_max[:3]]
        ##### Results From Fitting
        print('gamma = ', gamma)
        print('e_cut = ', e_cut)
        print('eta  = ', eta)
        print('PWN at position 6 = ', np.real(pulsar(MockEnergy, eta, gamma, e_cut, edot, td, delta, d0, e0, d))[5])
        print('--------------------')
        theta_max = samples[np.argmax(sampler.flatlnprobability)]
        reducedchi_2_Middle = round(reducedchi2(theta_max), 4)
        reducedchi_2po_Middle = round(reducedchi2po(theta_max), 4)
        reducedchi_2_combine_Middle = round(reducedchi2_combine(theta_max), 4)
        print('reducedchi_2 = ', reducedchi_2_Middle)
        print('reducedchi_2po = ', reducedchi_2po_Middle)
	    print('reducedchi_2_combine_Middle = ', reducedchi_2_combine_Middle)
        ##### Write down parameters Fitting in dat file
        file.write(f'{ATNF_NamePSR_Cut_Milli[i]} \t {ATNF_Edot_Cut_Milli[i]} \t {ATNF_Age_Cut_Milli[i]} \t {ATNF_Dist_Cut_Milli[i]} \t {gamma:.2f} \t {e_cut:.2f} \t {eta:.2f} \t {eta*edot} \t {e_max(td).value:.2f} \t {reducedchi_2_Middle:.2f} \t {reducedchi_2po_Middle:.2f} \t {reducedchi_2_combine_Middle}\n')
        file.flush()
        print("Mean acceptance fraction: {0:.3f}".format(np.mean(sampler.acceptance_fraction)))
        print('==========================')
        ##### Corner Plot and Walker Steps
        ### Corner Plot
        flat_samples = sampler.get_chain(discard=discard_adjust(niter), thin=15, flat=True)
        labels = ['$\gamma$', '$E_{cut}$', '$\eta$']
        fig = corner.corner(flat_samples, labels=labels, show_titles=True, plot_datapoint=False, quantiles=[0.16, 0.5, 0.84], bins=30, plot_density=True, levels=(0.68, 0.95), smooth=1.2, smooth1d=1.2, truths=theta_max)
        plt.savefig(f'{save_path_CornerPlots_Middle_PWN}', dpi=300)
        plt.close()
        ### Walker Steps
        fig, axes = plt.subplots(len(initial1), figsize=(15, 30), sharex=True)
        sample = sampler.get_chain()
        for i in range(ndim):
            ax = axes[i]
            ax.plot(sample[:, :, i], 'k', alpha=1.0)
            ax.set_xlim(0, len(sample))
            ax.set_ylabel(labels[i])
            ax.yaxis.set_label_coords(-0.1, 1.0)
            axes[-1].set_xlabel('step number');
            plt.savefig(save_path_WalkerSteps_Middle_PWN, dpi=300)
        plt.close()

        ##### Log-Log Scale Plots
        ## Plot with fitting parameters -- CRs data

        phi_ams = 0.55
        slope = 3
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
        plt.plot(MockEnergy, np.real(pulsar(MockEnergy, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value), color='g', linestyle='-.', label={PSR}, markersize=0.01)
        plt.plot(MockEnergy, np.real(pulsar(MockEnergy, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value) + MockDRAGON2, 'g', label='Total', markersize=0.01)

        legend_title = rf"$\gamma$ = {gamma:.2f} $E_{{cut}}$ = {e_cut:.2f} $\eta$ = {eta:.2f} $\chi^2$ = {reducedchi_2_Middle:.2f}"

        lg = ax.legend(fontsize = 15, loc = 'upper right', ncol = 2, title =legend_title)
        lg.get_title().set_fontsize(20)

        ax.set_ylabel("$E^{3} \Phi_{e^{-}+e^{+}} \, (GeV^{2} \, s^{-1} \, m^{-2} \, sr^{-1})$", fontsize = 22, labelpad = 10)
        ax.set_xlabel("Energy (GeV)", fontsize = 24)
        ax.set_xlim(left = 10, right = 5000)
        ax.set_ylim(bottom = 1e0, top = 5000)
        ax.grid(color = '0.9', linestyle='-.', linewidth=1)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=18)
        #### Save Figure in Folder
        plt.savefig(save_path_Plotting_Middle_PWN, dpi=300)

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
        plt.plot(MockEnergy_5000, 0.5*np.real(pulsar(MockEnergy_5000, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value), color='g', linestyle='-.', label={PSR}, markersize=0.01)
        plt.plot(MockEnergy_5000, 0.5*np.real(pulsar(MockEnergy_5000, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value) + MockDRAGON2_po_5000, 'g', label='Total', markersize=0.01)

        legend_title = rf"$\gamma$ = {gamma:.2f} $E_{{cut}}$ = {e_cut:.2f} $\eta$ = {eta:.2f} $\chi^2$ = {reducedchi_2po_Middle:.2f}"

        lg = ax.legend(fontsize = 15, loc = 'upper right', ncol = 2, title =legend_title)
        lg.get_title().set_fontsize(20)

        ax.set_ylabel("$E^{3} \Phi_{e^{-}+e^{+}} \, (GeV^{2} \, s^{-1} \, m^{-2} \, sr^{-1})$", fontsize = 22, labelpad = 10)
        ax.set_xlabel("Energy (GeV)", fontsize = 24)
        ax.set_xlim(left = 10, right = 5000)
        ax.set_ylim(bottom = 1e0, top = 500)
        ax.grid(color = '0.9', linestyle='-.', linewidth=1)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=18)
        #### Save Figure in Folder
        plt.savefig(save_path_Plotting_Middle_PWN2, dpi=300)
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
        plt.plot(MockEnergy, np.real(pulsar(MockEnergy, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value), color='g', linestyle='-.', label={PSR}, markersize=0.01)
        plt.plot(MockEnergy_5000, 0.5*np.real(pulsar(MockEnergy_5000, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value), color='b', linestyle='--', label={PSR}, markersize=0.01)

        plt.plot(MockEnergy, np.real(pulsar(MockEnergy, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value) + MockDRAGON2, 'g', label='Total', markersize=0.01)

        #### CR Positron data
        plt.plot(MockEnergy_5000, 0.5*np.real(pulsar(MockEnergy_5000, gamma, e_cut, eta, edot, td, delta, d0, e0, d).value) + MockDRAGON2_po_5000, 'b', label='Total $e^{+}$', markersize=0.01)    


        legend_title2 = rf"$\gamma$ = {gamma:.2f} $E_{{cut}}$ = {e_cut:.2f} $\eta$ = {eta:.2f} $\chi^2$ = {reducedchi_2_combine_Middle:.2f}"

        lg = ax.legend(fontsize = 15, loc = 'upper right', ncol = 2, title=legend_title2)
        lg.get_title().set_fontsize(20)

        ax.set_ylabel("$E^{3} \Phi_{e^{-}+e^{+}} \, (GeV^{2} \, s^{-1} \, m^{-2} \, sr^{-1})$", fontsize = 22, labelpad = 10)
        ax.set_xlabel("Energy (GeV)", fontsize = 24)
        ax.set_xlim(left = 10, right = 5000)
        ax.set_ylim(bottom = 1e0, top = 20000)
        ax.grid(color = '0.9', linestyle='-.', linewidth=1)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=18)
        #### Save Figure in Folder
        plt.savefig(save_path_Plotting_Middle_PWN3, dpi=300)

        plt.close()
        sampler.reset()
        del sampler
file.close()
