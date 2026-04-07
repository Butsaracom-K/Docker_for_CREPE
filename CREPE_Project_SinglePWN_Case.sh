#!/bin/bash

cd CREPE/
mkdir -p Results/
cd Results/
mkdir Single_PWN
cd Single_PWN
mkdir -p "$(date +%Y-%m-%d)"
cd "$(date +%Y-%m-%d)"

export current_date="$(date +%Y-%m-%d)"

#################################
mkdir -p FittingParameters/Young_PWN
mkdir -p CornerPlots/Young_PWN
mkdir -p WalkerSteps/Young_PWN
mkdir -p Plotting/Young_PWN
mkdir -p Plotting_Positrons/Young_PWN
mkdir -p Plotting_Combined/Young_PWN

mkdir -p FittingParameters/Middle_PWN
mkdir -p CornerPlots/Middle_PWN
mkdir -p WalkerSteps/Middle_PWN
mkdir -p Plotting/Middle_PWN
mkdir -p Plotting_Positrons/Middle_PWN
mkdir -p Plotting_Combined/Middle_PWN

mkdir -p FittingParameters/Old_PWN
mkdir -p CornerPlots/Old_PWN
mkdir -p WalkerSteps/Old_PWN
mkdir -p Plotting/Old_PWN
mkdir -p Plotting_Positrons/Old_PWN
mkdir -p Plotting_Combined/Old_PWN

cd ..
cd ..
cd ..

echo 'Folder has been created successfully'

## Adjust nwalkerSteps and niter for emcee Fitting
echo 'Please enter your nwalkers_step number [eg. 128]:'
read nwalkers_setup

echo 'Please enter your niter number [eg. 100 or 1000]:'
read niter_setup

## Adjust Processing -- [Check your CPU performance]
echo 'Please enter your processes_cpu number [eg. 16 -- Check your laptop performance]:'
read processes_cpu

echo 'Which pulsar population do you want to run fitting? [young/middle/old/all]'
read pulsar_pop

echo 'Waiting for a moment, take some coffee!'

########
if [ "$pulsar_pop" == "young" ]; then
    python3 run_young_PWN_MCMC.py Single_PWN $nwalkers_setup $niter_setup $processes_cpu
elif ["$pulsar_pop" == "middle" ]; then
    python3 run_middle_PWN_MCMC.py Single_PWN $nwalkers_setup $niter_setup $processes_cpu
elif ["$pulsar_pop" == "old" ]; then
    python3 run_old_PWN_MCMC.py Single_PWN $nwalkers_setup $niter_setup $processes_cpu
elif ["$pulsar_pop" == "all" ]; then
    python3 run_young_PWN_MCMC.py Single_PWN $nwalkers_setup $niter_setup $processes_cpu
    python3 run_middle_PWN_MCMC.py Single_PWN $nwalkers_setup $niter_setup $processes_cpu
    python3 run_old_PWN_MCMC.py Single_PWN $nwalkers_setup $niter_setup $processes_cpu
else
    echo 'error: invalid input'
fi

echo 'Fitting Results are done!'
