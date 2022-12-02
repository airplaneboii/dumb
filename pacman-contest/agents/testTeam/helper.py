import copy
import numpy as np

class Node:
    # type(labels)  
    def __init__(self, value, labels=None):
        self.value = value
        if labels is None:
            self.labels = {}
        else:
            assert type(labels) == dict, "Labels should be dictionary"
            self.labels = labels
    
    def get_value(self):
        return self.value

    def get_copy(self):
        return copy.deepcopy(self)
    
    def get_labels(self):
        return self.labels
    
    def get_label(self, key):
        assert key in self.labels.keys()
        return self.labels[key]

    def set_label(self, key, value):
        self.labels[key] = value
    
    def __str__(self):
        string = str(self.value)
        return string
    
    

# for field representation
class Graph:
    def __init__(self, values=None):
        if values is None:
            self.nodes = []
            # edges: [ [value1,weight1], [value2,weight2], ...]
            self.edges = {}
        else:
            self.nodes = []
            self.edges = {}
            for i in range(len(values)):
                node = Node(values[i])
                self.nodes.append(node)
                self.edges[values[i]] = []
    
    # node wasn't created yet
    def add_new_node(self, value, labels=None):
        assert value not in [node.value for node in self.nodes], "Already exists"
        if labels is None:
            self.nodes.append(Node(value))
            self.edges[value] = []
        else:
            self.nodes.append(Node(value, labels))
            self.edges[value] = []

    # node was created before (may not be needed)
    #def add_node(self, node):
    #    self.nodes.append(node)
    
    def find_node(self, value):
        for node in self.nodes:
            #print(str(node.value) + "; " + str(value))
            if node.value == value:
                return node
        return None
    
    # possible directed graphs
    def add_neighbor(self, value1, value2, weight=1):
        self.edges[value1].append([value2, weight])

    def add_edge(self, value1, value2, weight=1):
        #print(len(self.nodes))
        node1 = self.find_node(value1)
        node2 = self.find_node(value2)

        if (node1 is not None) and (node2 is not None):
            #print("Not none :)")
            #print(weight)
            self.add_neighbor(value1, value2, weight)
            self.add_neighbor(value2, value1, weight)
        else:   # not good
            print("Node(s) not found:\t" + str(value1) + ", " + str(value2))
    
    def add_edges(self, value, edges):
        assert value in [node.value for node in self.nodes], str(value) + " doesn't exist"
        for edge in edges:
            if not edge in self.edges[value]:
                self.edges[value].append(edge)
        #self.edges[value] += edges

    
    def number_of_nodes(self):
        return len(self.nodes)
    
    def are_connected(self, value1, value2):
        #node1 = self.find_node(value1)
        #node2 = self.find_node(value2)
        return value2 in [pos[0] for pos in self.edges[value1]]     # pos[1] is weight
    
    def get_nodes(self):
        return self.nodes
    
    def get_copy(self):
        return copy.deepcopy(self)
    
    # includes non-existing edges in subgraph
    def get_subgraph(self, nValues):
        values = [node.value for node in self.nodes]
        assert type(nValues) == list, "Nodes should be list"
        #assert set(nValues) <= set(values), "Not a subset"
        nValues = set(nValues).intersection(set(values))

        '''values = []
        #print(nValues)
        for node in self.nodes:
            #print(node)
            if node.get_value() in nValues:
                values.append(node)
                print(node)'''
        
        g = Graph()
        for value in nValues:
            #print(value)
            #print(value in self.edges.keys())
            #print(self.edges[value])
            g.add_new_node(value)
            g.add_edges(value, self.edges[value])  # add all extra edges
        
        return g


    # remove edges if nodes doesn't exist in graph
    '''def clean(self):
        values = [node.value for node in self.nodes]
        newNodes = copy.deepcopy(self.nodes)
        #print(values)
        for node in self.nodes:
            i = 0
            while i < len(self.edges[node.value]):
                neighbors = node.get_neighbors()
                nValues = [n[0].value for n in neighbors]
                #print(nValues)
                if not nValues[i] in values:
                    neighbors.remove(neighbors[i])
                    i -= 1
                i += 1
                neighbors = [e.get_value() for e in self.edges[node.value]]
                if not neighbors[i] in values:
                    newNodes.remove(neighbors[i])
                    i -= 1
                i += 1'''
    
    def clean(self):

        # for each node and each edge check if connection exists
        values = [node.value for node in self.nodes]
        #print(values)
        
        for value in values:
            edges = self.edges[value]

            self.edges[value] = list(filter(lambda v: v[0] in values, edges))

    
    # vertices vertically
    def __str__(self):
        string = ""
        for node in self.nodes:
            string += str(node) + ": " + str(self.edges[node.value]) + "\n"
        return string
    
    # some additional methods need to be found


''' testCapture.lay
%%%%%%%%%%%%
%        24%
%      %%%%%
%%%%%      %
%13     o  %
%%%%%%%%%%%%
'''
def generate_graph_from_layout(layout, reverse=False):
    nodes = []
    for i in range(len(layout)-1):
        for j in range(len(layout[i])):
            coordinates = (i,j)
            if (layout[i][j] != "%"):
                if (reverse):
                    nodes.append(Node((j,len(layout)-i-2)))
                else:
                    nodes.append(Node(coordinates))
    
    graph = Graph([n.get_value() for n in nodes])

    #for n in graph.get_nodes():
    #    print(n)

    for node in graph.get_nodes():
        coordinates = node.get_value()
        #print(coordinates)
        # check if neighbors right or down exist - if exist add connection
        # right
        coordinatesN = (coordinates[0], coordinates[1]+1)
        nodeN = graph.find_node(coordinatesN)
        if nodeN is not None:
            graph.add_edge(coordinates, coordinatesN)
        # down
        coordinatesN = (coordinates[0]+1, coordinates[1])
        #print(coordinatesN)
        nodeN = graph.find_node(coordinatesN)
        if nodeN is not None:
            graph.add_edge(coordinates, coordinatesN)
    
    return graph

# ex. for finding number of coins in neighborhood
# expand subgraph with connected vertices to subgraph
def expand_subgraph(graph, subgraph):
    assert type(graph) == Graph, "Wrong type" 
    assert type(subgraph) == Graph, "Wrong type"    # should be right type
    
    '''existingNodes = subgraph.get_nodes()
    newGraph = subgraph.get_copy()
    for node in existingNodes:
        for neighbor in node.get_neighbors():
            if not neighbor in newGraph.get_nodes():
                newGraph.add_node(neighbor[0])'''
    values = [node.get_value() for node in graph.get_nodes()]
    sValues = [node.get_value() for node in subgraph.get_nodes()]
    newGraph = subgraph.get_copy()

    for value in sValues:
        #print(value)
        edges = graph.edges[value]
        newGraph.add_edges(value, edges)
    
    #print(newGraph)

    for value in values:
        for sValue in sValues:
            edges = [edge[0] for edge in graph.edges[sValue]]
            if value in edges and not value in sValues:
                #print(graph.edges[value])
                newGraph.add_new_node(value)
                newGraph.add_edges(value, graph.edges[value])
                break

    return newGraph

def visualize(layout, graph):
    nodes = graph.get_nodes()
    #print(graph)
    #print([node.get_value() for node in nodes])
    out = ""
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            if (layout[i][j] == "%"):
                #print("%", end="")
                out += "%"
            elif (len(layout)-i-1,j) in [node.get_value() for node in nodes]:
                out += "x"
            else:
                #print(layout[i][j], end="")
                out += layout[i][j]
        out += "\n"
    print(out)