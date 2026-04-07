import pandas as pd
from pandas import DataFrame
import os

############################
# Changes the File Directory
############################

filename = '/CREPE_Dir'
os.makedirs(filename, exist_ok=True)

## ATNF Pulsar Catalogue
ATNFPular_file_Cut_Milli = pd.read_excel(filename + '/CREPE/ATNF_Pulsar/ATNF2024Pulsar_All1kpc_CutMillisecondPulsar.xlsx', 
                               names=['PSR', 'Distance', 'Age', 'Edot', 'P0', 'P1'])

ATNFPular_file_Cut_Milli_OldMiddleMilli = pd.read_excel(filename +'/CREPE/ATNF_Pulsar/ATNF2024Pulsar_All1kpc_CutMillisecondPulsar.xlsx', sheet_name="Sheet2" , 
                               names=['PSR', 'Distance', 'Age', 'Edot', 'P0', 'P1'])

ATNFPular_file_Only_Milli = pd.read_excel(filename + '/CREPE/ATNF_Pulsar/ATNF2024Pulsar_All1kpc_OnlyMillisecondPulsar.xlsx', 
                               names=['PSR', 'Distance', 'Age', 'Edot', 'P0', 'P1', 'Note'])

ATNF_NamePSR_Cut_Milli = ATNFPular_file_Cut_Milli['PSR']
ATNF_Dist_Cut_Milli = ATNFPular_file_Cut_Milli['Distance']
ATNF_Age_Cut_Milli = ATNFPular_file_Cut_Milli['Age']
ATNF_Edot_Cut_Milli = ATNFPular_file_Cut_Milli['Edot']
ATNF_P0_Cut_Milli = ATNFPular_file_Cut_Milli['P0']
ATNF_P1_Cut_Milli = ATNFPular_file_Cut_Milli['P1']

ATNF_NamePSR_Cut_Milli_OldMiddleMilli = ATNFPular_file_Cut_Milli_OldMiddleMilli['PSR']
ATNF_Dist_Cut_Milli_OldMiddleMilli = ATNFPular_file_Cut_Milli_OldMiddleMilli['Distance']
ATNF_Age_Cut_Milli_OldMiddleMilli = ATNFPular_file_Cut_Milli_OldMiddleMilli['Age']
ATNF_Edot_Cut_Milli_OldMiddleMilli = ATNFPular_file_Cut_Milli_OldMiddleMilli['Edot']
ATNF_P0_Cut_Milli_OldMiddleMilli = ATNFPular_file_Cut_Milli_OldMiddleMilli['P0']
ATNF_P1_Cut_Milli_OldMiddleMilli = ATNFPular_file_Cut_Milli_OldMiddleMilli['P1']

ATNF_NamePSR_Only_Milli = ATNFPular_file_Only_Milli['PSR']
ATNF_Dist_Only_Milli = ATNFPular_file_Only_Milli['Distance']
ATNF_Age_Only_Milli = ATNFPular_file_Only_Milli['Age']
ATNF_Edot_Only_Milli = ATNFPular_file_Only_Milli['Edot']
ATNF_P0_Only_Milli = ATNFPular_file_Only_Milli['P0']
ATNF_P1_Only_Milli = ATNFPular_file_Only_Milli['P1']
ATNF_Note_Only_Milli = ATNFPular_file_Only_Milli['Note']

## Call Pulsar Collection in MCMC
Young_Aged_PWNe_Cut_Milli = ATNFPular_file_Cut_Milli.query('Age <= 100000')
Middle_Aged_PWNe_Cut_Milli = ATNFPular_file_Cut_Milli.query('100000 < Age <= 10000000')
#Middle_Aged_PWNe_Cut_Milli_OldMilli = ATNFPular_file_Cut_Milli_OldMiddleMilli.query('100000 < Age <= 10000000')
Old_Aged_PWNe_Cut_Milli = ATNFPular_file_Cut_Milli.query('Age > 10000000')

Young_Aged_PWNe_Only_Milli = ATNFPular_file_Only_Milli.query('Age <= 100000')
Middle_Aged_PWNe_Only_Milli = ATNFPular_file_Only_Milli.query('100000 < Age <= 10000000')
Old_Aged_PWNe_Only_Milli = ATNFPular_file_Only_Milli.query('Age > 10000000')

### [0:237]

'''
## ATNF Pulsar Catalogue
ATNFPular_file_Cut_Milli_Old = pd.read_excel('/app/CREPE/ATNF_Pulsar/ATNF2024Pulsar_All1kpc_CutMillisecondPulsar_Old.xlsx', 
                               names=['PSR', 'Distance', 'Age', 'Edot', 'P0', 'P1'])

ATNF_NamePSR_Cut_Milli_Old = ATNFPular_file_Cut_Milli_Old['PSR']
ATNF_Dist_Cut_Milli_Old = ATNFPular_file_Cut_Milli_Old['Distance']
ATNF_Age_Cut_Milli_Old = ATNFPular_file_Cut_Milli_Old['Age']
ATNF_Edot_Cut_Milli_Old = ATNFPular_file_Cut_Milli_Old['Edot']
ATNF_P0_Cut_Milli_Old = ATNFPular_file_Cut_Milli_Old['P0']
ATNF_P1_Cut_Milli_Old = ATNFPular_file_Cut_Milli_Old['P1']

## Call Millisecond Old-Ages Pulsar Collection in MCMC
Old_Aged_PWNe_Cut_Milli_Old = ATNFPular_file_Cut_Milli_Old.query('Age > 10000000')


#ATNF_NamePSR = ATNFPular_file_Cut_Milli['PSR']
#ATNF_Dist = ATNFPular_file_Cut_Milli['Distance']
#ATNF_Age = ATNFPular_file_Cut_Milli['Age']
#ATNF_Edot = ATNFPular_file_Cut_Milli['Edot']

'''
