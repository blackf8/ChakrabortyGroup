import matplotlib.pyplot as plt
import os
import seaborn as sns
import math

import statsmodels
from statsmodels.graphics.tsaplots import plot_acf
from statistics import stdev
import numpy as np
import pandas as pd
import seaborn as sns
import statistics


def df_manual_acf(df, label, cwd):
    print("alpha",  (df['cumulated strain'].max() - df['cumulated strain'].min()), df['cumulated strain'].shape[0])
    alphaValue = (df['cumulated strain'].max() - df['cumulated strain'].min()) / df['cumulated strain'].shape[0]
    lags = df.shape[0] // 2
    resultList = [0] * lags
    deltaM = 1
    shearAverage = df['shear rate'].mean()
    #shift shear function to x=0
    df['shear rate shifted'] = df['shear rate'] - shearAverage

    #calculate the denominator
    df['acf denom'] = df['shear rate shifted'] ** 2
    denom = df['acf denom'].sum()

    #calculate autocorrelation
    shear_rate_shifted = list(df["shear rate shifted"])
    for i in range(lags):
        for j in range(df.shape[0] - i):
            resultList[i] += shear_rate_shifted[j] * shear_rate_shifted[j + i * deltaM]
        resultList[i] = resultList[i] / denom

    df_lags = pd.DataFrame(resultList, columns = ['lags'])
    return df_lags, alphaValue

def df_dataCalculation(df):
    df['pressure'] = ((df['total stress tensor (xx)'] + df['total stress tensor (zz)'])) / 2
    df['normalStress'] = df['total stress tensor (xx)'] - df['total stress tensor (zz)']
    df['muReal'] = ((df['normalStress'] ** 2) + (4 * (df['total stress tensor (xz)'] ** 2)) / (2 * df['pressure']))**.5
    cols = ['total stress tensor (xx)', 'total stress tensor (zz)', 'total stress tensor (xz)', 'pressure', 'normalStress', 'muReal']
    return df


def fileNameParser(fileName):
    # st_D2N1000VF0.8Bidi1.4_0.5Square_1_preshear_nobrownian_2D_stress1cl_shear
    parts = fileName.split("_")
    key = ["stress", "par", "VF", "shear.dat"]
    name = ""
    for i in range(len(parts)):
        for j in range(len(key)):
            if key[j] in parts[i]:
                name = name + parts[i]
    return name[:-4]

def dat_to_df(file_name, samples_skip = 0):
    '''
    Converts the data in a dat file to a dataframe.
    Args:
        file_name(Str): File name of .dat file data
    Return:
        df(DataFrame): Dataframe object holding .dat file data
    '''
    cols = ['time', 'cumulated strain', 'shear rate',
            'total stress tensor (xx)', 'total stress tensor (xy)', 'total stress tensor (xz)',
            'total stress tensor (yz)', 'total stress tensor (yy)', 'total stress tensor (zz)',
            'contact stress tensor (xx)', 'contact stress tensor (xy)', 'contact stress tensor (xz)',
            'contact stress tensor (yz)','contact stress tensor (yy)','contact stress tensor (zz)',
            'dashpot stress tensor (xx)', 'dashpot stress tensor (xy)', 'dashpot stress tensor (xz)',
            'dashpot stress tensor (yz)', 'dashpot stress tensor (yy)', 'dashpot stress tensor (zz)',
            'hydro stress tensor (xx)', 'hydro stress tensor (xy)', 'hydro stress tensor (xz)',
            'hydro stress tensor (yz)', 'hydro stress tensor (yy)', 'hydro stress tensor (zz)',
            'repulsion stress tensor (xx)', 'repulsion stress tensor (xy)', 'repulsion stress tensor (xz)',
            'repulsion stress tensor (yz)', 'repulsion stress tensor (yy)', 'repulsion stress tensor (zz)']
    file = open(file_name)
    lines = file.readlines()[17+samples_skip:]
    lines_split = []
    for line in lines:
        lines_split.append(line.split())
    df = pd.DataFrame(lines_split, columns = cols).astype(np.float)
    return df

def interpolate(df, maxLength):
    array = list(df['lags'])
    num_nulls = maxLength - len(array)
    if num_nulls != 0:
        placement = maxLength/num_nulls
    for i in range(1, num_nulls + 1):
        array.insert((i*round(placement))%len(array), np.nan)
    return pd.DataFrame(array, columns = ['lags']).interpolate(method='linear')

def main():
    plt.style.use("seaborn-deep")
    cwd = os.getcwd()
    files = os.listdir(cwd+"/data/")
    for file_name in files:
        print(file_name)
        listDir = os.listdir(cwd + "/data/" + file_name)
        data = {}
        maxLength = 0
        for i in range(len(listDir)):
            print(i)
            df = dat_to_df("data/"+ file_name +"/" + listDir[i], 23) #new dataframe implementation
            df_dataCalculation(df)
            a,b = df_manual_acf(df, fileNameParser(listDir[i]).split("stress"), cwd)
            maxLength = max(maxLength, a.shape[0])
            data[i] = (a,b)

        plot_avg = pd.DataFrame([0]*maxLength, columns = ['lags'])
        for key in data.keys():
            df_lags = interpolate(data[key][0], maxLength)
            plot_avg['lags'] = plot_avg['lags'] + df_lags['lags']
            alphaValue = data[key][1]
            print(alphaValue, len(df_lags.index), alphaValue * len(df_lags.index))
            plt.scatter(df_lags.index*alphaValue, df_lags['lags'], s=0.5)
        plt.title(file_name)
        plt.scatter(df_lags.index*alphaValue, plot_avg['lags']/10, s=0.5, linewidths = 3)
        plt.xlabel("Lag",fontsize=12)
        plt.ylabel("Cumulative Strain",fontsize = 12)
        plt.xlim(0,1)
        plt.savefig(cwd + "/samestressACF/" + fileNameParser(listDir[i]) + ".png")
        #plt.show()
        plt.close()
main()






'''
Notes:

For each dataset subtract the average.

*y axis is c
1) Create ten new lines with the average subtracted.
2) Square the resulting values
3) sum all 10 squared values
4) divide by 10 to normalize

How does the heigh

P: What does the variance look like for each overall dataset.


Final two plots:
a) averages at different stresses, for the same packing fraction, on the same plot
b) variance at different stresses, for the same packing fracion, on the same plot
'''
