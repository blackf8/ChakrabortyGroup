import os
import math
import timeit
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
"""
Program: networkx2.py
Author: Prabu Gugagantha
Date: Jun/21/2020

Details: Networkx2 is a reimplementation of the networkx program using object oriented methods.
This program aims to create videos of particle simulations that under-go DST.(Discontinuous Shear Thickening)
By using objects and generators we can greatly improve the runtime and memory usage of the program, thus
allowing the production of faster videos. At the end of this program I included some runtime tests to see how
efficient these changes actually are.
"""
#test
#height of box times the cumulative strain
#0.000214075 * 72.1195 == shift
# y val = add Lz to the original value for y.
# x val = add shift to the original value for x.
""""
Things to improve/ Things to add
--> Show portions of graphs, e.x: partial domains[x1,x2]
-*> Fix how the force time series is called in video
--> Add/Calculate boundary particles
-*> Automate the video making process
    -*> Allow for one video to be created automatically without manually inputting amount of Frames
    -*> Create a loop that will create multiple videos.
-*> Test all the videos in the database
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
Details: The frame object is used to produce a single graph with networkx/matplotlib packadges.
This constructor can be overloaded so that it can create both position and network graphs.
@param parReader: A FileReader object used to read par files containing data on particle positions.
@param intReader: A FileReader object used to read int files containing data on particle interations.

Fields:
frameTitle: Title for the graph/frame retrieved from the FileReader.frameDetails() method.
parReader: The FileReader object that reads the par files.
intreader: The FileReader object that reads the int files.
graph: A graph object that provides the image of our frame.
"""
class Frame:

    def __init__(self, parReader, intReader = None, frameNum = None): # network videos
        self.parReader  = parReader
        intCheck = (intReader == None)
        if(intCheck):
            type = "Position | "
        else:
            type = "Network | "
            self.intReader = intReader
        if(frameNum == None):
            self.frameNum = 1
            self.parReader.skip(17)
            if(intCheck == False):
                self.intReader.skip(20)
        else:
            self.frameNum = frameNum
        self.frameTitle =    type + parReader.frameDetails()

        self.graph = nx.Graph()

    """
    """
    def hasNextFrame(self):
        return not self.parReader.generator == None


    """
    Details: The method run will automatically call frame methods to produce a frame\graph.
    The if statement allows for the incorporation of the edges for our network graph.
    """
    def run(self,folder,line):
        legendElements = self.legendData(line)
        self.parser()
        redCount = None
        blueCount = None
        if("Network" in self.frameTitle):
            redCount, blueCount = self.parserInt(legendElements)
        self.networkX(legendElements, folder) #add a parameter that takes you to the folder. maybe the title string?
        return redCount,blueCount

    """
    Details: The method parserInt will clean the data from the intFile for plotting.
    This method is only called for network graphs.
    @param legendElements: A list of legend elements that will be modified with more information.
    @return numRed: The number of lubricated.......
    """
    def parserInt(self, legendElements):
        self.intReader.skip(6)
        condition = False
        line = self.intReader.next()
        posInfo = nx.get_node_attributes(self.graph, 'pos')
        numRed = 0 #non-lubricated/ Contact
        numBlue = 0#lubricated/ Non-Contact
        while(condition == False):
            line = line.split(" ")
            first = float(line[0])
            second = float(line[1])
            if(abs(posInfo[first][1]-posInfo[second][1]) < 50 and abs(posInfo[first][0]-posInfo[second][0]) < 50):
                if(line[2] == "0"): #no-contact
                    self.graph.add_edge(float(line[0]), float(line[1]), color = "blue")
                    numBlue = numBlue + 1
                elif(line[2] != "0"): #contact
                    self.graph.add_edge(float(line[0]), float(line[1]), color = "red")
                    numRed = numRed + 1
            else:
                """
                Here is where we would add the boundary points with different colored edges
                posInfo[first][0] = x1
                posInfo[first][1] = y1
                posInfo[second][0] = x2
                posInfo[second][1] = y2
                """
            line = self.intReader.next()
            if(not line == None):
                condition = '#' in line #error when hits final line
            else:
                condition = True
        legendElements.append(Line2D([0],[0],color = 'r', label = str(numRed) + '|#Contact' , lw = 3))
        legendElements.append(Line2D([0],[0], color = 'b', label = str(numBlue) +'|#!Contact', lw=3))
        return numRed,numBlue
    """
    Details: The method parser will clean our particle pos data for plotting via self.networkX().
    """
    def parser(self):
        numSmall = 0
        numLarge = 0

        color1 = "grey"
        color2 = "red"
        if("Network" in self.frameTitle):
            color2 = "grey"

        for i in range(0,1000):
            line = self.parReader.next().split(" ")
            particleName = line[0]
            particleRadius = float(line[1])
            xPos = float(line[2])
            zPos = float(line[3])
            if (particleRadius == 1):
                numSmall = numSmall + 1
                self.graph.add_node(i,pos = (xPos, zPos), size = particleRadius, color = color1)
            elif(particleRadius == 1.4):
                numLarge = numLarge + 1
                self.graph.add_node(i,pos = (xPos, zPos), size = particleRadius, color = color2)

    """
    Details: The method networkX will use the final set of data to produce our graph/frame.
    @param legendElements: A list of elements that build the legend which is added to the graph.
    """
    def networkX(self, legendElements, folder):

        fig = plt.figure()
        ax = fig.add_axes([.1,.1,.8,.8])

        plt.xlabel('X-Position')
        plt.ylabel('Y-Position')
        plt.title(self.frameTitle)

        positions = nx.get_node_attributes(self.graph, 'pos')
        sizes = self.shrink(list(nx.get_node_attributes(self.graph,'size').values()), math.pi)
        colors = list(nx.get_node_attributes(self.graph, 'color').values())

        edges = None
        if(self.intReader != None):
            edges = list(nx.get_edge_attributes(self.graph, 'color').values())

        nx.draw_networkx(self.graph, pos = positions,node_size = sizes, node_color = colors, edge_color = edges, with_labels = False)
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True) #used to reveil the axis numbers
        plt.legend(handles = legendElements,loc = 'upper right')#bbox_to_anchor=(1, 1));
        path = folder.split("/")
        newPath = ""
        for i in range (len(path)):
            newPath = newPath + path[i] + "\\"
        plt.savefig(newPath + str(self.frameNum))
        #plt.show()
        plt.close()

    """
    Details: The method shrink reduces an array's elements by a scalar amount.
    @param arr: The array that we will be modifying.
    @param scale: The scalar amount the array will be modified by.
    @return arr: The newly modified array.
    """
    #Shrinks a given array by a specific amount
    def shrink(self, arr, scale):
        for element in range(0,len(arr)):
            arr[element] = math.pow(arr[element],2)*scale
        return arr

    """
    Details: The method legendData produces all of the pos data needed for the legend of the graph.
    @legendElements: The legend elements saved to a list for use in the networkx() method.
    """
    def legendData(self, line):# this method will take in the first line of the frame from the video loop.
        cumStrain = line.split(" ")[4]
        #cumStrain = self.parReader.next().split(" ")[4]
        self.parReader.skip(1)
        stress = self.parReader.next().split(" ")[4]
        self.parReader.skip(3)
        frame_label = 'Frame:' + str(self.frameNum)
        legendElements = [Line2D([0],[0], marker = 'o',color = 'w', label = frame_label, markerfacecolor = 'black', markersize = 5),
                          Line2D([0],[0], marker = 'o',color = 'w', label = 'cumStrn:' + cumStrain[:6], markerfacecolor = 'black', markersize = 5),
                          Line2D([0],[0], marker = 'o',color = 'w', label = 'shearRt:' + stress[:6], markerfacecolor = 'black', markersize = 5)]
        return legendElements

    """
    Details: The method incrementFrameNum keeps track of the number of frames in a specific video.
    """
    def incrementFrameNum(self):
        self.frameNum = self.frameNum + 1

    """
    Details: The method toString prints the objects name for debugging purposes.
    @return self.frameTitle: Returns the title of this frame object.
    """
    def toString(self):
        return self.frameTitle


"""
Details: The Video object is used to produce a single graph with networkx/matplotlib packadges.
This constructor can be overloaded so that it can create both position and network graphs.
@param frame: This frame will be the initial frame of our video.
@param forceType: This variable allows you to get a timeseries of network videos.
@param folder: The path of the folder we want to save the video, in string format.
"""
class Video:
#redundant code fix this later* Remember: matplotlib kills runtime and storage
    def __init__(self, frame, forceType): # network videos
        self.frame = frame
        self.forceType = forceType
        if(self.forceType):
            self.x1 = []
            self.x2 = []

        temp = self.frame.frameTitle.split(" ")[2]
        parent = "D:/Chakraborty/frames/"
        path = os.path.join(parent,temp)
        if not os.path.exists(path):
            os.makedirs(parent + temp)
            self.folder = path

    """
    Details: The method nextFrame creates the next frame for our video.
    """
    def nextFrame(self, line):
        print(self.frame.frameNum)
        if(self.forceType):
            x1,x2 = self.frame.run(self.folder, line)
            self.x1.append(x1)
            self.x2.append(x2)
        else:
            self.frame.run(self.folder, line)
        cur = self.frame
        cur.incrementFrameNum()
        self.frame = Frame(cur.parReader,cur.intReader, cur.frameNum)

    """
    Details: The method run repeatedly calls on nextFrame to form our video.
    @param videoLength: The length of the video we want.
    """
    def run(self, videoLength):
        line = self.frame.parReader.next()
        for i in range(0, videoLength):
            self.nextFrame(line)
            line = self.frame.parReader.next()
        if(videoLength == 0):
            while(not line == None):
                self.nextFrame(line)
                line = self.frame.parReader.next()
        self.forceTypePlot()
        #self.frame.hasNextFrame()


    """
    Details: The method forceTypePlot plots a timeseries of the forces in a network video.
    """
    def forceTypePlot(self):

        size = []
        for i in range(len(self.x1)):
            size.append(50)

        plt.plot(list(range(0,self.frame.frameNum-1)),self.x1, color = 'r', marker = 'o', markersize = 5)
        plt.plot(list(range(0,self.frame.frameNum-1)),self.x2, color = 'b', marker = 'o', markersize = 5)
        plt.xlabel("TimeStep(Frames)")
        plt.ylabel("Number of Forces")
        plt.title(self.frame.parReader.frameDetails())
        #plt.show()
        path = self.folder.split("/")
        newPath = ""
        for i in range (len(path)):
            newPath = newPath + path[i] + "\\"
        plt.savefig(newPath + "forceTypePlot")
        plt.close()

        fractions = []
        for i in range(len(self.x1)):
            fractions.append(self.x1[i]/self.x2[i])
        plt.hist(fractions,bins = round(math.sqrt(len(fractions))))
        plt.xlabel("Data Intervals")
        plt.ylabel("Frequency(contact/non-contact)")
        plt.title("Distribution: " + self.frame.parReader.frameDetails())

        plt.savefig(newPath + "distribution")
        plt.close()

"""
Details: The main method is where we create objects for testing and programming purposes.
"""
def main():
    startTime = timeit.default_timer()

    directionData = "D:\\Chakraborty\\data/"
    directionInt = "D:\\Chakraborty\\int/"
    listDirData = sorted(os.listdir(directionData))# returns a list of files within this directory
    listDirInt = sorted(os.listdir(directionInt))# returns a list of files within this directory
    for i in range(len(listDirData)):
        print("File Number: " + str(i))
        print(listDirData[i])
        print(listDirInt[i])
        x = FileReader(listDirData[i], directionData)
        y = FileReader(listDirInt[i], directionInt)

        originalFrame = Frame(x,y)
        video = Video(originalFrame, True)
        video.run(0)

    print("Runtime: ", timeit.default_timer() - startTime)
main()


"""
Experimental Data gain from using this program against the older version 'networkx.py'

Format:
(Experiment name):
v.# s#
(old program)  [(num of frames, time in seconds)]
#old:[(#f,s)]
(new program)  [(num of frames, time in seconds)] "Sometimes the scale is written here"
#new:[(#f,s)]


v.8 s1
#old:[(100f,79.88500909999999)]
#new:[(100f,32.1224409)]2x?

v.8 s1
#old:[(300f, 355.95)]
#new:[(300f, 139.19)]2.5x?


v.8 s10 "test2"
#old:[(100f,407.7904915)]
#new:[(100f,36.5035438)] 10x???

v.8 s10 "test1"
#old:[(450f, 2132.4332805999998)]
#new:[(450f,213.9816998)] 10x???

v.8 s10
#old:[(860f,4185.770987)]
#new:[(860f,371.5872071)] 10x???

v.8 s100
#old:[(100f,392.7095309)]
#new:[(100f,43.3015117)] 10x???

v.8 s100
#old:[(450f,2014.4692045)]
#new:[(450f, 171.2547038000000)]x10??

v.8 s100
#old:[(860f,3291.9093841000004)]
#new:[(860f,388.1169188)] 10x???
"""
"""
#direction = "C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty\\ParticleData/"
directionTest = "D:\\Chakraborty\\data/"
listDir = sorted(os.listdir(directionTest))  # returns a list of files within this directory
file = open(directionTest+ listDir[0], "r") #creates a file object from list listDir
x = FileReader(listDir[0],directionTest)

#direction = "C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty\\ParticleInteration/"
directionTest = "D:\\Chakraborty\\int/"
listDir = sorted(os.listdir(directionTest))  # returns a list of files within this directory
file = open(directionTest + listDir[0], "r") #creates a file object from list listDir
y = FileReader(listDir[0], directionTest)

frame1 = Frame(x,y)
video = Video(frame1, True)
video.run(0)
"""
