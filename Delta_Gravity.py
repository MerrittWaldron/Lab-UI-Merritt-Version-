# Written by Caitlin Keady, 2023

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def deltagrav(brand_input):
    rootdir = os.getcwd()
    os.chdir(r'../Tracking')
    
    final = pd.read_excel('ABV Tracking.xlsx', 'Final Gravity')
    pack = pd.read_excel('ABV Tracking.xlsx', 'Final Package')
    lib = pd.read_excel('ABV Tracking.xlsx', 'Library')
    
    final_brand = final[final.Brand == brand_input]
    pack_brand = pack[pack.Brand == brand_input]
    lib_brand = lib[lib.Brand == brand_input]
    
    final_brand = final_brand.rename(columns={'Plato (P\N{degree sign})': 'finalG'})
    pack_brand = pack_brand.rename(columns={'Plato (P\N{degree sign})': 'packG'})
    lib_brand = lib_brand.rename(columns={'Plato (P\N{degree sign})': 'libG'})
    
    for i in np.arange(len(pack_brand)):
        if isinstance(pack_brand.iloc[i, 2], str):
            pack_brand.iloc[i, 2] = int(pack_brand.iloc[i, 2][:5])
            
    for i in np.arange(len(lib_brand)):
        if isinstance(lib_brand.iloc[i, 2], str):
            lib_brand.iloc[i, 2] = int(lib_brand.iloc[i, 2][:5])
    
    brand = final_brand[['Brand', 'Batch', 'finalG']]
    brand = pd.merge(brand, pack_brand[['packG', 'Batch']], on='Batch', how='left')
    brand = pd.merge(brand, lib_brand[['libG', 'Batch']], on='Batch', how='left')
    
    last_ten = brand.tail(10)
    
    final_mean = np.mean(brand.finalG)
    pack_mean = np.mean(brand.packG)
    lib_mean = np.mean(brand.libG)
    
    final_sd = np.std(brand.finalG)
    pack_sd = np.std(brand.packG)
    lib_sd = np.std(brand.libG)
    
    bars = plt.bar(['Final Gravity', 'Pack Gravity', 'Lib Gravity'], 
                   [final_mean, pack_mean, lib_mean], yerr=[final_sd, pack_sd, lib_sd],
                   align='center', alpha=0.5, ecolor='black', capsize=10)
    plt.bar_label(bars, label_type='center')
    plt.ylabel('Gravity (\N{degree sign}P)')
    plt.title(f'Gravity changes since DTest: {brand_input}')
    
    plt.show()
    plt.close()
    
    for i in np.arange(len(last_ten)):
        plt.plot(['Final Grav', 'Pack Grav'], [last_ten.iloc[i,2], last_ten.iloc[i,3]], label=last_ten.iloc[i,1])
    
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.ylabel('Gravity (\N{degree sign}P)')
    plt.title(f'Gravity changes since DTest: {brand_input}')
    
    os.chdir(rootdir)
