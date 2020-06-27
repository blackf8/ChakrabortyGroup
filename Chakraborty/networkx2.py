import os
import math
import timeit
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
#test
#height of box times the cumulative strain
#0.000214075 * 72.1195 == shift
# y val = add Lz to the original value for y.
# x val = add the shift to the original value for x.

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
    @return self.file.readline(): Uses our file object's readline method to return a line of text.
    """
    def readLine(self):
        return self.file.readline()

    """
    Details: The method readLines reads every line from a given file.
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
    @return self.generator.__next__(): Returns a reference to the iterator after calling __next__().
    """
    def next(self):
        return self.generator.__next__()

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
    #def frameCreator(self):



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
        if(intReader == None):
            type = "Position | "
        else:
            type = "Network | "
        if(frameNum == None):
            self.frameNum = 1
        else:
            self.frameNum = frameNum
        self.frameTitle =    type + parReader.frameDetails()
        self.parReader  = parReader
        self.intReader = intReader
        self.graph = nx.Graph()

    """
    Details: The method run will automatically call frame methods to produce a frame\graph.
    The if statement allows for the incorporation of the edges for our network graph.
    """
    def run(self):
        #self.parReader.skip(17)
        legendElements = self.legendData()
        self.parser()
        if("Network" in self.frameTitle):
            self.parserInt(legendElements)
        self.networkX(legendElements)

    """
    Details: The method parserInt will clean the data from the intFile for plotting.
    This method is only called for network graphs.
    @param legendElements: A list of legend elements that will be modified with more information.
    """
    def parserInt(self, legendElements):
        self.intReader.skip(6)
        condition = False
        line = self.intReader.next()
        posInfo = nx.get_node_attributes(self.graph, 'pos')
        numRed = 0
        numBlue = 0
        while(condition == False):
            line = line.split(" ")
            first = float(line[0])
            second = float(line[1])
            if(abs(posInfo[first][1]-posInfo[second][1]) < 50 and abs(posInfo[first][0]-posInfo[second][0]) < 50):
                if(line[2] == "0"): #no-contact
                    self.graph.add_edge(float(line[0]), float(line[1]), color = "red")
                    numRed = numRed + 1
                elif(line[2] != "0"): #contact
                    self.graph.add_edge(float(line[0]), float(line[1]), color = "blue")
                    numBlue = numBlue + 1
            line = self.intReader.next()
            condition = '#' in line
        legendElements.append(Line2D([0],[0],color = 'r', label = str(numRed) + '|#!Contact' , lw = 3))
        legendElements.append(Line2D([0],[0], color = 'b', label = str(numBlue) +'|#Contact', lw=3))

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
    def networkX(self, legendElements):

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

        plt.savefig("C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty\\FinalImages\\FrameVideo\\" + str(self.frameNum))
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
    def legendData(self):
        cumStrain = self.parReader.next().split(" ")[4]
        self.parReader.skip(1)
        stress = self.parReader.next().split(" ")[4]
        self.parReader.skip(3)

        legendElements = [Line2D([0],[0], marker = 'o',color = 'w', label = 'cumStrn:' + cumStrain[:6], markerfacecolor = 'black', markersize = 5),
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

"""
class Video:

    def __init__(self, frame): # network videos
        self.frame = frame
        self.frame.run()
    def nextFrame(self):
        print(self.frame.frameNum)
        cur = self.frame
        cur.incrementFrameNum()
        self.frame = Frame(cur.parReader,cur.intReader, cur.frameNum)
        self.frame.run()

    def run(self, videoLength):
        for i in range(0, videoLength):
            self.nextFrame()
def main():
    startTime = timeit.default_timer()

    direction = "C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty\\ParticleData/"
    listDir = os.listdir(direction)  # returns a list of files within this directory
    file = open(direction+ listDir[0], "r") #creates a file object from list listDir
    x = FileReader(listDir[0],direction)
    x.skip(17)

    direction = "C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty\\ParticleInteration/"
    listDir = os.listdir(direction)  # returns a list of files within this directory
    file = open(direction + listDir[0], "r") #creates a file object from list listDir
    y = FileReader(listDir[0], direction)
    y.skip(20)

    frame1 = Frame(x,y)
    video = Video(frame1)
    video.run(100)

    print("Runtime: ", timeit.default_timer() - startTime)
main()

"""
v.8 s1
#old:[(300f, 355.95)]
#new:[(300f, 139.19)]2.5x


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
#old:[(860f,3291.9093841000004)]
#new:[(860f,388.1169188)] 10x???
"""
