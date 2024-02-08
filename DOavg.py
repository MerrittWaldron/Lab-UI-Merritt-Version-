# Written by Caitlin Keady, 2023

import pandas as pd
import os
import numpy as np

rootdir = os.getcwd()
os.chdir(r'input/condlog')

for filename in os.listdir():
    if filename != 'README.md':
        condlog = pd.read_csv(filename, names=['Batch', 'Date', 'bbls', 'Carb', 'CO2', 'DO', 'SetPoint', 'Temp'], header=0)


condlog[['Brand', 'Batch']] = condlog['Batch'].str.split(' ', 1, expand=True)

condlog.Batch = condlog['Batch'].str.split(' ', 1, expand=True)[0]

firstcol = condlog.pop('Brand')
condlog.insert(0, 'Brand', firstcol)
condlog = condlog[condlog['DO'].notna()]
condlog = condlog[condlog['DO'] != 0]

#condlog.to_csv(r'C:/Users/caitlin/Downloads/CondLog.csv', index=False)

condlog['Type'] = ''

for i in np.arange(len(condlog)):
    if condlog['Brand'].iloc[i] in ['STAY', 'LRL', 'OKT', 'MU2C', 'LIL']:
        condlog['Type'].iloc[i] = 'lager'
    else:
        condlog['Type'].iloc[i] = 'ale'
    
ales =  condlog[condlog['Type'] == 'ale']
lagers =  condlog[condlog['Type'] == 'lager']

DOavg_ale = np.mean(ales['DO'])
DOavg_lag = np.mean(lagers['DO'])

DOsd_ale = np.std(ales['DO'])
DOsd_lag = np.std(lagers['DO'])