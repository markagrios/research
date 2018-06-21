from brian2 import *
import networkx as nx
import numpy as np
import math
import cmath
import csv
import time as TIME
import matplotlib.pyplot as plt
import sys


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

H = G.subgraph(range(50,70))

N = H.number_of_nodes()
print(N)

qwe = array(nx.to_numpy_matrix(H))
adj_matrix = np.zeros((N,N), dtype=int)
for i in range(0,N):
    for j in range(0,N):
        adj_matrix[i][j] = int(qwe[i][j])

print(adj_matrix)
np.savetxt(matrix[:-4]+"-subgraph.csv", adj_matrix, delimiter=",", fmt='%s')


nx.draw_kamada_kawai(H, with_labels=True, font_weight='bold')
# nx.draw_shell(H, with_labels=True, font_weight='bold')
plt.show(block=False)

savesim = raw_input("save graph? ")
if(savesim == 'y'):
    simname = raw_input("network name: ")
    if(simname == ''):
        simname = matrix[:-4]+"-subgraph"
    # plt.savefig('../networks/' + simname + '.png')
    plt.savefig(simname + '.png')
