import statsmodels
from statsmodels.graphics.tsaplots import plot_acf
import math
import os
from statistics import stdev
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statistics
# m= row number
#  = cumulative strain
# =
# =
# =
# =

def alphaScatter(listofAlpha):
   plt.plot(listofAlpha, markersize = '10', marker = '.')
   #plt.xlim(min(listofAlpha),max(listofAlpha))
   #plt.show()




def manual_acf(shear_rate, label, cwd, newFileName, m, cumulative_Strain):
    #alphaValue = alpha(cumulative_Strain, label, cwd, newFileName, m)
    if len(cumulative_Strain) != 0:
        alphaValue = alpha(cumulative_Strain, label, cwd, newFileName, m)
        result = 0
        xAxis = []
        lags = len(m) // 2
        xCounter = 0
        for l in range(lags):
            xAxis.append(xCounter)
            xCounter+=1
        resultList = [0] * lags
        deltaM = 1
        shearAverage = statistics.mean(shear_rate)
        DeltaShearRate = [0] * len(shear_rate)
        for i in range(len(shear_rate)):
            DeltaShearRate[i] = shear_rate[i] - shearAverage
        shearSquared = 0
        TestList = [0] * (len(m) - lags)
        for k in range(len(m)):
            shearSquared += DeltaShearRate[k] * DeltaShearRate[k]
        for j in range(lags):
            for i in range(len(m) - j):
                resultList[j] += (DeltaShearRate[i + (j) * deltaM] * DeltaShearRate[i])
            resultList[j] = (resultList[j] / (shearSquared))
        for i in range(len(m) - lags):
            TestList[i] = (DeltaShearRate[i + (40) * deltaM] * DeltaShearRate[i])
        m = np.array(m)
        xAxis = np.array(xAxis)
        resultList = np.array(resultList)
        plt.scatter(xAxis*alphaValue,resultList, s=0.5)
        #plt.plot(resultList)
        plt.xlabel("Lag",fontsize=12)
        plt.ylabel("Cumulative Strain",fontsize = 12)
        plt.xlim(0,3)
        #plt.savefig(cwd + "/ACFxAlpha/" + newFileName + ".png")
        #plt.show()
        #print(label)
        #print(len(resultList))
        #print(m)
def system_strain(cumulative_Strain, label, cwd, newFileName, m):
    plt.plot(m,cumulative_Strain)
    plt.xlabel(label)
    plt.xlabel("Time")
    plt.ylabel("Cumulative Strain",fontsize = 12)
    return label
    #plt.savefig(cwd + "/shearvsM/" + newFileName + ".png")
    #plt.show()


def alpha(cumulative_Strain, label, cwd, newFileName, m):
    #print(len(shear_rate))
    if len(cumulative_Strain) != 0:
        #print(len(cumulative_Strain))
        alp = ((cumulative_Strain[-1])-(cumulative_Strain[0])) / len(cumulative_Strain)
        print(alp)
        #listofAlpha.append(alp)
        #print(label)
        #print(alp)
        #print(str((cumulative_Strain[len(cumulative_Strain)-1])))
        #print(str(len(cumulative_Strain)))
        #print(cumulative_Strain)
        #plt.plot(float(label2[0]), alp, marker=".", markersize=5, color='r')
        #plt.xlabel("Stress")
        #plt.ylabel("Alpha")
        #plt.show()
        return alp

def dataCalculation(listOfXX, listOfXZ, listOfZZ, pressure, normalStress, muReal):
    for i in range(len(listOfXX)):
        pressure.append((listOfXX[i] + listOfZZ[i]) / 2)
        normalStress.append(listOfXX[i] - listOfZZ[i])
        muReal.append(math.sqrt((normalStress[i] ** 2) + 4 * (listOfXZ[i]) ** 2) / (2 * pressure[i]))


def dataExtraction(output_number, m,time, listOfXX, listOfXZ, listOfZZ, gamma_dot, listOfData, shear_rate,cumulative_Strain):
    for i in range(40, len(listOfData)):
        line = listOfData[i].split(" ")
        m.append(output_number)
        time.append(float(line[0]))
        cumulative_Strain.append(float(line[1]))
        shear_rate.append(float(line[2]))
        listOfXX.append(float(line[3]))
        listOfXZ.append(float(line[5]))
        listOfZZ.append(float(line[8]))
        gamma_dot.append(float(line[2]))
        output_number += 1


def dataExec(listOfData, cwd, newFileName, i, label):  # Graph individual components of stress xx zz..
    output_number = 0
    m = []
    time = []
    listofAlpha = []
    cumulative_Strain = []
    shear_rate = []
    listOfXX = []
    listOfZZ = []
    listOfXZ = []
    gamma_dot = []
    dataExtraction(output_number, m,time, listOfXX, listOfXZ, listOfZZ, gamma_dot, listOfData, shear_rate,cumulative_Strain)
    pressure = []
    normalStress = []
    muReal = []
    dataCalculation(listOfXX, listOfXZ, listOfZZ, pressure, normalStress, muReal)
    total_data = [m, listOfXX, listOfXZ, listOfZZ, pressure, normalStress, muReal]
    #print(cumulative_Strain)
    #print(shear_rate)
    label = newFileName.split("stress")
    #label2 = label[1].split("clshear")
    #system_strain(cumulative_Strain, label, cwd, newFileName, m)
    #alpha(cumulative_Strain, label, cwd, newFileName, m)
    manual_acf(shear_rate, label, cwd, newFileName, m, cumulative_Strain)
    #statACF(shear_rate, label, cwd, newFileName, m)
    #alphaScatter(listofAlpha)

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


def main():
    plt.style.use("seaborn-deep")
    cwd = os.getcwd()
    listDir = os.listdir(cwd + "/data/0.76stress20")
    for i in range(len(listDir)):
        file = open("data/0.76stress20/" + listDir[i], encoding="ISO-8859-1")
        s = listDir[i]
        label = []
        newFileName = fileNameParser(listDir[i])
        listOfData = file.readlines()
        dataExec(listOfData, cwd, newFileName, i, label)
        file.close
    #plt.legend(label)
    plt.savefig(cwd + "/samestressACF/" + newFileName + ".png")
    plt.show()
main()
