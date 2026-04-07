# CREPE
Cosmic Ray Electron and Positron Excess - Using PWNe Model

Note: file name utils_CR.py adopts from PDL github --> https://github.com/tospines/ISAPP-school-2021_HandsOn-DRAGON2

------------------
Update 4Mar2026
------------------
- Run MCMC Fiiting (the emcee Python package) by using bash command in the terminal

- Bash files will create folders for keeping Results files

- Command for Single PWN Model [Adjust python Run_{...}_PWN_MCMC.py inside ./{...}.sh first]:

```
bash CREPE_Project_SinglePWN_Case.sh
```

- Command for Multiple PWNe Model:
```
bash CREPE_Project_MultiplePWNe_Case.sh
```

------------------
Design Structure Code
------------------
- Python Package Requirements
    - pandas - Dataframe
    - matplotlib
    - os
    - numpy
    - scipy - constants, integrate, interpolate
    - astropy - fits, unit, constants
    - emcee
    - corner
    - multiprocessing - Pool
    - unittest
    - utils_CR -- Credit: PDL github



| Process | Filename/Folder | Description  | Note |
| :---: | :---: | :--- | :--- |
| Input | CRs_data.py | Cosmic Ray Electron and Positron data - Database CRDBs | Credit: PDL GitHub |
|  | EnergyAll.py | Cosmic Ray Electron and Positron, Cosmic Ray Positron, and Background data | Data From Jounal |
|  | utils_CR.py | Cosmic Ray Electron and Positron Background Function using with DRAGON2 code | Credit: PDL github |
|  | ATNF_Pulsar_Catalogue_1kpc.py | Pulsar in 1 kpc -- Database ATNF pulsar Catalogue | /ATNF_Pulsar |
|  | CREPE_Mockdata.py | Mock Data For Plotting Process | Cosmic Rays, and Background using Interpolation function |
|  | CREPE_Constants.py | Parameters Constants using for calculations |  |
|  | CREPE_PWN_Equations.py | The Pulsar Wind Nebula (PWN) Model | Model For Fitting with data using MCMC Method |
|  | CREPE_Directory_Setup.py | Set up Directory path for the Results | For Single Young-Ages, Middle-Ages, and Old-Ages PWN Models |
|  | Fitting Parameters/, Corner Plots/ , WalkerSteps/ | Collect Results from Fitting in Results/ |  |
|  | Plotting/ | Collects Only Cosmic Ray Electron and Positron Plots |  | 
|  | Plotting_Positrons/ | Collects Only Cosmic Ray Positron Plots |  |
|  | Plotting_Combined/ | Collects Both Cosmic Ray Electron and Positron and Cosmic Ray Positron Plots |  |
| Method | CREPE_SinglePWN_Setup.py | Setup information for using in emcee fitting | The emcee Python Package |
|  | CREPE_SinglePWN_Boundaries_Setup.py | Setup Boundaries parameters for each cases of Single PWN |  |
|  | Run_Young_PWN_MCMC.py | Contains emcee code for fitting in loop functions | For Single Young-Ages PWN Model |
|  | Run_Middle_PWN_MCMC.py | Contains emcee code for fitting in loop functions | For Single Middle-Ages PWN Model |
|  | Run_Old_PWN_MCMC.py | Contains emcee code for fitting in loop functions | For Single Old-Ages PWN Model |
|  | CREPE_MultiPWNe_emcee_Setup.py | Setup information for using in emcee fitting | Multiple Pulsar Wind Nebulae Fitting Process |
|  | CREPE_MultiPWNe_emcee_Running.py | Contains emcee code for Fitting | Combines All PWNe in 1 kpc |
| Output | Results/ | Results_SinglePWN Folder | Collects Results and All plots from Fitting with emcee |
| Bash Setup | CREPE_Project_SinglePWN_Case.sh | Create Folders, python ./FittingFile.py | Command line: bash CREPE_Project_SinglePWN_Case.sh |
|  | CREPE_Project_MultiplePWNe_Case.sh | Create Folders, python ./FittingFile.py | Command line: bash CREPE_Project_MultiplePWNe_Case.sh |