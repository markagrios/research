import networkx as nx
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/mark/gudhi/build/cython')

# def N_from_Matrix(matrix):
#     with open("connection_matrices/"+matrix) as csvfile:
#         readCSV = csv.reader(csvfile, delimiter=',')
#         a = list(readCSV)
#
#     return(len(a))
#
# def count_connections(matrix):
#     n = 0
#     with open("connection_matrices/"+matrix) as csvfile:
#         readCSV = csv.reader(csvfile, delimiter=',')
#         a = list(readCSV)
#
#     for ri in range(len(a[0])):
#         for ci in range(len(a[0])):
#             if(a[ri][ci] != "0"):
#                 n += 1
#
#     return(n)

def connect_from_Matrix(nxgraph,matrix):
    with open(matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                nxgraph.add_edge(ri,ci)

G = nx.Graph()

connect_from_Matrix(G,"celegans131matrix.csv")

N = len(G.nodes())
Nsyn = len(G.edges())
rawcliques = zip(nx.find_cliques_recursive(G))      # this just finds maximal cliques so maybe that's why it's falling short of the neurotop answer


cliques = []
for i in range(len(rawcliques)):
    cliques.append(rawcliques[i][0])

# print("---")
# print(len(rawcliques))
# print(rawcliques[123][0])

# print(cliques)

print(131+687+639+207+29+1)
print(N + Nsyn + len(cliques))

# print(nx.graph_number_of_cliques(G))
print(nx.graph_clique_number(G))
