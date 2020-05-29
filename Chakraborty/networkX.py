import networkx as nx
import matplotlib.pyplot as plt
import os
import math

#Shrinks a given array by a specific amount
def shrink(arr, scale):
    for element in range(0,len(arr)):
        arr[element] = math.pow(arr[element],2)*scale
    return arr
def addEdges(graph,p1,p2,pos):
    for i in range(0,len(p1)):
        if(abs(pos[p1[i]][1]-pos[p2[i]][1]) < 50 and abs(pos[p1[i]][0]-pos[p2[i]][0]) < 50):
            graph.add_edge(p1[i],p2[i])


def networkX(num, X, Y, radius, color, p1, p2, interact, frameNum):
    graph = nx.Graph()
    graph.add_nodes_from(num)
    for count in range(0,1000):
        graph.add_node(count, pos = (X[count],Y[count]))
    pos= nx.get_node_attributes(graph, 'pos')
    addEdges(graph,p1,p2,pos)
    fig = plt.figure()
    ax = fig.add_axes([.1,.1,.8,.8])
    plt.xlabel('X-Position')
    plt.ylabel('Y-Position')
    title = 'Frame '+ str(frameNum)
    plt.title(title)
    radius = shrink(radius, math.pi)
    nx.draw_networkx(graph, pos = pos,node_size = radius,node_color = color,edge_color = interact, with_labels=False, ax=ax) #draws the actual graph
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True) #used to reveil the axis numbers
    plt.savefig("C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty\\FinalImages\\FrameVideo\\"+title)
    plt.show()
    plt.close()

def dataQuery(start, end):
    cwd  = os.getcwd() #gets current path directory
    listDir = os.listdir(cwd+ "/ParticleData")  # returns a list of files within this directory
    file = open("ParticleData/" + listDir[0], "r") #creates a file object from list listDir
    listOfData = file.readlines() #Reads the lines of a specific file returned as a list
    particleRadius = [] #list of particle radius, could be useful for graph
    particleX = [] # list of x position data per node.
    particleZ = [] # list of y position data per node.
    particleNum = [] # particle num, this
    particleColor = [] # Coloring for the particles, differentiated by size
    line = listOfData[start] # string data of the first frame
    for count in range(start, end):
        line = listOfData[count]
        splitLine = line.split(" ")
        particleNum.append(float(splitLine[0]))
        particleRadius.append(float(splitLine[1]))
        if(splitLine[1] == "1"):
            particleColor.append("red")
        else:
            particleColor.append("yellow")
        particleX.append(float(splitLine[2]))
        particleZ.append(float(splitLine[3]))
    return(particleNum, particleX, particleZ, particleRadius, particleColor)

def intQuery(start2):
    cwd  = os.getcwd() #gets current path directory
    direction = "C:\\Users\\prabu\\OneDrive\Desktop\\School\\MikeInts\\Chakraborty"
    listDir = os.listdir(direction+ "/ParticleInteration")  # returns a list of files within this directory
    file = open(direction + "\\ParticleInteration/" + listDir[0], "r") #creates a file object from list listDir
    listOfData = file.readlines() #Reads the lines of a specific file returned as a list
    particleInteraction1 = []
    particleInteraction2 = []
    particleInteraction3 = []
    con = "#" in listOfData[start2]
    while (con == False):
        splitLine = listOfData[start2].split(" ")
        particleInteraction1.append(float(splitLine[0]))
        particleInteraction2.append(float(splitLine[1]))
        temp = splitLine[2]
        if(temp=="1"): #frictionless contact
            particleInteraction3.append("darkcyan")
        elif(temp == "2"): #non sliding frictional
            particleInteraction3.append("darkmagenta")
        elif(temp == "3"): #sliding frictional
            particleInteraction3.append("black")
        elif(temp == "0"): #no contact, aka lubricated contacts
            particleInteraction3.append("peru")
            #first do contacts and no contacts (0 vs non 0)
        start2 = start2 + 1
        con = "#" in listOfData[start2]
    #for i in range(start2, end2):
    return particleInteraction1, particleInteraction2, particleInteraction3, start2 + 6

def initializationData(frames): # assume 1
    start = 23
    for count in range(1,frames):
        start = start + 1006
    end = start + 1000
    return start, end

def main():
    frames = int(input("How many frames do you want to produce?"))
    start2 = 26
    for count in range(0,frames):
        start, end = initializationData(count + 1)
        num, X, Y, radius, color = dataQuery(start, end) #gets the vertex data
        p1Interact, p2Interact, typeInteract, start2 = intQuery(start2) # gets the edge data
        networkX(num, X, Y, radius, color, p1Interact, p2Interact, typeInteract, count + 1) #plots the graph
main()







#this method is ocasionally used to test the networkX packadge
#It is also used for personal debugging perposes.
def test():
    graph = nx.Graph()
    graph.add_node(1, pos = (1,2), size = 1)
    graph.add_node(2, pos = (3,4), size = 10)
    graph.add_node(3, pos = (2,1), size = 5)
    graph.add_edge(1,2)
    graph.add_edge(3,2)

    pos= nx.get_node_attributes(graph, 'pos')

    fig = plt.figure()
    ax = fig.add_axes([.1,.1,.8,.8])

    plt.xlabel('X-Position')
    plt.ylabel('Y-Position')
    nx.draw_networkx(graph, pos = pos, with_labels=False, ax=ax) #draws the actual graph
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True) #used to reveil the axis numbers
    plt.show()
