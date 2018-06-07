import networkx as nx
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/osboxes/gudhi/build/cython')
import gudhi


def drawGraph(matrix):

    with open("connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    G = nx.DiGraph()
    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                G.add_edge(ri,ci)

    nx.draw_shell(G, with_labels=True, font_weight='bold')
    plt.show()


def raiseton(matrix,n):
    Nmatrix = np.linalg.matrix_power(matrix,n)
    for i in range(len(Nmatrix[0])):
        Nmatrix[i][i] = 0

    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            if(Nmatrix[i][j] >= 1):
                Nmatrix[i][j] = n
            else:
                Nmatrix[i][j] = 0

    return Nmatrix

def takeminpaths(matrix1,matrix2):     # creates a new matrix by taking the min of each entry of two matrices
    newmatrix = matrix1
    for i in range(len(matrix1[0])):
        for j in range(len(matrix1[0])):
            newmatrix[i][j] = min(matrix1[i][j],matrix2[i][j])

    return newmatrix

def getpowers(matrixarray):
    # iterate through to some number and then add to array to get sequence of min path length matrices
    M0 = matrixarray[0]

    for i in range(2,SIZE+1): # instead of SIZE+1 this should just be the length of the longest path in the graph
        newmatrix = raiseton(M0,i)
        matrixarray.append(newmatrix)

    # return matrixarray[1:]
    return matrixarray

def decompose(matrix):
    N = len(matrix[0])

    paths = []
    for i in range(N):
        for j in range(N):
            paths.append(matrix[i][j])

    maxpath = np.max(paths)
    # print(maxpath)
    decomp = []

    for k in range(0,maxpath+1):
        part = np.zeros((N,N), dtype=int)
        for i in range(0,N):
            for j in range(0,N):
                if(matrix[i][j] == k):
                    part[i][j] = k
        decomp.append(part)

    return(decomp)

def getSimpsfromGraph(G):
    undG = G.to_undirected()
    simps = sorted(nx.find_cliques(undG))
    # for i in range(0,N):
    #     simps.append(i)

    simps = simps[::-1]

    return(simps)

################################################################################

matrix = sys.argv[1] + ".csv"

M = []
reader = csv.reader(open("../connection_matrices/" + matrix, "rb"), delimiter=",")
x = list(reader)
M.append(np.array(x).astype("int"))

ROWS = len(M[0])
COLUMNS = len(M[0])
SIZE = len(M[0])

M[0] = np.maximum(M[0], M[0].transpose())

print(M[0])

powerlist = getpowers(M)
# for i in range(len(powerlist)):
#     print powerlist[i]
#     print("~")

print("---------")

richM = np.zeros((ROWS,COLUMNS), dtype=int)
for k in range(len(powerlist)):
    richM = np.add(richM,powerlist[k])
    for i in range(len(richM)):
        for j in range(len(richM)):
            if(richM[i][j] > k+1):
                richM[i][j] -= k+1

print(richM)

print("---------")

N = len(richM[0])

G = nx.Graph()
G.add_nodes_from(range(0,N))

for i in range(N):
    for j in range(N):
        if(M[0][i][j] > 0):
            G.add_edge(i,j)


print("----decompisition-----")
D = decompose(richM)
for i in D:
    print(i)

print("----filtration--------")

graphFiltration = []
for i in range(len(D)):
    graphFiltration.append(sum(D[:i+1]))

# for filt in graphFiltration:
#     print(filt)

SimpComp = gudhi.SimplexTree()
SimpComp.set_dimension(len(D))

for i in range(N):
    SimpComp.insert([i],0)

for i in range(1,len(D)):
    # print(D[i])
    graph = nx.Graph()
    for ri in range(len(graphFiltration[i][0])):
        for ci in range(len(graphFiltration[i][0])):
            if(graphFiltration[i][ri][ci] != 0):
                graph.add_edge(ri,ci)

    simplist = getSimpsfromGraph(graph)

    for j in range(len(simplist)):
        SimpComp.insert(simplist[j],i)

    nx.draw_shell(graph,with_labels=True)
    plt.show()

SimpComp.initialize_filtration()

# This takes like a super long time to print out..
# print("Filtration:")
# for i in range(len(SimpComp.get_filtration())):
#     print(SimpComp.get_filtration()[i])

p = SimpComp.persistence()

perscolors = ["red","green","blue","cyan","magenta","yellow","black","maroon","chartreuse?","azure","a very unappealing yellowish green","purple","blue-grey"]
for dim in range(len(SimpComp.get_filtration()[-1])+3):
    print("Persistence of dim " + str(dim) + " (" + perscolors[dim] + ")" + ": ")
    for i in SimpComp.persistence_intervals_in_dimension(dim):
        print("   " + str(i))

print("---")
print("Betti numbers: ")
print("   " + str(SimpComp.betti_numbers()))

gudhi.plot_persistence_diagram(p)

nx.draw_shell(G,with_labels=True)
plt.show()
