import os
import networkx as nx
import matplotlib.pyplot as plt
import math
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
There are two constructors for the different graphs we want to create depending on available data.
@param parReader: A FileReader object used to read par files containing data on particle positions.
@param intReader: A FileReader object used to read int files containing data on particle interations.

Fields:
frameTitle: Title for the graph/frame retrieved from the FileReader.frameDetails() method.
parReader: The FileReader object that reads the par files.
intreader: The FileReader object that reads the int files.
graph: A graph object that provides the image of our frame.
"""
class Frame:

    def __init__(self, parReader, intReader): # network videos
        self.frameTitle = "Network | " + parReader.frameDetails()
        self.parReader  = parReader
        self.intReader = intReader
        self.graph = nx.Graph()

    def __init__(self, parReader): # postiion videos
        self.frameTitle =  "Position | "  + parReader.frameDetails()
        self.parReader  = parReader
        self.intReader = None
        self.graph = nx.Graph()

    """
    Details: The method parser will clean our data for plotting via self.networkX().
    @return None.
    """
    def parser(self):
        numSmall = 0
        numLarge = 0

        color1 = "red"
        color2 = "grey"
        if("Position" in self.frameTitle):
            color1 = "grey"

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
        self.networkX()

    """
    Details: The method networkX will use the final set of data to produce our graph/frame.
    @return None.
    """
    def networkX(self):
        cumStrain, stress, legendElements = self.legendData()

        fig = plt.figure()
        ax = fig.add_axes([.1,.1,.8,.8])

        plt.xlabel('X-Position')
        plt.ylabel('Y-Position')
        plt.title(self.frameTitle)

        positions = nx.get_node_attributes(self.graph, 'pos')
        sizes = self.shrink(list(nx.get_node_attributes(self.graph,'size').values()), math.pi)
        colors = list(nx.get_node_attributes(self.graph, 'color').values())

        nx.draw_networkx(self.graph, pos = positions,node_size = sizes, node_color = colors, with_labels = False)
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True) #used to reveil the axis numbers
        plt.legend(handles = legendElements,loc = 'upper right')#bbox_to_anchor=(1, 1));
        plt.show()
        return None

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
    Details: The method legendData produces all of the data needed for the legend of the graph.
    @return cumStrain,stress: The cumStrain and stress of the system at hand.
    """
    def legendData(self):
        cumStrain = self.parReader.next().split(" ")[4]
        self.parReader.skip(1)
        stress = self.parReader.next().split(" ")[4]
        self.parReader.skip(3)

        legendElements = None
        #[Line2D([0],[0], marker = 'o',color = 'w', label = 'cumStrn:' + cumStrain, markerfacecolor = 'black', markersize = 5),
        #Line2D([0],[0], marker = 'o',color = 'w', label = 'shearRt:' + stress, markerfacecolor = 'black', markersize = 5)]
        return cumStrain,stress, legendElements
        #You just finished this class. LOL psych! 6/24/2020

    """
    Details: The method toString prints the objects name for debugging purposes.
    @return self.frameTitle: Returns the title of this frame object.
    """
    def toString(self):
        return self.frameTitle

def main():
    cwd  = os.getcwd() #gets current path directory
    direction = "C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty"
    listDir = os.listdir(direction+ "/ParticleData")  # returns a list of files within this directory
    file = open(direction + "\\ParticleData/" + listDir[0], "r") #creates a file object from list listDir
    x = FileReader(listDir[0],direction + "\\ParticleData/")
    x.skip(17)
    frame1 = Frame(x)
    frame1.legendData()
    frame1.parser()
main()
