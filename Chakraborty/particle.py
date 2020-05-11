import math
import matplotlib
import matplotlib.pyplot as plt
import os
# make a movie out of the various particle configs. ffmpeg
def graphFrame(particleRadius, particleX, particleZ, counter, cwd):
    plt.scatter(particleX, particleZ, s=particleRadius) ##look into the size variable, plotting circles.
    # Might be over printing.
    plt.title('Initial Particle format ' + str(counter))
    plt.xlabel('X-Position')
    plt.ylabel('Y-Position')
    plt.savefig(cwd + "/particlePos/"+ str(counter)+".png")
    print(counter)
    plt.show()

def lineParser(currentLine, particleRadius, particleX, particleZ): #this goes through each particle in a singl frame, extracting information
    splitLine = currentLine.split(" ");
    particleRadius.append(float(splitLine[1]))
    particleX.append(float(splitLine[2]))
    particleZ.append(float(splitLine[3]))


def main():
    cwd  = os.getcwd()
    listDir = os.listdir(cwd+ "/ParticleData")
    file = open("ParticleData/" + listDir[0], "r")
    listOfData = file.readlines()
    counter = 0 #keeps track of the amount of frames in our graphs
    particleRadius = []
    particleX = []
    particleZ = []
    for i in range(17, (1006*60) + 17,1006*5): #130,797
        temp = i
        counter = counter + 1
        for j in range(i + 6, temp + 1006):
            currentLine = listOfData[j]
            parsedLine = lineParser(currentLine, particleRadius, particleX, particleZ)
        graphFrame(particleRadius,particleX, particleZ, counter, cwd)
    file.close()
main()
