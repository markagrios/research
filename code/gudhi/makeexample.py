import networkx as nx
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/mark/gudhi/build/cython')
import gudhi

def filtmetric(statevariablelist):
    sumdist = 0
    countdist = 0
    for i in range(len(statevariablelist)):
        for j in range(len(statevariablelist)):
            if(i < j):
                sumdist += abs(statevariablelist[i] - statevariablelist[j])
                countdist += 1

    if(countdist == 0):
        countdist += 1

    # meandist = sumdist/countdist
    meandist = sumdist/len(statevariablelist)     # this actually works with the set simplex to lower filt value than faces porblem. Not sure why, but it does
    metric = max(statevariablelist) + meandist
    return(metric)


SC = [[0],[1],[2],[3],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3],[0,1,2],[0,1,3],[0,2,3],[1,2,3],[0,1,2,3]]
vertex_sv_list = [1.7,1.2,2.3,2.1]

st = gudhi.SimplexTree()
st.set_dimension(len(SC[-1]))
st.initialize_filtration()


for i in range(len(SC)):
    sv_of_clique = []
    for j in range(len(SC[i])):
        sv_of_clique.append(vertex_sv_list[SC[i][j]])

    st.insert(SC[i],filtmetric(sv_of_clique))





print("dimension of simplicial complex: " + str(st.dimension()))
print("---")

print("Filtration:")
for i in range(len(st.get_filtration())):
    print(st.get_filtration()[i])

p = st.persistence()

print("---")
perscolors = ["red","green","blue","cyan","magenta","yellow","black","maroon","chartreuse?","azure","a very unappealing yellowish green","purple","blue-grey"]
for dim in range(len(st.get_filtration()[-1])+3):
    print("Persistence of dim " + str(dim) + " (" + perscolors[dim] + ")" + ": ")
    for i in st.persistence_intervals_in_dimension(dim):
        print("   " + str(i))

print("---")
print("Betti numbers: ")
print("   " + str(st.betti_numbers()))

gudhi.plot_persistence_diagram(p)
