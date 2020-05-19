import networkx as nx
import matplotlib.pyplot as plt
import os

#Shrinks a given array by a specific amount
def shrink(arr, scale):
    for element in range(0,len(arr)):
        arr[element] = arr[element]*scale*element
    return arr


def networkX(num, X, Y, radius, color):
    graph = nx.Graph()
    graph.add_nodes_from(num)
    for count in range(0,1000):
        graph.add_node(count, pos = (X[count],Y[count]))

    pos= nx.get_node_attributes(graph, 'pos')

    fig = plt.figure()
    ax = fig.add_axes([.1,.1,.8,.8])

    plt.xlabel('X-Position')
    plt.ylabel('Y-Position')
    plt.title('Frame 1')
    radius = shrink(radius, .01)
    nx.draw_networkx(graph, pos = pos,node_size = radius,node_color = color, with_labels=False, ax=ax) #draws the actual graph
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True) #used to reveil the axis numbers
    plt.show()


def dataQuery():
    cwd  = os.getcwd() #gets current path directory
    listDir = os.listdir(cwd+ "/ParticleData")  # returns a list of files within this directory
    file = open("ParticleData/" + listDir[0], "r") #creates a file object from list listDir
    listOfData = file.readlines() #Reads the lines of a specific file returned as a list
    particleRadius = [] #list of particle radius, could be useful for graph
    particleX = [] # list of x position data per node.
    particleZ = [] # list of y position data per node.
    particleNum = [] # particle num, this
    particleColor = [] # Coloring for the particles, differentiated by size
    line = listOfData[23] # string data of the first frame
    for count in range(23, 1023):
        line = listOfData[count]
        splitLine = line.split(" ")
        particleNum.append(float(splitLine[0]))
        particleRadius.append(float(splitLine[1]))
        if(float(splitLine[1] == "1")):
            particleColor.append("red")
        else:
            particleColor.append("yellow")
        particleX.append(float(splitLine[2]))
        particleZ.append(float(splitLine[3]))
    return(particleNum, particleX, particleZ, particleRadius, particleColor)


def main():
    num, X, Y, radius, color = dataQuery()
    networkX(num, X, Y, radius, color)
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
