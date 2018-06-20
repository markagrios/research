from brian2 import *
import networkx as nx
import numpy as np
import math
import cmath
import csv
import time as TIME
import matplotlib.pyplot as plt
import sys

G = nx.Graph()

G.add_edges_from([
    [1,2],[1,3],[1,5],
    [2,4],[2,5],
    [3,5],[3,11],
    [4,5],[4,6],
    [5,6],[5,10],[5,11],
    [6,7],[6,8],
    [7,8],[7,9],
    [8,13],[8,14],
    [9,14],
    [10,13],
    [11,12],[11,13],[11,20],[11,21],
    [12,13],
    [13,15],
    [14,15],[14,16],[14,17],
    [15,18],[15,20],
    [17,18],
    [18,19],
    [19,20],[19,21]
])

N = G.number_of_nodes()
print(N)

qwe = array(nx.to_numpy_matrix(G))
adj_matrix = np.zeros((N,N), dtype=int)
for i in range(0,N):
    for j in range(0,N):
        adj_matrix[i][j] = int(qwe[i][j])

print(adj_matrix)
# np.savetxt("preBotC.csv", adj_matrix, delimiter=",", fmt='%s')


nx.draw_kamada_kawai(G, with_labels=True, font_weight='bold')
# nx.draw_shell(G, with_labels=True, font_weight='bold')
plt.show()
