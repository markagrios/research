import numpy as np
import sys
from mogutda import SimplicialComplex

def getsimps(simpfile):
    simpfile = simpfile + "_dlist.csv"
    simps = []
    for line in open("../connection_matrices/simp_lists/" + simpfile):
        line = line.rstrip()
        if " " in line:
            line = line.split(" ")
            for n in range(len(line)):
                line[n] = int(line[n])
            simps.append(tuple(line))

    return(simps)

def ablateN(simpcomp,neuron):
    newSC = []
    for i in range(len(simpcomp)):
        if neuron not in simpcomp[i]:
            newSC.append(simpcomp[i])

    return newSC


simplist = sys.argv[1]
neuron = sys.argv[2]

# sc = getsimps("ER_n330p0125-subgraph15")
sc = getsimps(simplist)
K1 = SimplicialComplex(simplices=sc)
print(K1.betti_number(0),K1.betti_number(1),K1.betti_number(2))
print("---")
K2 = SimplicialComplex(simplices=ablateN(sc,neuron))
print(K2.betti_number(0),K2.betti_number(1),K2.betti_number(2))


print("=============")
betti = 0
for i in range(2):
    betti += (K2.betti_number(i)-K1.betti_number(i))

print(betti)









# sc = [(0,1),(1,2),(0,2),(0,1,2),(1,3),(2,3)]
# K = SimplicialComplex(simplices=sc)
#
# print(K.betti_number(0))
# print(K.betti_number(1))
# print(K.betti_number(2))
#
# # sc.remove((3,4))
# # K = SimplicialComplex(simplices=sc)
# #
# # print("---")
# # print(K.betti_number(0))
# # print(K.betti_number(1))
# # print(K.betti_number(2))
