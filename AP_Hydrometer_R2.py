# Written by Caitlin Keady, 2023

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.chdir(r'input/fermlog')

for filename in os.listdir():
    if filename != 'README.md':
        fermlog = pd.read_csv(filename, names=['Date', 'Location', 'Gravity', 'pH', 'Temp', 'ABV', 'Start', 'Brand', 'Batch'], 
                              header=1)

os.chdir(r'../../../../Documents - Brewery Operations/Lab/Tracking')

antonpaar = pd.read_excel('ABV Tracking.xlsx', 'Final Gravity')
target = pd.read_excel('ABV Tracking.xlsx', 'abv targets')

fermlog['Days'] = np.nan
fermlog['BrandCode'] = np.nan
antonpaar['NewBatch'] = np.nan

# Format dates from Ekos import
antonpaar['Date'] = pd.to_datetime(antonpaar['Date']).dt.strftime('%m/%d/%Y')
fermlog['Date'] = pd.to_datetime(fermlog['Date']).dt.strftime('%m/%d/%Y')

for i in np.arange(len(fermlog)):
    fermlog.iloc[i, 10] = fermlog['Batch'][i].split(' ', 1)[0]
    
for i in np.arange(len(antonpaar)):
    antonpaar.iloc[i, 9] = str(antonpaar['Batch'][i]).split('-', 1)[0]
for i in np.arange(len(antonpaar)):
    antonpaar.iloc[i, 9] = str(antonpaar['NewBatch'][i]).split('/', 1)[0]
for i in np.arange(len(antonpaar)):
    antonpaar.iloc[i, 9] = str(antonpaar['NewBatch'][i]).split('.', 1)[0]
    
batches = fermlog.Batch.unique()

for i in np.arange(len(fermlog)):
    fermlog.iloc[i, 7] = fermlog.iloc[i, 7].lower()

brand_code = target['Brand Code']
ap = []
hydrom = []

for i in np.arange(len(brand_code)):
    abv_by_brand = antonpaar[antonpaar.Brand == brand_code[i]]
    abv_by_brand.reset_index(drop=True, inplace=True)
    
    ekos_by_brand = fermlog[fermlog.BrandCode == brand_code[i]]
    ekos_by_brand = ekos_by_brand[~ekos_by_brand['Batch'].str.contains('\\.')]
    ekos_by_brand = ekos_by_brand[ekos_by_brand['Gravity'] != '0']
    ekos_by_brand.reset_index(drop=True, inplace=True)

    for j in np.arange(len(abv_by_brand)):
        for k in np.arange(len(ekos_by_brand)):
            if abv_by_brand['NewBatch'][j] in ekos_by_brand['Batch'][k]:
                if abv_by_brand['Date'][j] == ekos_by_brand['Date'][k]:
                    if len(str(float(ekos_by_brand['Gravity'][k])).split('.', 1)[1]) == 1:
                        ap = np.append(ap, abv_by_brand['Plato (P°)'][j])
                        hydrom = np.append(hydrom, ekos_by_brand['Gravity'][k])

hydrom = hydrom.astype(float)
gravity = pd.DataFrame({'AntonPaar': ap, 'Hydrometer': hydrom})
gravity['AP_rounded'] = ap.round(1)

gravity = gravity[(gravity > 0).all(1)]

rmse = np.sqrt(((gravity['Hydrometer'] - gravity['AP_rounded']) ** 2).mean())

plt.rcParams['figure.dpi'] = 300
plt.scatter(gravity['AP_rounded'], gravity['Hydrometer'])
plt.plot([0, max(ap)], [0, max(ap)], 'k')
plt.xlabel('Anton Paar reading (°P)')
plt.ylabel('Hydrometer reading (°P)')
plt.title(f'Gravity Comparison: RMSE = {round(rmse, 3)}')
plt.show()
