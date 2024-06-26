# Written by Caitlin Keady, 2023
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def fermcurve(menubrand):
    rootdir = os.getcwd()
    os.chdir(r'input/fermlog')
    finaldf = pd.DataFrame()
    for filename in os.listdir():
        if filename != 'README.md':
            data = pd.read_csv(filename, names=['Date', 'Location', 'Gravity', 'pH', 'Temp', 'ABV', 'Start', 'Brand', 'Batch', 'Original', 'OGDate'], header=0)
    brand_input = data['Batch'].unique()
    #print('BRAND',brand_input)
    # iterate thru all the brands and create a new entry for each brew. that entry will contain
    # the original gravity for that brew. The code will extract the OG and create a new entry with the date
    # being a day before the first fermentation log entry. 
    for i in range(len(brand_input)):
        b = brand_input[i]
        templist= []
        for index in data.index:
            if data.loc[index, 'Batch'] == b:
                #print('Match',index,b)
                row = data.loc[index].copy()
                templist.append(row)
        #tempdf contains a brew when the brand macthes
        #we are going to create a new entry for each batch that will contain OG information
        tempdf = pd.DataFrame(templist, columns=['Date', 'Location', 'Gravity', 'pH', 'Temp', 'ABV', 'Start', 'Brand', 'Batch', 'Original', 'OGDate'])
        tempdf.reset_index(drop=True, inplace=True)
        count_row = tempdf.shape[0]  # Gives number of rows
        newrow = tempdf.loc[count_row-1].copy()
        
        #now append the new entry into the brew. This will be the OG entry
        tempdf = tempdf.append(newrow)
        #tempdf = pd.concat([tempdf, newrow], ignore_index=True, sort=False)
        tempdf.reset_index(drop=True, inplace=True)    
        count_row = tempdf.shape[0]  # Gives number of rows
        count_col = tempdf.shape[1]  # Gives number of columns
        #grab the OG from any of the ferm log entries for that bacth
        OG = tempdf[tempdf['Batch'] == b]['Original']
        #print ("OG",OG[1])
        tempdf.loc[count_row-1, ['Gravity']] = OG[0]
        #grab the OG date from any of the ferm log entries for that bacth
        OGDate = tempdf[tempdf['Batch'] == b]['OGDate']
        tempdf.loc[count_row-1, ['Date']] = OGDate[0]
        # now add theis batch entry to the new conprehensive DF that will be plotted
        finaldf = pd.concat([finaldf, tempdf], ignore_index=True, sort=False)
    finaldf['Days'] = np.nan

    finaldf['Date'] = pd.to_datetime(finaldf['Date']).dt.strftime('%m/%d/%Y')
    finaldf = finaldf[finaldf['Gravity'] != 0]
    finaldf = finaldf[~finaldf['Batch'].str.contains('\\.')]

    # Calculate days since start of brew
    for i in np.arange(len(finaldf)):
        t2 = datetime.strptime(finaldf.iloc[i, 6].split(" ", 1)[0].strip(), "%m/%d/%Y")
        t1 = datetime.strptime(finaldf.iloc[i, 0], "%m/%d/%Y")
        finaldf.iloc[i, 11] = (t1 - t2).days + 1

    for i in np.arange(len(finaldf)):
        finaldf.iloc[i, 7] = finaldf.iloc[i, 7].lower()

    ###inprog = finaldf[finaldf['Location'].str.contains('FV', na=False)]
    inprog = finaldf
    if menubrand != 'ALL':
        inprog = inprog[inprog.Batch.str[:3] == menubrand]
    brand_input = inprog['Batch'].unique()
    for i in range(len(brand_input)):
        b = brand_input[i]
        user_grav = inprog[inprog['Batch'] == b]['Gravity']
        #print('UG', user_grav)
        user_days = inprog[inprog['Batch'] == b]['Days']
        user_grav = user_grav.astype(float)
        user_days.reset_index(drop=True, inplace=True)
        user_grav.reset_index(drop=True, inplace=True)

        # Filter by user brand input
        by_brand = finaldf[finaldf['Batch'].str.contains(b[0:3])]
        #print("1", by_brand)
        by_brand = by_brand[~by_brand['Batch'].str.contains(r'\.')]
        #print("2", by_brand)
        by_brand = by_brand[by_brand['Gravity'] != '0']
        #print("3", by_brand)

        # Calculate average gravity by day including historical data
        days = np.arange(max(by_brand.Days) + 1)
        #print('DAYS',days)
        all_days = []
        avg_grav = []
        sd_grav = []


        for d in np.arange(max(days) + 1):
            all_days = np.append(all_days, d)
            #print(by_brand.Days)
            grav1 = by_brand[by_brand.Days == d].iloc[:, 2].astype(float)
            if len(grav1) > 0:
                avg_grav = np.append(avg_grav, np.mean(grav1))
                sd_grav = np.append(sd_grav, np.std(grav1))
            else:
                avg_grav = np.append(avg_grav, np.nan)
                sd_grav = np.append(sd_grav, np.nan)
        # plot Ekos data, baxter UI data, average curve
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams.update({'font.size': 10})

        plt.plot(all_days, avg_grav, color='k')
        plt.plot(all_days, avg_grav + sd_grav, color='k', linestyle='dashed', linewidth=1)
        plt.plot(all_days, avg_grav - sd_grav, color='k', linestyle='dashed', linewidth=1)
        plt.scatter(by_brand.Days, by_brand.Gravity.astype(float), color='silver')
        plt.title(b)
        plt.xlim([0, max(all_days)])
        plt.xlabel('Days')
        plt.ylabel('Gravity (\N{degree sign} Plato)')

        for j in np.arange(len(user_days)):
            d = int(user_days[j])
            if avg_grav[d] + sd_grav[d] > user_grav[j] > avg_grav[d] - sd_grav[d]:
                c = 'limegreen'
            else:
                c = 'red'
            plt.scatter(user_days[j], user_grav[j], color=c)

        os.chdir(rootdir)
        plt.savefig(f'plot_{b.replace(".", "_")}', dpi=150)
        plt.close()
