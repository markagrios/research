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


def longest(l):
    if(not isinstance(l, list)): return(0)
    return(max([len(l),] + [len(subl) for subl in l if isinstance(subl, list)] + [longest(subl) for subl in l]))

################################################################################


matrix = sys.argv[1] + ".csv"

def connect_from_Matrix(nxgraph,matrix):


    with open("../connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                nxgraph.add_edge(ri,ci)

    return(nxgraph)

G = nx.DiGraph()
G = connect_from_Matrix(G,matrix)


num = randint(0,257)
# num = 36
H = G.subgraph(range(num,num+33))
print(num,num+33)
# print(nx.is_connected(H.to_undirected()))
# print(nx.number_connected_components(H.to_undirected()))

cc = nx.connected_components(H.to_undirected())
cc = list(cc)
maxcc = list(max(cc, key=len))
print(len(maxcc))

H = G.subgraph(maxcc)


print("---")


N = H.number_of_nodes()
print(N)

qwe = array(nx.to_numpy_matrix(H))
adj_matrix = np.zeros((N,N), dtype=int)
for i in range(0,N):
    for j in range(0,N):
        adj_matrix[i][j] = int(qwe[i][j])

print(adj_matrix)

nx.draw_kamada_kawai(H, with_labels=True, font_weight='bold')
# nx.draw_shell(H, with_labels=True, font_weight='bold')
plt.show(block=False)

savesim = raw_input("save graph? ")
if(savesim == 'y'):
    simname = raw_input("network name: ")
    if(simname == ''):
        simname = matrix[:-4]+"-subgraph" + str(num)
    # plt.savefig('../networks/' + simname + '.png')
    plt.savefig(simname + '.png')
    np.savetxt(matrix[:-4]+"-subgraph" + str(num) + ".csv", adj_matrix, delimiter=",", fmt='%s')
