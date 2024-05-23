# Written by Caitlin Keady, 2023

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def DOchart(brand_input, plot_points):
    rootdir = os.getcwd()
    os.chdir(r'input/condlog')

    for filename in os.listdir():
        if filename != 'README.md':
            condlog = pd.read_csv(filename, names=['Batch', 'Date', 'bbls', 'Carb', 'CO2', 'DO', 'SetPoint', 'Temp'], header=0)

    for i in np.arange(len(condlog)):
        condlog.iloc[i, 0] = condlog.iloc[i, 0].upper()

    if brand_input == 'ALL':
        user_brand = ' '
    else:
        user_brand = brand_input

    by_brand = condlog[condlog['Batch'].str.contains(user_brand)]
    by_brand = by_brand[by_brand['DO'].notna()]
    by_brand = by_brand[by_brand['DO'] != 0]

    #NEW CODE   
    myrows = by_brand.shape[0]
    print('SIZE', myrows)
    #if myrows > 100:
    #    myrows = myrows-200
    print('SIZEMOD',myrows)
    by_brand.drop(by_brand.index[0:myrows-int(plot_points)], inplace=True)
    print('SHAPEAFTER', by_brand.shape)
    #END OF NEW CODE

    by_brand.reset_index(drop=True, inplace=True)


    targ = np.mean(by_brand.iloc[:, 5])
    n = len(by_brand)

    if brand_input == 'ALL':
        xtitles = [i + ' ' + j for i, j in zip(by_brand.Date.str[0:5], by_brand.Batch.str[0:3])]
        fontsize = 12
        figwidth = 25
    else:
        xtitles = by_brand.Date.str[0:5]
        fontsize = 18
        figwidth = 15
        
    if n == 2:
        e = 2.66
        d = 3.267
    elif n == 3:
        e = 1.772
        d = 2.574
    elif n == 4:
        e = 1.457
        d = 2.282
    elif n == 5:
        e = 1.29
        d = 2.114
    elif n == 6:
        e = 1.184
        d = 2.004
    elif n == 7:
        e = 1.109
        d = 1.924
    elif n == 8:
        e = 1.054
        d = 1.864
    elif n == 9:
        e = 1.01
        d = 1.816
    else:
        e = 0.975
        d = 1.777

    mr = [np.nan]
    for i in np.arange(1, len(by_brand)):
        mr.append(abs(by_brand.iloc[i, 5] - by_brand.iloc[i-1, 5]))

    mr_bar = np.nansum(mr) / (len(mr) - 1)

    upp_targ = targ + e*mr_bar
    low_targ = targ - e*mr_bar

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams.update({'font.size': 18})
    fig, axs = plt.subplots(2, figsize=(figwidth, 15), sharex=True)
    fig.subplots_adjust(hspace=0.4)

    axs[0].axhline(targ, color='k')
    axs[0].axhline(upp_targ, color='red', linestyle='dashed')
    axs[0].axhline(low_targ, color='red', linestyle='dashed')
    axs[0].plot(by_brand.iloc[:, 5], linestyle='-', marker='o')
    axs[0].set_xticks(np.arange(len(by_brand)))
    axs[0].axes.xaxis.set_ticklabels(xtitles)
    axs[0].xaxis.set_tick_params(labelbottom=True)
    axs[0].tick_params(axis='x', labelrotation=90, labelsize = fontsize)
    axs[0].set_title(f'Individual: {user_brand.upper()}')
    axs[0].set(xlabel='', ylabel='DO')

    axs[1].axhline(np.nanmean(mr), color='k')
    axs[1].axhline(d*np.nanmean(mr), color='red', linestyle='dashed')
    axs[1].axhline(0, color='red', linestyle='dashed')
    axs[1].set_xticks(np.arange(len(by_brand)))
    axs[1].axes.xaxis.set_ticklabels(xtitles)
    axs[1].tick_params(axis='x', labelrotation=90, labelsize = fontsize)
    axs[1].plot(mr, linestyle='-', marker='o',)

    axs[1].set_title(f'Moving Range: {user_brand.upper()}')
    axs[1].set(xlabel='', ylabel='Range')

    os.chdir(rootdir)
    plt.savefig('plot', dpi=55)
    plt.close()
