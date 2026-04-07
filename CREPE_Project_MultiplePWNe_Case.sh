#!/bin/bash

cd CREPE/
mkdir -p Results/
cd Results/
mkdir Multiple_PWNe
cd Multiple_PWNe
mkdir -p "$(date +%Y-%m-%d)"
cd "$(date +%Y-%m-%d)"

export current_date="$(date +%Y-%m-%d)"


mkdir -p FittingParameters
mkdir -p CornerPlots
mkdir -p WalkerSteps
mkdir -p Plotting
mkdir -p Plotting_Positrons
mkdir -p Plotting_Combined

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

echo 'Waiting for a moment, take some coffee!'
####################

python3 multiple_PWNe_emcee_running.py Multiple_PWNe $niter_setup $nwalkers_setup $processes_cpu

echo 'Fitting Results are done!'
