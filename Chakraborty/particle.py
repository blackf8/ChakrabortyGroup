import math
import matplotlib
import matplotlib.pyplot as plt
import os
# make a movie out of the various particle configs. ffmpeg
def graphFrame(particleRadius, particleX, particleZ, counter, cwd):
    particleRadius = [x*25 for x in particleRadius]
    color = [];
    for i in range(len(particleRadius)):
        if particleRadius[i] == 1 * 25:
            color.append("red");
        elif particleRadius[i] == 1.4 * 25:
            color.append("yellow");
        else:
            color.append("black");
    #look into the size variable, plotting circles.
    plt.scatter(particleX, particleZ,c=color, s=particleRadius*20)
    plt.title('Initial Particle format ' + str(counter))
    plt.xlabel('X-Position')
    plt.ylabel('Y-Position')
    plt.savefig(cwd + "/particlePos/"+ str(counter)+".png")
    plt.close()
    print(counter)

#this goes through each particle in a single frame, extracting information
def lineParser(currentLine, particleRadius, particleX, particleZ):
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
    for i in range(17, (1006*5*26) + 17,1006*5): #130,797
        temp = i
        counter = counter + 1
        for j in range(i + 6, temp + 1006):
            currentLine = listOfData[j]
            parsedLine = lineParser(currentLine, particleRadius, particleX, particleZ)
        graphFrame(particleRadius,particleX, particleZ, counter, cwd)
        particleRadius = []
        particleX = []
        particleZ = []
    file.close()
main()
