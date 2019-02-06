import sys
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt
from mogutda import SimplicialComplex

def getsimps(simpfile):
    simpfile = simpfile + "_dlist.csv"
    simps = []
    for line in open("../connection_matrices/simp_lists/" + simpfile):
        line = line.rstrip()
        oneD = [-1]
        if " " in line:
            line = line.split(" ")
            for n in range(len(line)):
                line[n] = int(line[n])
            simps.append(tuple(line))
        else:
            oneD[0] = int(line)
            simps.append(oneD)

    # print(simps)
    return(simps)

def ablateN(simpcomp,neuron):
    newSC = []
    neuron = int(neuron)
    for i in range(len(simpcomp)):
        if neuron not in simpcomp[i]:
            newSC.append(simpcomp[i])

    return newSC

def preserves_homology(SC1,SC2):
    K1 = SimplicialComplex(simplices=SC1)
    K2 = SimplicialComplex(simplices=SC2)

    bettis = 0
    for i in range(3):
        bettis += K2.betti_number(i)-K1.betti_number(i)

    if(bettis == 0):
        return("X")
    else:
        return("S")

def check_homology(initSC,abllist):
    SC = initSC
    homolist = []
    K = SimplicialComplex(simplices=SC)
    print(K.betti_number(0),K.betti_number(1),K.betti_number(2))

    betas = [[K.betti_number(0)],[K.betti_number(1)],[K.betti_number(2)]]

    for i in range(0,len(abllist)):
        homolist.append(preserves_homology(SC,ablateN(SC,int(ablation_list[i]))))
        SC = ablateN(SC,int(ablation_list[i]))
        K = SimplicialComplex(simplices=SC)
        print(K.betti_number(0),K.betti_number(1),K.betti_number(2))
        betas[0].append(K.betti_number(0))
        betas[1].append(K.betti_number(1))
        betas[2].append(K.betti_number(2))


    pickle.dump(betas, open("storeddata/betas.p","wb"))
    # print(SC)
    return(homolist)




################################################################################

matrix = sys.argv[1]
ablation_list = sys.argv[2].split(",")


print(ablation_list)

simplist = getsimps(matrix)
homo = check_homology(simplist,ablation_list)
# pickle.dump(homo, open("storeddata/homo.p","wb"))
betas = pickle.load(open("storeddata/betas.p", "rb"))
print(betas)

homXS = []
for i in range(len(ablation_list)):
    ablation_list[i] = str(ablation_list[i])
    homXS.append((ablation_list[i], homo[i]))

print(homXS)
pickle.dump(homXS, open("storeddata/homXS.p", "wb"))
