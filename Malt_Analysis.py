# Written by Caitlin Keady, 2022
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def maltplot(brand_input):
    rootdir = os.getcwd()
    os.chdir(r'input/castout')

    for filename in os.listdir():
        if filename != 'README.md':
            castout = pd.read_csv(filename)

    os.chdir(r'../malts')

    for filename in os.listdir():
        if filename != 'README.md':
            malts = pd.read_csv(filename)
            
    os.chdir(r'../../../../Documents - Brewery Operations/Lab/Tracking')
    abv = pd.read_excel('ABV Tracking.xlsx', 'Final Package')

    coa22 = pd.read_excel('Updated Malt COA.xlsx', '2022', skiprows=10, header=[0, 1])
    coa23 = pd.read_excel('Updated Malt COA.xlsx', '2023', skiprows=10, header=[0, 1])

    coa22['lot'] = np.nan
    coa23['lot'] = np.nan

    for i in np.arange(len(coa22)):
        if not pd.isnull(coa22.iloc[i, 1]):
            coa22.iloc[i, 22] = int(coa22.iloc[i, 1].strftime('%m%d%y'))
        else:
            coa22.iloc[i, 22] = np.nan

    for i in np.arange(len(coa23)):
        if not pd.isnull(coa23.iloc[i, 1]):
            coa23.iloc[i, 22] = int(coa23.iloc[i, 1].strftime('%m%d%y'))
        else:
            coa23.iloc[i, 22] = np.nan
            
    malts.Quantity = -malts.Quantity
    malts['lot'] = np.nan
    castout['RDF'] = np.nan

    for i in np.arange(len(castout)):
        for j in np.arange(len(abv)):
            if str(abv.iloc[j, 2]) in str(castout.iloc[i, 1]) and str(abv.iloc[j, 0]) in str(castout.iloc[i, 1]):
                castout.iloc[i, 10] = abv.iloc[j, 6]

    castout_total = castout.groupby(["Number", "Start Date", "Turn Count"]).Units.sum().reset_index()

    for i in np.arange(len(malts)):
        if malts.Item[i] == '2 Row (Bulk)':
            malts.iloc[i, 6] = int(malts.LotTracking[i].split(' ', 1)[0])
        else:
            malts.iloc[i, 6] = np.nan

    tworow = malts[malts.Item == '2 Row (Bulk)'].groupby(["Number", "lot"]).Quantity.sum().reset_index()
    tworow['Extract'] = np.nan
    tworow['BG'] = np.nan

    for i in np.arange(len(tworow)):
        for a in np.arange(len(coa23)):
            if tworow.iloc[i, 1] == coa23.iloc[a, 22]:
                tworow.iloc[i, 3] = coa23.iloc[a, 3]
                tworow.iloc[i, 4] = coa23.iloc[a, 16]
            elif not np.isnan(coa23.iloc[a, 22]) and abs((pd.to_datetime(coa23.iloc[a, 22],
                                                                         format='%m%d%y') - pd.to_datetime(tworow.iloc[i, 1],
                                                                                                           format='%m%d%y')).days) <= 5:
                tworow.iloc[i, 3] = coa23.iloc[a, 3]
                tworow.iloc[i, 4] = coa23.iloc[a, 16]
        for b in np.arange(len(coa22)):
            if tworow.iloc[i, 1] == coa22.iloc[b, 22]:
                tworow.iloc[i, 3] = coa22.iloc[b, 3]
                tworow.iloc[i, 4] = coa22.iloc[b, 16]
            elif not np.isnan(coa22.iloc[b, 22]) and abs((pd.to_datetime(coa22.iloc[b, 22],
                                                                         format='%m%d%y') - pd.to_datetime(tworow.iloc[i, 1],
                                                                                                           format='%m%d%y')).days) <= 5:
                tworow.iloc[i, 3] = coa22.iloc[b, 3]
                tworow.iloc[i, 4] = coa22.iloc[b, 16]

    malt_sum = malts.groupby(["Number", "Original Gravity"]).Quantity.sum().reset_index()

    data = pd.merge(malt_sum, tworow, on='Number', sort=False)
    data = pd.merge(data, castout_total, on='Number', sort=False)
    data.columns = ['Batch', 'OG', 'Grist_Wt', 'lot', '2row', 'Extract', 'BG', 'StartDate', 'Turns', 'bbls']
    data['%2row'] = data['2row'] / data['Grist_Wt']
    data['malt/turn'] = round((data['Grist_Wt'] / data['Turns'])/100)

    data['start_ext'] = data['Grist_Wt'] * data['Extract']/100

    data['sg'] = 1 + data['OG'] / (258.6 - (data['OG']*227.1/258.2))
    data['recov_ext'] = 257.9 * data['sg'] * (data['OG']/100) * data['bbls']
    data['pyield'] = 100*data['recov_ext']/data['start_ext']
    data = data[data['pyield'] != 0]

    data['brandcode'] = data['Batch'].str[:3]

    brands = ['CAD', 'COH', 'COS', 'ICE', 'IPA', 'LRL', 'OUT', 'STA']

    data = data[data['brandcode'].isin(brands)]

    # Plotting
    plt.rcParams.update({'font.size': 10})
    plt.gca().set_prop_cycle(color=['lightsalmon', 'darkviolet', 'navy', 'lightgray',
                                    '#ec4c2f', 'gold', 'skyblue', 'teal'])

    # for i in np.sort(data['malt/turn'].unique()):
    if brand_input == 'ALL':
        for i in data['brandcode'].unique():
            df = data[data['brandcode'] == i]
            plt.scatter(df['BG'], df['pyield'], label=i)
    else:
        df = data[data['brandcode'] == brand_input]
        plt.scatter(df['BG'], df['pyield'], label=brand_input, color='k')

    plt.xlabel('Beta Glucan')
    plt.ylabel('% Yield')
    plt.legend(bbox_to_anchor=(1.2, 1), loc='upper right', ncol=1)

    os.chdir(rootdir)
    plt.savefig('plot', dpi=150, bbox_inches='tight')
    plt.close()
