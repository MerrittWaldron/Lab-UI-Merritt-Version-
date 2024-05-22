# Written by Caitlin Keady, 2023
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as plt1

plt1.use('agg')


def fermcurve(menubrand):
    rootdir = os.getcwd()
    os.chdir(r'input/fermlog')

    for filename in os.listdir():
        if filename != 'README.md':
            data = pd.read_csv(filename, names=['Date', 'Location', 'Gravity', 'pH', 'Temp', 'ABV',
                                                'Start', 'Brand', 'Batch'], header=0)

    data['Days'] = np.nan

    data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%m/%d/%Y')
    data = data[data['Gravity'] != 0]
    data = data[~data['Batch'].str.contains('\\.')]

    # Calculate days since start of brew
    for i in np.arange(len(data)):
        t2 = datetime.strptime(data.iloc[i, 6].split(" ", 1)[0].strip(), "%m/%d/%Y")
        t1 = datetime.strptime(data.iloc[i, 0], "%m/%d/%Y")
        data.iloc[i, 9] = (t1 - t2).days + 1

    for i in np.arange(len(data)):
        data.iloc[i, 7] = data.iloc[i, 7].lower()

    inprog = data[data['Location'].str.contains('FV', na=False)]
    if menubrand != 'ALL':
        inprog = inprog[inprog.Batch.str[:3] == menubrand]

    brand_input = inprog['Batch'].unique()
    for i in range(len(brand_input)):
        b = brand_input[i]
        user_grav = inprog[inprog['Batch'] == b]['Gravity']
        user_days = inprog[inprog['Batch'] == b]['Days']
        user_grav = user_grav.astype(float)
        user_days.reset_index(drop=True, inplace=True)
        user_grav.reset_index(drop=True, inplace=True)

        # Filter by user brand input
        by_brand = data[data['Batch'].str.contains(b[0:3])]
        by_brand = by_brand[~by_brand['Batch'].str.contains(r'\.')]
        by_brand = by_brand[by_brand['Gravity'] != '0']

        # Calculate average gravity by day including historical data
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
