import networkx as nx
import matplotlib.pyplot as plt

def main():
    graph = nx.Graph()
    graph.add_node(1, pos = (1,2))
    graph.add_node(2, pos = (3,4))
    graph.add_edge(1,2)
    #nx.draw(graph, with_labels=True, font_weight='bold')
    #nx.draw_shell(graph)
    pos= nx.get_node_attributes(graph, 'pos')

    fig, ax = plt.subplots()
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    #ax.set_xticklabels(['zero','two','four','six'])


    nx.draw(graph, pos, with_labels=True, label = 'hello')
    plt.axis('on')
    ax.set_yticks([1,2,3,4,5])
    ax.set_xticks([0,1,2,3,4])
    plt.show()
main()
