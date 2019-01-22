from brian2 import *
import networkx as nx
import numpy as np
import math
import cmath
import csv
import time as TIME
import matplotlib.pyplot as plt
import sys
from random import randint

G = nx.erdos_renyi_graph(33,0.125,directed=True)

N = G.number_of_nodes()
print(N)

qwe = array(nx.to_numpy_matrix(G))
adj_matrix = np.zeros((N,N), dtype=int)
for i in range(0,N):
    for j in range(0,N):
        adj_matrix[i][j] = int(qwe[i][j])

print(adj_matrix)

np.savetxt("small_ER_n33p0125.csv", adj_matrix, delimiter=",", fmt='%s')


nx.draw_kamada_kawai(G)
plt.show()
