import numpy as np
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


sc = getsimps("ER_n330p0125-subgraph15")
K = SimplicialComplex(simplices=sc)

print(K.betti_number(0))
print(K.betti_number(1))
print(K.betti_number(2))













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
