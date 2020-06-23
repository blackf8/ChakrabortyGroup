import os

#test
#height of box times the cumulative strain
#0.000214075 * 72.1195 == shift
# y val + lz
# x val = add the shift to the original value for x.
class frame:
    def __init__():
        self.data = null

class fileReader:
    def __init__(self,fileName, directory):
        self.name = fileName
        self.dir = directory
        self.file = open(self.dir + self.name, "r")
        self.generator = self.generator_read()
        self.frame = frame()

    def readLine(self):
        return self.file.readline()

    def readLines(self):
        return self.file.readlines()

    def generator_read(self):
        for row in (self.file):
            yield row

    def next(self):
        return self.generator.__next__()

    def startUp(self):
        for i in range(17):
            self.next()

    def frameDetails(self):

cwd  = os.getcwd() #gets current path directory
direction = "C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty"
listDir = os.listdir(direction+ "/ParticleData")  # returns a list of files within this directory
file = open(direction + "\\ParticleData/" + listDir[0], "r") #creates a file object from list listDir
x = fileReader(listDir[0],direction + "\\ParticleData/")
x.startUp()
print(x.next())
