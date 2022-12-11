import copy
import numpy as np
#from clustering.clustering_algorithm import *
from matplotlib import pyplot as plt

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
                self.edges[values[i]] = {}
    
    # node wasn't created yet
    def add_new_node(self, value, labels=None):
        assert value not in [node.value for node in self.nodes], "Already exists"
        if labels is None:
            self.nodes.append(Node(value))
            self.edges[value] = {}
        else:
            self.nodes.append(Node(value, labels))
            self.edges[value] = {}

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
        self.edges[value1][value2] = weight

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
        #print(self.edges[value])
        for edge in edges.keys():
            #print("hehe")
            #print("edge: " + str(edge))
            #print(type(self.edges[value]))
            #print(value)
            if not edge in self.edges[value]:
                self.edges[value][edge] = edges[edge]
            #print(self.edges[value])
        #self.edges[value] += edges

    
    def number_of_nodes(self):
        return len(self.nodes)
    
    def are_connected(self, value1, value2):
        return value1 in self.get_edges()[value2].keys() or value2 in self.get_edges()[value1].keys()
    
    def get_nodes(self):
        return self.nodes
    
    def get_edges(self):
        return self.edges
    
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
            to_remove = []

            #self.edges[value] = list(filter(lambda v: v[0] in values, edges))
            for edge in edges.keys():
                if not edge in values:
                    to_remove.append(edge)
            for e in to_remove:
                edges.pop(e, None)

    
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
def generate_graph_from_layout(layout):
    nodes = []
    for i in range(1,len(layout)-3):
        for j in range(1,len(layout[i])-1):
            #print(str((i,j)) + " -> " + str((j,len(layout)-i-3)) + ": " + str(layout[i][j]))
            if (layout[i][j] != "%"):
                nodes.append(Node((j,len(layout)-i-3)))
    
    graph = Graph([n.get_value() for n in nodes])
    #print([node.value for node in graph.get_nodes()])
    #print([node.value for node in nodes])
    #print((1,1) in [node.value for node in graph.get_nodes()])

    for x in range(1, len(layout[0])):
        for y in range(1, len(layout)):
            #print(str((x,y)))
            if ((x,y) in [node.value for node in graph.get_nodes()]):
                #print(str((x,y)))
                pass
    

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
        newGraph.add_edges(value, graph.edges[value])
    
    #print(newGraph.edges)

    for value in values:
        for sValue in sValues:
            edges = graph.edges[sValue].keys()
            if value in edges and not value in sValues:
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

def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    #print(unvisited_nodes)
    unvisited_nodes = [node.get_value() for node in unvisited_nodes]
    shortest_path = {}
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = float("inf")
    for node in unvisited_nodes:
        shortest_path[node] = max_value

    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        #for e in graph.get_edges():
        #    print(str(e) + ": " + str(graph.get_edges()[e]))
        #print(type(current_min_node))
        #print(graph.get_edges()[current_min_node])
        neighbors = graph.get_edges()[current_min_node].keys()
        costs = graph.get_edges()[current_min_node].values()
        #print(costs)

        for neighbor in neighbors:
            #iss = graph.get_edges()[current_min_node]
            e = graph.get_edges()[current_min_node]
            #print(e)
            #print(e[neighbor])
            tentative_value = shortest_path[current_min_node] + e[neighbor]
            #tentative_value = shortest_path[current_min_node] + graph.get_edges()[current_min_node] neighbor
            #tentative_value = shortest_path[current_min_node] + 1
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
        unvisited_nodes.remove(current_min_node)
    return previous_nodes, shortest_path


# note: very important function
# returns whether movement in certain direction traps agent
# assuming curr_position and new_position are neighboring and
# movement from curr_position to new_position
# barriers: dodane ovire (npr. duhec na poti)
def is_trap(graph, curr_position, new_position, barriers=[]):
    graph2 = graph.get_copy()
    # delete edge
    graph2.edges[curr_position].pop(new_position, None)
    graph2.edges[new_position].pop(curr_position, None)
    for barrier in barriers:
        #print(barrier)
        node = graph2.get_nodes()[barrier]
        graph2.get_nodes().remove(node)
    graph2.clean()
    # calculate paths
    previous_nodes, shortest_path = dijkstra_algorithm(graph2, new_position)
    #print((shortest_path))
    # if not enough exist -> trap
    return sum(1 for v in shortest_path.values() if v == float('inf')) >= len(shortest_path) / 2

def get_bordering_fields(graph, layout, is_red, my_border):
    xMin = 1
    xMax = len(layout[0])-2
    yMin = 1
    yMax = len(layout)-2
    xL = (xMin+xMax)//2
    xR = xL + 1
    fieldsL = []
    fieldsR = []
    for i in range(yMin, yMax+1):
        if (xL,i) in [node.value for node in graph.nodes]:
           fieldsL.append((xL, i))
        if (xR,i) in [node.value for node in graph.nodes]:
            fieldsR.append((xR, i))
    
    if is_red ^ my_border:
        return fieldsR
    else:
        return fieldsL

def return_min_len_to_fields(graph, pos, fields):
    previous_nodes, shortest_path = dijkstra_algorithm(graph, pos)
    print(fields)
    print(shortest_path.keys())
    distances = {key: shortest_path[key] for key in fields}
    for p in distances:
        print(str(p) + ": " + str(distances[p]))
    #print(shortest_path)
    return min(distances.values())