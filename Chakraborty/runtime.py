from matplotlib import pyplot as plt
import math
def grapher(num, file):
    xOld = []
    yOld = []
    xNew = []
    yNew = []
    for i in range(num):
        experimentTitle1 = file.readline().split(".")
        experimentTitle1 = experimentTitle1[0] + experimentTitle1[1]
        experimentTitle1 = experimentTitle1.split(" ")
        experimentTitle = experimentTitle1[0] + experimentTitle1[1]

        old = file.readline().split(",")
        new = file.readline().split(",")
        file.readline()
        xOld.append(float(old[1]))
        yOld.append(float(old[2]))
        xNew.append(float(new[1]))
        yNew.append(float(new[2]))
    plt.title(experimentTitle)
    plt.plot(xOld,yOld, 'b', marker = 'o', markerfacecolor = 'r', label = 'Old Program')
    plt.plot(xNew,yNew, 'g', marker = 'o', markerfacecolor = 'r', label = 'New Program')
    plt.legend()
    plt.ylabel('Time in Seconds')
    plt.xlabel('Number of Frames')
    plt.savefig("C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty\\FinalImages\\FrameVideo\\" + experimentTitle)
    #plt.show()
    plt.close()

def runtimeGraph():
    file = open('runtime.txt')
    for i in range(4):
        file.readline()
    grapher(2, file) #experiment 1
    grapher(3, file) #experiment 2
    grapher(3, file) #experiment 3

runtimeGraph()
