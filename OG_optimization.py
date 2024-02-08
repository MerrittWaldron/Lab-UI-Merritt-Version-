# Written by Caitlin Keady, 2023

import os
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt


def optog(brand):
    rootdir = os.getcwd()
    os.chdir(r'../Tracking')
    
    abvdata = pd.read_excel('ABV Tracking.xlsx', 'Final Package')
    
    # Import ekos OG by batch report
    os.chdir(r'../Lab UI/input/og')
    
    for filename in os.listdir():
        if filename != 'README.md':
            og = pd.read_csv(filename)
    
    og = og.drop_duplicates()
    og = og.reset_index(drop=True)
    
    bybrand = abvdata[abvdata.Brand == brand]
    
    abvdata.iloc[:, 2] = abvdata['Batch'].astype(str)
    abvdata.iloc[:, 2] = abvdata.iloc[:, 2].str[:5]
    
    og['ABV'] = np.nan
    og['RDF'] = np.nan
    

    for i in np.arange(len(abvdata)):
        batchid = abvdata.iloc[i, 2]
        for j in np.arange(len(og)):
            if batchid in og.iloc[j, 0]:
                og.iloc[j, 4] = abvdata.iloc[i, 4]
                og.iloc[j, 5] = abvdata.iloc[i, 6]
    
    og = og.dropna()
    
    # Build equation RDF * OG = m * ABV + b
    x = og['ABV']
    y = (og['Original Gravity'] * 0.9584 - 0.2739) * og['RDF'] / 100
    og['RDFxOG'] = y
    
    og['Start Date'] = pd.to_datetime(og['Start Date'])
    d = datetime.today() - timedelta(days=365)
    current = og[(og['Start Date'] > d)]

    # Equation for data within the last year
    x = current['ABV']
    y = (current['Original Gravity'] * 0.9584 - 0.2739) * current['RDF'] / 100
    current['RDFxOG'] = y
        
    num = np.sum((x-np.mean(x))*(y - np.mean(y)))
    den = np.sum((x-np.mean(x))**2)
    
    m = num/den
    b = np.mean(y) - m*np.mean(x)
    
    avgrdf = np.mean(bybrand['RDF (%)'])/100
    
    if brand == 'IPA':
        abv = 6.9
    elif brand == 'COHZ':
        abv = 5.9
    elif brand == 'STAY':
        abv = 4.9
    elif brand == 'LRL':
        abv = 3.9
    elif brand == 'BLU':
        abv = 4.5
    
    # calculate target OG based on avg RDF and target ABV
    targetog = ((abv * m + b)/avgrdf + 0.2739) / 0.9584
    
    minrdf = ((abv - 0.3) * m + b)/(targetog * 0.9584 - 0.2739)
    maxrdf = ((abv + 0.3) * m + b)/(targetog * 0.9584 - 0.2739)
    
    rdf_range = 100 * round((maxrdf-minrdf)/2,2)
    
    # minog = ((abv * m + b)/maxrdf + 0.2739) / 0.9584
    # maxog = ((abv * m + b)/minrdf + 0.2739) / 0.9584
    
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams.update({'font.size': 10})
        
    plt.scatter(x, y)
    plt.plot(x, m*x+b, 'k')
    plt.xlabel('ABV')
    plt.ylabel('RDF*OG')
    plt.title(brand, fontweight='bold')
    plt.title(f'RDF = {np.round(100*avgrdf,2)} \u00B1 {rdf_range} %', loc='right')
    plt.title(f'Target OG = {np.round(targetog,2)} P', loc='left', color='red')

    os.chdir(rootdir)
    plt.savefig('plot', dpi=150)
    plt.close()
    
    # og['predABV'] = np.nan
    # og['predABV'] = (y - b) /m
    
    # plt.scatter(og['ABV'], og['predABV'])
    # plt.plot([min(og['ABV']), max(og['ABV'])], [min(og['ABV']), max(og['ABV'])], 'k')
    # plt.xlabel('Actual ABV')
    # plt.ylabel('Predicted ABV')
    # plt.title(f'{brand} Model Validation', fontweight='bold')
    
    # plt.savefig('plot2', dpi=150)
    # plt.close()
