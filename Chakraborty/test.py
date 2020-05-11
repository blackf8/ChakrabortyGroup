import math
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
#print(plt.style.available)
def histMu(muReal): # smaller bins, maybe 5? hist --> prob Distribution
    x = len(muReal)
    hist, bin_edges = np.histogram(muReal)
    print(hist)
    print(bin_edges)
    plt.figure(figsize = [10,8])
    plt.bar(bin_edges[:-1], hist, width = 0.03, color='#0504aa',alpha=0.7)
    plt.xlim(min(bin_edges), max(bin_edges))
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value',fontsize=15)
    plt.ylabel('Frequency',fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel('Frequency',fontsize=15)
    plt.title('Mu Distribution Histogram',fontsize=15)
    plt.show()

def graphStress(timestamps, stressRate, averageStressList, cwd,newFileName, i): # split eh constant stress graph from the other graoh.
    plt.plot(timestamps,stressRate)
    plt.plot(timestamps,averageStressList)
    plt.title("Shear Rate Over Time")
    plt.xlabel("Timestamps")
    plt.ylabel("Shear Rate")
    plt.savefig(cwd + "/finalGraphs/"+ str(i + 1)+ "stressRate"  + newFileName + ".png")
    plt.show()

def graphMu(timestamps, muReal, muApprox, averageMuList, cwd,newFileName,  i):
        plt.plot(timestamps,muReal)
        plt.plot(timestamps,muApprox)
        plt.plot(timestamps,averageMuList)
        plt.title("Mu over time")
        plt.xlabel("Timestamps")
        plt.ylabel("Mu Real and Approx")
        plt.savefig(cwd + "/finalGraphs/" + str(i + 1) +"mu"+ newFileName + ".png")
        plt.show()

def muAverage(muReal):
        x = 0
        for i in range(0,len(muReal)):
            x = x + muReal[i]
        return x/len(muReal)

def stressAverage(normalStress):
    x = 0
    for i in range(0,len(normalStress)):
        x = x + normalStress[i]
    return x/len(normalStress)

def dataCalculation(listOfXX, listOfXZ, listOfZZ, pressure, normalStress, muApprox, muReal):
    for i in range(len(listOfXX)):
        pressure.append((listOfXX[i]+ listOfZZ[i])/2)
        normalStress.append(listOfXX[i] - listOfZZ[i])
        muApprox.append(listOfXZ[i]/pressure[i])
        muReal.append(math.sqrt((normalStress[i]**2) + 4*(listOfXZ[i])**2)/(2*pressure[i]))

def dataExtraction(timestamps, listOfXX, listOfXZ, listOfZZ, stressRate, listOfData):
    for i in range(17,len(listOfData)):
        line = listOfData[i].split(" ")
        timestamps.append(float(line[0]))
        listOfXX.append(float(line[3]))
        listOfXZ.append(float(line[5]))
        listOfZZ.append(float(line[8]))
        stressRate.append(float(line[2]))

def dataExec(listOfData, cwd, newFileName, i): #Graph individual components of stress xx zz..
    timestamps = []
    listOfXX = []
    listOfZZ = []
    listOfXZ = []
    stressRate = []
    dataExtraction(timestamps, listOfXX, listOfXZ, listOfZZ, stressRate, listOfData)
    pressure = []
    normalStress = []
    muApprox = []
    muReal = []
    dataCalculation(listOfXX, listOfXZ, listOfZZ, pressure, normalStress, muApprox, muReal)
    totalData = [timestamps,listOfXX,listOfXZ,listOfZZ,pressure,normalStress,muApprox,muReal]
    averageStress = stressAverage(normalStress)
    averageStressList = [averageStress]*len(normalStress)
    averageMu = muAverage(muReal)
    averageMuList = [averageMu]*len(muReal)
    graphMu(timestamps, muReal, muApprox, averageMuList, cwd, newFileName, i)
    graphStress(timestamps, stressRate, averageStressList, cwd, newFileName, i)
    histMu(muReal)

def fileNameParser(fileName):
    #st_D2N1000VF0.8Bidi1.4_0.5Square_1_preshear_nobrownian_2D_stress1cl_shear
    parts = fileName.split("_")
    key = ["stress","par", "VF", "shear.dat"]
    name = ""
    for i in range(len(parts)):
        for j in range(len(key)):
            if(key[j] in parts[i]):
                name = name + parts[i]
    return name[:-4]

def main():
    plt.style.use("seaborn-deep")
    cwd = os.getcwd()
    listDir = os.listdir(cwd+ "/dataFiles")
    for i in range(len(listDir)):
        file = open("dataFiles/"+listDir[i])
        newFileName = fileNameParser(listDir[i])
        listOfData = file.readlines()
        dataExec(listOfData, cwd, newFileName, i)
        file.close()
main()
