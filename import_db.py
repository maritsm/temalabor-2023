#!/usr/bin/python3

#TODO: decide whether to use pandas or networkx
# we're using networkx for now

import networkx as nx
import matplotlib.pyplot as plt
import csv

def createNxGraph(filename):
    G = nx.Graph()
    with open(filename, 'r') as inputfile:
        csvr = csv.reader(inputfile, delimiter=',')
        for line in csvr:
            #print(line)
            # we add an edge between the ID of the proposition
            # and the ID of the MEP
            G.add_edge(line[0], line[6])
    return G

if __name__ == "__main__":
    myGraph = createNxGraph("db/ep_cosponsorship_dataset.csv")
    
    print(f"Some information about this graph:\n"
          f"Number of nodes: {nx.number_of_nodes(myGraph)}\n"
          f"Number of edges: {nx.number_of_edges(myGraph)}\n")