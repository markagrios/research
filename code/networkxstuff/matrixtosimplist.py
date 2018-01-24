import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import csv

# G = nx.DiGraph()
G = nx.Graph()

# with open("connection_matrices/"+matrix) as csvfile:
matrix = "6weird.csv"
with open(matrix) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    a = list(readCSV)

for ri in range(len(a[0])):
    for ci in range(len(a[0])):
        if(a[ri][ci] != "0"):
            print(ri,ci)
            G.add_edge(ri,ci)

print(G.nodes())
print(G.edges())
# nx.draw(G)
# plt.show()
print(nx.find_cliques(G))
