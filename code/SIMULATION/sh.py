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

def preserves_homology(SC1,SC2): # True for keeps homology, False for changes it
    K1 = SimplicialComplex(simplices=SC1)
    K2 = SimplicialComplex(simplices=SC2)

    # betti = [K2.betti_number(0)-K1.betti_number(0),K2.betti_number(1)-K1.betti_number(1),K2.betti_number(2)-K1.betti_number(2),K2.betti_number(3)-K1.betti_number(3)]

    bettis = tuple(np.subtract((K1.betti_number(0),K1.betti_number(1),K1.betti_number(2)),(K2.betti_number(0),K2.betti_number(1),K2.betti_number(2))))

    return(bettis)

def check_homology(initSC,abllist):
    SC = initSC
    homolist = []
    K = SimplicialComplex(simplices=SC)
    print(K.betti_number(0),K.betti_number(1),K.betti_number(2))
    for i in range(0,len(abllist)):
        homolist.append(preserves_homology(SC,ablateN(SC,int(ablation_list[i]))))
        SC = ablateN(SC,int(ablation_list[i]))
        K = SimplicialComplex(simplices=SC)
        print(K.betti_number(0),K.betti_number(1),K.betti_number(2))

    print(SC)
    return(homolist)

##########################
simps = sys.argv[1]
neuron1 = int(sys.argv[2])
neuron2 = int(sys.argv[3])

SC = getsimps(simps)
K = SimplicialComplex(simplices=SC)
print(ablateN(SC,int(neuron1)))
print(preserves_homology(SC,ablateN(SC,neuron1)))
SC = ablateN(SC,neuron1)
print(preserves_homology(SC,ablateN(SC,neuron2)))








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
