import os
import sys
import random
import numpy as np
import cPickle as pickle
from mogutda import SimplicialComplex

# example run: python thewholedeal.py ER_n330p0125-subgraph15 20
# runs 20 ablations.

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

def preserves_homology(SC1,SC2): # True for keeps homology, False for changes it
    K1 = SimplicialComplex(simplices=SC1)
    K2 = SimplicialComplex(simplices=SC2)

    bettis = 0
    for i in range(3):
        bettis += K2.betti_number(i)-K1.betti_number(i)

    if(bettis == 0):
        return("X?")
    else:
        return("S?")

    # return(bettis)

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

def multiindex(element, lst):
    index_list = []
    for i in range(len(lst)):
        if(lst[i] ==  element):
            index_list.append(i)

    return(index_list)

################################################################################

network = sys.argv[1]
numabl = sys.argv[2]

if("," in numabl):
    ablation_list = sys.argv[2]
    ablation_list = ablation_list.split(",")
    pickle.dump(ablation_list, open("storeddata/ablationlist.p","wb"))
    print(ablation_list)
if(numabl == "r"):
    numabl = raw_input("how many ablations? ")
    ablation_list = list(np.random.choice(32, int(numabl), replace=False ))
    for i in range(len(ablation_list)):
        ablation_list[i] = int(ablation_list[i])
    pickle.dump(ablation_list, open("storeddata/ablationlist.p","wb"))
    print(ablation_list)

# networksimps = getsimps(network)
# homo = check_homology(networksimps,ablation_list)
# pickle.dump(homo, open("storeddata/homo.p","wb"))
command = "python ablate.py " + network
for i in range(len(ablation_list)):
    ablation_list[i] = str(ablation_list[i])
    # print(ablation_list[i], homo[i])





print("---")

qcontinue = raw_input("continue with this ablation sequence? ")
if(qcontinue == "y"):
    os.system(command + " q []")           # just to stabilize the network
    os.system(command + " cont []")        # just to run it once

    for i in range(len(ablation_list)):
        argpassed = "python ablate.py " + network + " cont " + ",".join(ablation_list[:i+1])
        # argpassed = "python ablate.py " + network + " cont " + str(ablation_list)
        print("Now ablating neuron: " + ablation_list[i])
        os.system(argpassed)


    os.system("python plot.py " + network)
