# Written by Caitlin Keady, 2024

import os
import pandas as pd
import numpy as np
import xlsxwriter
import re
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt


def batchreport(batch):
    batch = int(batch)
    
    rootdir = os.getcwd()
    
    # GET ABV AND GRAVITY DATA
    os.chdir(r'../Tracking')
    
    final = pd.read_excel('ABV Tracking.xlsx', 'Final Gravity')
    pack = pd.read_excel('ABV Tracking.xlsx', 'Final Package')
    lib = pd.read_excel('ABV Tracking.xlsx', 'Library')
    
    final = final.drop(final.columns[[7, 8]], axis=1) 
    pack = pack.drop(pack.columns[[5, 8, 9, 11, 12, 13]], axis=1) 
    lib = lib.drop(lib.columns[[5, 8, 9, 11, 12]], axis=1) 
    
    pack['Batch'] = pack['Batch'].astype(str)
    lib['Batch'] = lib['Batch'].astype(str)
    
    final['Sample Date'] = final['Sample Date'].astype(str)
    pack['Sample Date'] = pack['Sample Date'].astype(str)
    lib['Brew Date'] = lib['Brew Date'].astype(str)
    
    batch_final = final[final.Batch == batch]
    batch_pack = pack[pack['Batch'].str.contains(str(batch))]
    batch_lib = lib[lib['Batch'].str.contains(str(batch))]
    
    batch_final = batch_final.drop(batch_final.columns[[0, 2]], axis=1) 
    batch_pack = batch_pack.drop(batch_pack.columns[[0, 2]], axis=1) 
    batch_lib = batch_lib.drop(batch_lib.columns[[0, 2]], axis=1) 
    
    
    
    
    # GET MICRO DATA
    micro = pd.read_excel('Micro Results Tracking.xlsx', 'Data')
    micro = micro.drop(micro.columns[[5, 6, 8, 9, 10, 11, 12, 13, 20, 21, 22, 23]], axis=1) 
    print('MICROORG',micro)

    batch_micro = micro[micro.Batch == batch]
    print('MICRO',batch_micro)
    brewdate = batch_micro.iloc[0,2]
    
    batch_micro['Test Date'] = batch_micro['Test Date'].astype(str)
    
    week = brewdate - timedelta(days=brewdate.weekday()) - timedelta(days=1)
    weekdate = week.strftime('%m.%#d.%y').lstrip('0')
    
    batch_micro = batch_micro.drop(micro.columns[[0, 1, 2]], axis=1)
    
    
    
    
    # GET BREWSHEETS
    os.chdir(r"../../Brewery and Cellar/Brewing Logs/Old Brewing Logs")
    brewsheet = pd.read_excel(f"Week of {weekdate}.xlsx", sheet_name=None, header=None)
        
    brewsheet = {k: v for k, v in brewsheet.items() if str(batch) in k}
    
    brewsheet1 = list (brewsheet.values())[0]
    brewsheet1 = brewsheet1.fillna('')
    brewsheet1 = brewsheet1.astype(str)
    brewsheet2 = None
    
    if len(brewsheet) == 2:
        brewsheet2 = list (brewsheet.values())[1]
        brewsheet2 = brewsheet2.fillna('')
        brewsheet2 = brewsheet2.astype(str)
    
    batch_size = int(re.findall(r'\d+', list (brewsheet.keys())[0])[1])
    
    brand = brewsheet1.iloc[0,4][0:3].upper()
    
    os.chdir(rootdir)
    
    
    
    # GET FERM DATA
    os.chdir(r'input/fermlog')
    
    for filename in os.listdir():
        if filename != 'README.md':
            fermdata = pd.read_csv(filename, names=['Date', 'Location', 'Gravity', 'pH', 'Temp', 'ABV',
                                                'Start', 'Brand', 'Batch'], header=0)
    
    fermdata['Days'] = np.nan
    
    fermdata['Sample Date'] = pd.to_datetime(fermdata['Sample Date']).dt.strftime('%m/%d/%Y')
    fermdata = fermdata[fermdata['Gravity'] != 0]
    fermdata = fermdata[~fermdata['Batch'].str.contains('\\.')]
    
    # Calculate days since start of brew
    for i in np.arange(len(fermdata)):
        t2 = datetime.strptime(fermdata.iloc[i, 6].split(" ", 1)[0].strip(), "%m/%d/%Y")
        t1 = datetime.strptime(fermdata.iloc[i, 0], "%m/%d/%Y")
        fermdata.iloc[i, 9] = (t1 - t2).days + 1
    
    for i in np.arange(len(fermdata)):
        fermdata.iloc[i, 7] = fermdata.iloc[i, 7].lower()
        
    batch_ferm = fermdata[fermdata['Batch'].str.contains(str(batch), na=True)]
    
    batch_grav = batch_ferm[batch_ferm['Batch'].str.contains(str(batch))]['Gravity']
    batch_days = batch_ferm[batch_ferm['Batch'].str.contains(str(batch))]['Days']
    batch_grav = batch_grav.astype(float)
    batch_days.reset_index(drop=True, inplace=True)
    batch_grav.reset_index(drop=True, inplace=True)
    
    # Filter by brand
    by_brand = fermdata[fermdata['Batch'].str.contains(brand)]
    by_brand = by_brand[~by_brand['Batch'].str.contains(r'\.')]
    by_brand = by_brand[by_brand['Gravity'] != '0']
    
    # Calculate average gravity by day
    days = np.arange(max(by_brand.Days) + 1)
    all_days = []
    avg_grav = []
    sd_grav = []
    
    
    for d in np.arange(max(days) + 1):
        all_days = np.append(all_days, d)
        grav1 = by_brand[by_brand.Days == d].iloc[:, 2].astype(float)
        if len(grav1) > 0:
            avg_grav = np.append(avg_grav, np.mean(grav1))
            sd_grav = np.append(sd_grav, np.std(grav1))
        else:
            avg_grav = np.append(avg_grav, np.nan)
            sd_grav = np.append(sd_grav, np.nan)
           
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams.update({'font.size': 10})
    
    plt.plot(all_days, avg_grav, color='k')
    plt.plot(all_days, avg_grav + sd_grav, color='k', linestyle='dashed', linewidth=1)
    plt.plot(all_days, avg_grav - sd_grav, color='k', linestyle='dashed', linewidth=1)
    plt.scatter(by_brand.Days, by_brand.Gravity.astype(float), color='silver')
    plt.title(f'{brand} {batch}')
    plt.xlim([0, max(all_days)])
    plt.xlabel('Days')
    plt.ylabel('Gravity (\N{degree sign} Plato)')
    
    for j in np.arange(len(batch_days)):
        d = int(batch_days[j])
        if avg_grav[d] + sd_grav[d] > batch_grav[j] > avg_grav[d] - sd_grav[d]:
            c = 'limegreen'
        else:
            c = 'red'
        plt.scatter(batch_days[j], batch_grav[j], color=c)
    
    os.chdir(rootdir)
            
    plt.savefig('fermplot', dpi=200)
    plt.close()
            
    batch_ferm = batch_ferm.drop(batch_ferm.columns[[1, 5, 6, 7, 8]], axis=1)
    
    
    
    # BRITE DO DATA
    os.chdir(r'input/condlog')
    
    for filename in os.listdir():
        if filename != 'README.md':
            condlog = pd.read_csv(filename, names=['Batch', 'Completion Date', 'bbls', 'Carb', 'CO2', 'DO', 'SetPoint', 'Temp'], header=0)
    
    for i in np.arange(len(condlog)):
        condlog.iloc[i, 0] = condlog.iloc[i, 0].upper()
    
    batch_do = condlog[condlog['Batch'].str.contains(str(batch))]
    batch_do = batch_do[batch_do['DO'].notna()]
    batch_do = batch_do[batch_do['DO'] != 0]
    batch_do.reset_index(drop=True, inplace=True)
    
    batch_do = batch_do.drop(batch_do.columns[[3]], axis=1)
    
    
    
    # CAN DO DATA
    os.chdir(r'../../../Tracking')
    
    can_do = pd.read_excel('CFT DO Tracking.xlsx', 'Can Data')
    can_do['Batch'] = can_do['Batch'].astype(str)
    can_do['Completion Date'] = can_do['Completion Date'].astype(str)
    
    can_do = can_do[can_do['Batch'].str.contains(str(batch))]
    
    grouped = can_do.groupby(['Batch', 'Eq.'], as_index=False)
    avg_do = grouped.mean()
    
    can_do = can_do.drop(can_do.columns[[0, 8, 9, 11, 12]], axis=1)
    avg_do = avg_do.drop(avg_do.columns[[2, 3, 7, 8, 10]], axis=1)
    
    
    
    # WRITE TO EXCEL WORKBOOK
    os.chdir(rootdir)
    workbook = xlsxwriter.Workbook('BatchReport.xlsx')
    
    tab1 = workbook.add_worksheet('Batch Data')
     
    tab1.write('A1', 'Batch')
    tab1.write('B1', 'Brand')
    tab1.write('C1', 'Brew Date')
    tab1.write('D1', 'Batch Size')
    tab1.write('A2', batch)
    tab1.write('B2', brand)
    tab1.write('C2', brewdate.strftime('%m/%d/%y'))
    tab1.write('D2', batch_size)
    
    tab1.write('A7', 'Final')
    tab1.write('A8', 'Package')
    tab1.write('A9', 'Library')
    
    tab1.write('A5', 'ABV Data')
    
    start = 5
    
    for idx, header in enumerate(batch_final):
        tab1.write(start, idx+1, header)
        try:
            for i in np.arange(len(batch_final)):
                tab1.write(start+1+i, idx+1, batch_final.iloc[i,idx])
        except:
            pass
        
    for idx, header in enumerate(batch_pack):
        try:
            for i in np.arange(len(batch_pack)):
                tab1.write(start+2+i, idx+1, batch_pack.iloc[i,idx])
        except:
            pass
    
    for idx, header in enumerate(batch_lib):
        try:
            for i in np.arange(len(batch_lib)):
                tab1.write(start+3+i, idx+1, batch_lib.iloc[i,idx])
        except:
            pass    
    
    tab1.write(start+6, 0, 'Micro')
    
    for idx, header in enumerate(batch_micro):
        tab1.write(start+7, idx, header)
        try:
            for i in np.arange(len(batch_micro)):
                tab1.write(start+8+i, idx, batch_micro.iloc[i,idx])
        except:
            pass
        
    tab1.write(start+12, 0, 'Ferm Log Data')
    
    for idx, header in enumerate(batch_ferm):
        tab1.write(start+13, idx, header)
        try:
            for i in np.arange(len(batch_ferm)):
                tab1.write(start+14+i, idx, batch_ferm.iloc[i,idx])
        except:
            pass
    
    tab1.insert_image(3, 15, 'fermplot.png')
    
    
    start = start+16+len(batch_ferm)
    
    tab1.write(start, 0, 'Brite DO Data')
    
    for idx, header in enumerate(batch_do):
        tab1.write(start+1, idx, header)
        try:
            for i in np.arange(len(batch_do)):
                tab1.write(start+2+i, idx, batch_do.iloc[i,idx])
        except:
            pass
    
    
    
    start = start+4+len(batch_do)
    
    tab1.write(start, 0, 'Can DO Data')
    
    for idx, header in enumerate(can_do):
        tab1.write(start+1, idx, header)
        try:
            for i in np.arange(len(can_do)):
                try:
                    tab1.write(start+2+i, idx, can_do.iloc[i,idx])
                except:
                    pass
        except:
            pass
    
    
    tab1.write(start, 11, 'Avg Can DO Data')
    
    for idx, header in enumerate(avg_do):
        tab1.write(start+1, idx+11, header)
        try:
            for i in np.arange(len(avg_do)):
                tab1.write(start+2+i, idx+11, avg_do.iloc[i,idx])
        except:
            pass
    
        
        
    tab2 = workbook.add_worksheet('Brewsheet')
    
    
    for idx, header in enumerate(brewsheet1):
        try:
            for i in np.arange(len(brewsheet1)):
                try:
                    tab2.write(i, idx, brewsheet1.iloc[i,idx])
                
                except:
                    pass
        except:
            pass
    
    
    if brewsheet2 is not None:
        
        tab2 = workbook.add_worksheet('Brewsheet2')
    
    
        for idx, header in enumerate(brewsheet2):
            try:
                for i in np.arange(len(brewsheet2)):
                    try:
                        tab2.write(i, idx, brewsheet2.iloc[i,idx])
                    
                    except:
                        pass
            except:
                pass
    
    
    workbook.close()
    
    
    os.remove('fermplot.png')
    
    os.system("start EXCEL.EXE BatchReport.xlsx")



