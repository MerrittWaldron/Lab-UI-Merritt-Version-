# Written by Caitlin Keady, 2023

import os
import pandas as pd
import numpy as np

rootdir = os.getcwd()
os.chdir(r'input/sensory')

num_tasters = 27

# Choose which tests are available
desc_test = 1
ttt_test = 1
hed_test = 1

for filename in os.listdir():
    if filename != 'README.md':
        if desc_test == 1:
            desc = pd.read_excel(filename, 'Description', skiprows=9, header=1)
        if ttt_test == 1:
            ttt = pd.read_excel(filename, 'TTT', skiprows=9, header=1)
        if hed_test == 1:
            hed = pd.read_excel(filename, 'Hedonic', skiprows=9, header=1)

if desc_test == 1:        
    tasters = desc['Name'].unique()
    panel = desc['Test Id'].unique()

if ttt_test == 1:
    tasters = np.unique(np.append(tasters, ttt['Name'].unique()))
    panel = np.unique(np.append(panel, ttt['Test Id'].unique()))

if hed_test == 1:
    tasters = np.unique(np.append(tasters, hed['Name'].unique()))
    panel = np.unique(np.append(panel, hed['Test Id'].unique()))

if desc_test == 1:
    test_summary = desc[['Test Id', 'Panel Name']].copy()
    
if ttt_test == 1:
    test_summary = test_summary.append(ttt[['Test Id', 'Panel Name']].copy())
    
if hed_test == 1:
    test_summary = test_summary.append(hed[['Test Id', 'Panel Name']].copy())
    
test_summary = test_summary.drop_duplicates(subset=['Test Id'])

name_count = []
desc_count = 0
ttt_count = 0
hed_count = 0

for name in tasters:
    if desc_test == 1:
        desc_count = len(desc[desc['Name'] == name]['Test Id'].unique())
    if ttt_test == 1:
        ttt_count = len(ttt[ttt['Name'] == name]['Test Id'].unique())
    if hed_test == 1:
        hed_count = len(hed[hed['Name'] == name]['Test Id'].unique())
    
    name_count = np.append(name_count, desc_count + ttt_count + hed_count)

name_summary = pd.DataFrame(data = {'Tasters': tasters, 'Tests': name_count})        
     
panel_count = []
desc_count = 0
ttt_count = 0
hed_count = 0

for test in panel:
    if desc_test == 1:
        desc_count = len(desc[desc['Test Id'] == test]['Name'].unique())
    if ttt_test == 1:
        ttt_count = len(ttt[ttt['Test Id'] == test]['Name'].unique())
    if hed_test == 1:
        hed_count = len(hed[hed['Test Id'] == test]['Name'].unique())
    
    panel_count = np.append(panel_count, desc_count + ttt_count + hed_count)
    
test_summary['Tasters'] = panel_count
test_summary['% complete'] = panel_count/num_tasters

test_index = len(test_summary.index)
total_tasters = sum(test_summary['Tasters'])
total_perc = total_tasters/(num_tasters*(test_index))

test_summary.loc[test_index] = ['Total', 'Total', total_tasters, total_perc]

os.chdir(rootdir)
