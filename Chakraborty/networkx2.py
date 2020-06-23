import os

#test
#height of box times the cumulative strain
#0.000214075 * 72.1195 == shift
# y val = add Lz to the original value for y.
# x val = add the shift to the original value for x.
class frame:
    def __init__(self):
        self.data = None

class fileReader:

    """
    Details: The fileReader object initialization begins here.
    @param fileName: The name of the file we want to read.
    @param directory: The path directory for that file.

    Fields:
    name: The name of the file we will be reading.
    dir: The directory of the file we are reading.
    file: A file object that opens the file using self.name and self.dir.
    generator: A iterator object that will be used to parse through a file.
    frame: A frame object that will store the file data and produce a resulting graph.
    """
    def __init__(self,fileName, directory):
        self.name = fileName
        self.dir = directory
        self.file = open(self.dir + self.name, "r")
        self.generator = self.generator_read()
        self.frame = frame()

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
    def startUp(self, num): # num = 17 for our files.
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

def main():
    cwd  = os.getcwd() #gets current path directory
    direction = "C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty"
    listDir = os.listdir(direction+ "/ParticleData")  # returns a list of files within this directory
    file = open(direction + "\\ParticleData/" + listDir[0], "r") #creates a file object from list listDir
    x = fileReader(listDir[0],direction + "\\ParticleData/")
    x.startUp(17)
    print(x.next())
    x.frameDetails()

main()
