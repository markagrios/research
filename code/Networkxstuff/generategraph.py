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

n = 33
p = 0.1

G = nx.erdos_renyi_graph(n,p,directed=True)

N = G.number_of_nodes()
print(N)

qwe = array(nx.to_numpy_matrix(G))
adj_matrix = np.zeros((N,N), dtype=int)
for i in range(0,N):
    for j in range(0,N):
        adj_matrix[i][j] = int(qwe[i][j])

print(adj_matrix)

np.savetxt("ER_n" + str(n) + "p" +str(p) + "_D" + ".csv", adj_matrix, delimiter=",", fmt='%s')
# np.savetxt("ER_n" + str(n) + "p" +str(p) + ".csv", adj_matrix, delimiter=",", fmt='%s')


nx.draw_kamada_kawai(G)
plt.show()
