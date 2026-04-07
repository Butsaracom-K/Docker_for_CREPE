import pandas as pd
from pandas import DataFrame
import numpy as np
import os

filename = '/CREPE_Dir/CREPE/Mockdata/'
os.makedirs(filename, exist_ok=True)
df_Mockdata = pd.read_excel(filename + 'Fakedata.xlsx', names=['Energy', 'BGDRAGON2'])

MockEnergy = np.array(df_Mockdata['Energy'])
MockDRAGON2 = np.array(df_Mockdata['BGDRAGON2'])

#################### Mock data 5000 GeV

df_Mockdata5000 = pd.read_excel(filename + 'Mockdata5000.xlsx', names=['Energy5000', 'BGDRAGON25000', 'BGDRAGON2_po_5000'])

MockEnergy_5000 = np.array(df_Mockdata5000['Energy5000'])
MockDRAGON2_5000 = np.array(df_Mockdata5000['BGDRAGON25000'])
MockDRAGON2_po_5000 = np.array(df_Mockdata5000['BGDRAGON2_po_5000'])

####
df_Mockdata7000 = pd.read_excel(filename + 'Mockdata7000.xlsx', names=['Energy7000', 'BGDRAGON27000', 'BGDRAGON2_po_7000'])

MockEnergy_7000 = np.array(df_Mockdata7000['Energy7000'])
MockDRAGON2_7000 = np.array(df_Mockdata7000['BGDRAGON27000'])
MockDRAGON2_po_7000 = np.array(df_Mockdata7000['BGDRAGON2_po_7000'])
