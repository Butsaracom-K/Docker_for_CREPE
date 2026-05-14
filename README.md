# Automated-Data-Processing-Workflow-with-Docker Project

# Dockerized Scientific Data Processing Workflow

A containerized Python workflow for automated scientific data processing, parallel execution, and reproducible analytical pipelines using Docker, Bash, and multiprocessing.

This project demonstrates:
- Workflow automation with Bash
- Reproducible environments using Docker
- Parallel data processing using multiprocessing
- Structured result and output management
- Modular scientific data analysis pipelines

Originally developed for computational astrophysics research workflows.

--------------------------------------

## Technologies Used

- Python
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
- Docker
- Bash
- Linux
- Git

---------------------------------------

I have 2 options for you to build a Docker container

For Build Docker 

# Option 1: [Self adjust]

- Before running the command, please install Docker first

   - check the version of Docker

```
Docker --version
```

- Build Docker image [Self type -- feel free to name the Docker image]:

- Command:
```
docker build -t crepe/ubuntu.22 .
```

# Option 2: [Build Automation - Using Bash Script]
## Follow the Steps! [Build, Run and Access for the 1st time, and Access again next time]
- Command 1 [Build Docker]:
```
bash build-docker-command.sh
```

-------------------------------------------
# For Access into Docker

- Command 2 [Run Docker Image]:
```
bash run-docker-after-build-image.sh
```

* after access for the 1st time, please run bash script to update and upgrade before run the project's code:
```
bash run-script-Inside_Docker-firsttime.sh 
```

Note: If you want to exit from Docker, please type:
```
exit
```

-------------------------------------------
# For Access next time

- Command 3 [Access again next time [Container ID]!]:
```
bash access-docker-daily-use.sh
```

*Next, please follow the steps below to run the project's code

#Inside Docker
--------------------------
For running using bash:

- This project has two models:

    - A Single Pulsar Wind Nebula Model

- Command:
```
bash CREPE_Project_SinglePWN_Case.sh
```

Note: Don't forget to input requirements (nwalker steps, niter, processing_cpu for multiprocessing, and pulsar popoulation cases)

- The Multiple Pulsar Wind Nebulae Model:

- Command:
```
bash CREPE_Project_MultiplePWNe_Case.sh
```

Note: Don't forget to input requirements (nwalker steps, niter, and processing_cpu for multiprocessing)

-----------------------------------------

------------------
Update April 7, 2026
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

-----------------------

```mermaid
graph TD

    subgraph Input ["1. Input & Resources"]
        direction TB
        A1[CRs_data.py / spectrum.py<br/>Collects data]
        A2[utils_CR.py / constants.py<br/>Background & Parameters]
        A3[ATNF_Pulsar_Catalogue_1kpc.py<br/>Pulsar Database]
        A4[equations.py<br/>PWN Model Equations]
        A5[mockdata.py<br/>Mock Data for Interpolation]
        A6[directory & Output Paths<br/>Fitting, Plots, Results]
    end

    subgraph Bash ["0. Automation Setup"]
        B1[CREPE_Project_SinglePWN_Case.sh]
        B2[CREPE_Project_MultiplePWNe_Case.sh]
    end

    subgraph Method ["2. Processing & Fitting (emcee)"]
        direction TB
        M1[single_PWN_setup.py<br/>Boundaries & emcee Config]
        subgraph Single ["Single PWN Models"]
            S1[run_young_PWN_MCMC.py]
            S2[run_middle_PWN_MCMC.py]
            S3[run_old_PWN_MCMC.py]
        end

        subgraph Multi ["Multiple PWNe Models"]
            M2[multiple_PWNe_emcee_setup.py]
            M3[multiple_PWNe_emcee_running.py]
        end
    end

    subgraph Output ["3. Results & Visualization"]
        O1[(Results/ Folder)]
        O2[Current Date]
        O3[Fitting_Parameters]
        O4[Corner Plots / Walker Steps]
        O5[Cosmic Ray & Positron Plots]
    end

    %% Relationships
    B1 --> M1
    B2 --> M2
    A1 & A2 & A3 & A4 --> M1 & M2
    M1 --> S1 & S2 & S3
    M2 --> M3
    S1 & S2 & S3 & M3 --> O1
    O1 --> O2 & O3 & O4 & O5
```

------------------------------------