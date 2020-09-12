import os
import matplotlib.pyplot as plt
import math
from matplotlib.lines import Line2D
import seaborn as sns
"""
Program: hist.py
Author: Prabu Gugagantha
Date: Aug/5/2020
Details: Trying to seperate the historgram processes from the video ones.
         Aiming to only create graphs that describe the whole system in this program.
"""



"""
Details: The fileReader object initialization begins here.
@param fileName: The name of the file we want to read.
@param directory: The path directory for that file.

Fields:
name: The name of the file we will be reading.
dir: The directory of the file we are reading.
file: A file object that opens the file using self.name and self.dir.
generator: A iterator object that will be used to parse through a file.
#frame: A frame object that will store the file data and produce a resulting graph.
"""
class FileReader:

    def __init__(self,fileName, directory):
        self.name = fileName
        self.dir = directory
        self.file = open(self.dir + self.name, "r")
        self.generator = self.generator_read()
        self.title = self.fileTitle()


    """
    """
    def fileTitle(self):
        splitName = self.name.split("_")

        filetype = splitName[0]
        experimentNum = splitName[3]
        stress = splitName[7]
        if("." in stress):
            stress = stress[6:7] + "_" + stress[8:9]
        else:
            stress = stress[5:].split("c")[0]
        #filetype + "_" + "experiment" + experimentNum + "_" + "stress" + stress
        return "stress" + stress
    """
    Details: The method readLine reads a single line from a given file.
    Not used currently but is useful for testing the file reader.
    @return self.file.readline(): Uses our file object's readline method to return a line of text.
    """
    def readLine(self):
        return self.file.readline()

    """
    Details: The method readLines reads every line from a given file.
    Not used currently but is useful for testing the file reader.
    @return self.file.readlines(): Uses our file object's readlines method to return a list of rows.
    """
    def readLines(self):
        return self.file.readlines()

    """
    Details: The method generator_read creates an iterator that is stored in self.generator_read
    @yield row: Returns the next line of text in our file
    """
    def generator_read(self):
        for row in (self.file):
            yield row

    """
    Details: The method next simply calls next on our iterator object self.generator
    @return self.generator.__next__(): Returns the next line after calling __next__().
    """
    def next(self):
        try:
            return self.generator.__next__()
        except StopIteration:
            return None


    """
    Details: The method skip will iterate through the lines of a file a set number of times.
    @param num: The number of times you want to iterate.
    """
    def skip(self, num): # num = 17 for our files.
        for i in range(num):
            self.next()

    """
    Details: The method frameDetails will use the file name and extract the graph title.
    @return packingFrac + stress: The title of the frame which will be created.
    """
    def frameDetails(self):
        splitName = self.name.split("_")
        packingFrac = splitName[1][7:].split("B")[0]
        stress = splitName[7].split("cl")[0]
        return packingFrac + stress


"""
Method: parser
Details: Used to count how many contact/non-contact forces there are.
@param intReader: A file reader that will read different interaction files.
@return numBlue : The number of non-contact Forces.
@return numRed : The number of contact forces.
@return line : The current line we are on in the int file.
"""
def parser(intReader):
    numBlue = 0;
    numRed = 0;
    condition = False;
    intReader.skip(6);
    line = intReader.next()
    while(condition ==  False):
        line = line.split(" ")
        if(line[2] == "0"): #no-contact
            numBlue = numBlue + 1
        elif(line[2] != "0"): #contact
            numRed = numRed + 1
        line = intReader.next()
        if(not line == None):
            condition = '#' in line #error when hits final line
        else:
            condition = True
    return numBlue,numRed,line



"""
Method: color
Details: Provides the color of a specific graph using matplotlibs basic colors.
@param i : What color we want from our list.
"""
def color(i):
    #color = ['b','g','r','c','m','y','k'] #7
    color = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    return color[int(i % len(color))]

#K = 1 + 3. 322 logx:round(1 + 3.322*(math.log(len(fractionList))))
#sqrt(x):round(math.sqrt(len(fractionList)))
"""
Method: histograph
Details: Takes the fractionList and plots the histogram with plt.bar.
@param fractionList : The resulting list fraction of contact forces in a specific experiment.
@param intReader: A file reader that will read different interaction files.
@param colorNum : The color of the histogram
@return fractionList : An updated fractionList with begining values trimmed off.
"""
def histograph(fractionList, intReader, colorNum):
    fractionList.sort()
    if("_" not in intReader.title):
        fractionList = fractionList[10:]
    binNum = 100 #round(1 + 3.322*(math.log(len(fractionList))))
    listMin = round(min(fractionList),7)
    listMax = round(max(fractionList),7)
    binWidth = (listMax-listMin)/binNum
    sumVal = sum(fractionList)

    #print(newfraclist)
    # you are here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
    newfraclist = []#  a list showing the bin boundary a.k.a x coordinates for the line graph
    for i in range(binNum + 1):
        newfraclist.append(listMin + binWidth/2 + (binWidth*i))
    #print(newfraclist,listMax,listMin,len(newfraclist))
    #plt.ylim(0,400)

    binList = [0]* (len(newfraclist)) # a list holding the counts in each bin    a.k.a y coordinates for line graph
    for i in fractionList:
        newval = math.floor((i - listMin)/binWidth) #---> which b3in does a number fall in.
        binList[newval] = binList[newval] + 1
    totalCount = sum(binList)
    #print(binList)

    divisor = [] # a list of the new count values normalized
    for count in binList:
        divisor.append((count/totalCount)/binWidth)


    #print(newfraclist,listMax)
    #print(color(colorNum),colorNum)
    #print(len(newfraclist),len(divisor),len(fractionList))
    #print(plt.hist(fractionList, bins = binNum, label = intReader.title + " #: " + str(len(fractionList)))[1])
    #print(newfraclist)

    #.366788         .463898
    barBool = 3
    if(barBool == 1):
        plt.bar(newfraclist,divisor,binWidth,edgecolor = color(colorNum),linewidth = 3,color = 'white',label = intReader.title + " #: " + str(len(fractionList)))
        print(sum(divisor)*binWidth)
        plt.plot(newfraclist,divisor,color = color(colorNum + 1),linewidth = 3,label = intReader.title + " #: " + str(len(fractionList)))
    elif(barBool == 2):
        print(sum(divisor)*binWidth)
        newx = [newfraclist[0]-(binWidth/2),newfraclist[0]-(binWidth/2)]
        newy = [0,divisor[0]]
        for i in range(1,len(newfraclist)):
            newx.append(newfraclist[i]-(binWidth/2))
            newy.append(divisor[i-1])

            newx.append(newfraclist[i]-(binWidth/2))
            newy.append(divisor[i])
        newx.append(newfraclist[len(newfraclist) - 1]+(binWidth/2))
        newy.append(divisor[len(divisor) - 1])

        newx.append(newfraclist[len(newfraclist) - 1]+(binWidth/2))
        newy.append(0)

        #print(" ")
        #print(newx,newy)
        plt.plot(newx,newy,color = color(colorNum),linewidth = 3,label = intReader.title + " #: " + str(len(fractionList)))
        plt.plot(newfraclist,divisor,color = color(colorNum + 1),linewidth = 3,label = intReader.title + " #: " + str(len(fractionList)))
        #newfraclist,divisor,binWidth,edgecolor = color(colorNum),linewidth = 3,color = 'white',label = intReader.title + " #: " + str(len(fractionList))
    elif(barBool == 3):
        print(sum(divisor)*binWidth)
        plt.plot(newfraclist,divisor,color = color(colorNum),linewidth = 3,label = intReader.title + " #: " + str(len(fractionList)))
    return fractionList, intReader.title + " #: " + str(len(fractionList))

"""
Method: graph
Details: Edits the graph with labels and shows the resulting graph.
@param intReader: A file reader that will read different interaction files.
@param fractionListLength : The length of the fractionList.
@param saveTitle : The resulting file name that the graph will be saved as.

"""
def graph(intReader,fractionListLength, saveTitle):
    """
    legendElements = [Line2D([0],[0], marker = 'o',color = 'w', label = '#ofPoints: ' + str(len(fractionList)), markerfacecolor = 'black', markersize = 5),
                      Line2D([0],[0], marker = 'o',color = 'w', label = '#ofBins: ' + str(binNum), markerfacecolor = 'black', markersize = 5),
                      Line2D([0],[0], marker = 'o',color = 'w', label = 'BinWidth: ' + str(binWidth)[:7], markerfacecolor = 'black', markersize = 5)]
    plt.legend(handles = legendElements,loc = 'upper right')#bbox_to_anchor=(1, 1));
    """
    #print(fractionListLength)
    legendElements = [Line2D([0],[0], marker = 'o',color = 'w', label = '#ofPoints: ' + str(fractionListLength), markerfacecolor = 'black', markersize = 5)]
    plt.legend(loc = 'upper right')
    plt.xlabel("Fraction of Contact Forces")
    plt.ylabel("Probability Density")
    plt.title("Distribution: " + intReader.frameDetails().split("s")[0])

    temp = "histtest"
    #temp = "histSquareRoot"
    parent = "E:/Chakraborty/frames/"
    path = os.path.join(parent,temp)
    if not os.path.exists(path):
        os.makedirs(parent + temp)
    print(saveTitle.split(" ")[0])
    #plt.savefig("D:\\Chakraborty\\frames\\histtest\\" + saveTitle.split(" ")[0]) # D:\Chakraborty\frames\histtest
    plt.show()
    plt.close()

"""
Method: forceCount
Details: Runs through an int file and counts\calculates the percent of contact forces.
@param folderString : A string representation of the folder we want to access.
@param fileNum : The specific file id we are going to access data from.
@return fractionList : The resulting list fraction of contact forces in a specific experiment.
@return intReader: A file reader that will read different interaction files.
"""
def forceCount(folderString, fileNum):

    fractionList = []

    for i in range(1,11): #10 experiments

        directionInt = folderString + str(i) +"/"
        listDirInt = sorted(os.listdir(directionInt))# returns a list of files within this directory
        listDirIntLength = len(sorted(os.listdir(directionInt)))

        intReader = FileReader(listDirInt[fileNum], directionInt)
        intReader.skip(20)
        print(listDirInt[fileNum])

        line = ""
        while(line != None):
            b,r,line = parser(intReader)
            fractionList.append(round(r/(r+b),7))

    return fractionList, intReader

def main():
    folderString = "E:\\Chakraborty\\int\\"
    directionInt = folderString + "1/"
    listDirInt = sorted(os.listdir(directionInt))# returns a list of files within this directory
    listDirIntLength = len(listDirInt)
    print(listDirInt)
    key = [9,11,13,14,16,18,7]  #[0,1,2,3,4,5] # [9,11,13,14,16,18,7] # [8,10,12,15,17,6] #all [1:18]
    intReader = None
    fractionList = []
    for i in range(len(listDirInt)): # len(listDirInt)   ... listDirIntLength    #g1: 0,6   #g2:6,12?
        if(i in key):
            print("File Number: " + str(i))
            fractionList,intReader = forceCount(folderString,i)
            fractionList,saveTitle  = histograph(fractionList,intReader,i)

    saveTitle = "CrossBreed"
    graph(intReader,len(fractionList), saveTitle)
main()
















"""
.1  -->0
.2  -->1
.3  -->2
.5  -->3
.7  -->4
.8  -->5

1  -->9
2  -->11
3  -->13
4  -->14
5  -->16
7  -->18
10  -->7


15  -->8
20  -->10
30  -->12
50  -->15
75  -->17
100  -->6
"""
