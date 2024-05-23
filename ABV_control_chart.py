# Written by Caitlin Keady, 2023

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def abvchart(brand_input):
    rootdir = os.getcwd()
    os.chdir(r'../Tracking')
    
    # import ABV spreadsheet
    abv = pd.read_excel('ABV Tracking.xlsx', 'Final Package')
    target = pd.read_excel('ABV Tracking.xlsx', 'Targets')     
    abv['Sample Date'] = [date_obj.strftime('%m/%d/%Y') for date_obj in abv['Sample Date']]

    for i in np.arange(len(abv)):
        abv.iloc[i, 0] = abv.iloc[i, 0].upper()

    for i in np.arange(len(target)):
        target.iloc[i, 1] = target.iloc[i, 1].upper()

    user_brand = brand_input

    # Establish ABV target and limits
    brand_targ = target[target['Brand Code'] == user_brand].iloc[0, 3]

    upp_targ = brand_targ + 0.3
    low_targ = brand_targ - 0.3

    by_brand = abv[abv.Brand == user_brand]
    by_brand = by_brand.tail(20)
    by_brand.reset_index(drop=True, inplace=True)
    mr = [np.nan]
    for i in np.arange(1, len(by_brand)):
        mr.append(abs(by_brand.iloc[i, 4] - by_brand.iloc[i-1, 4]))

    plt.rcParams['figure.dpi'] = 300
    plt.rcParams.update({'font.size': 18})
    fig, axs = plt.subplots(2, figsize=(15, 15), sharex=True)
    fig.subplots_adjust(hspace=0.4)

    axs[0].axhline(brand_targ, color='k')
    axs[0].axhline(upp_targ, color='red', linestyle='dashed')
    axs[0].axhline(low_targ, color='red', linestyle='dashed')
    axs[0].plot(by_brand.iloc[:, 4], linestyle='-', marker='o')
    axs[0].set_xticks(np.arange(len(by_brand)))
    mydates = by_brand['Sample Date']
    mydates = mydates.astype(str)
    axs[0].axes.xaxis.set_ticklabels(mydates.str[0:11])

    axs[0].xaxis.set_tick_params(labelbottom=True)
    axs[0].tick_params(axis='x', labelrotation=90)
    axs[0].set_title(f'Individual: {user_brand.upper()}')
    axs[0].set(xlabel='', ylabel='ABV')

    axs[1].axhline(np.nanmean(mr), color='k')
    axs[1].axhline(3.267*np.nanmean(mr), color='red', linestyle='dashed')
    axs[1].axhline(0, color='red', linestyle='dashed')
    axs[1].set_xticks(np.arange(len(by_brand)))
    axs[1].axes.xaxis.set_ticklabels(mydates.str[0:11])

    axs[1].tick_params(axis='x', labelrotation=90)
    axs[1].plot(mr, linestyle='-', marker='o',)

    axs[1].set_title(f'Moving Range: {user_brand.upper()}')
    axs[1].set(xlabel='', ylabel='Range')

    os.chdir(rootdir)
    plt.savefig('plot', dpi=55)
    plt.close()
