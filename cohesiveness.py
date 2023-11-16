import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime

def cohesiveness(Graph, VertexSet):
    # purely graph-theoretic function
    
    H = nx.induced_subgraph(Graph, VertexSet)
    n = H.number_of_nodes()
    e = H.number_of_edges()

    if n in [0,1]:
        return 0
    else:
        return (2*e)/(n*(n-1)) ## proportion of edges