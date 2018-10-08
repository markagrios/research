import os
import sys
import random
import numpy as np
import cPickle as pickle

# example run: python thewholedeal.py ER_n330p0125-subgraph15 20
# runs 20 ablations.

def sublist(lst1, lst2):
    one = lst1
    two = lst2
    return(set(one).intersection(set(two)) == set(one))

def getsimps(simpfile):
    simpfile = simpfile + "_dlist.csv"
    simps = []
    for line in open("../connection_matrices/simp_lists/" + simpfile):
        simps.append(line.split())

    # print(simps)
    # print("---")

    synapses = []
    for i in range(len(simps)):
        if(len(simps[i]) == 2):
            synapses.append(simps[i])

    return(synapses,simps)


def check_homology(syn, simp_list):
    higher = []
    index = 0
    for i in range(len(simp_list)):
        if(len(simp_list[i]) < 3):
            index += 1

    for i in range(index,len(simp_list)):
        if(sublist(syn, simp_list[i]) == True):
            higher.append(simp_list[i])

    # print(higher)
    # print("---")

    if(len(higher) == 0):
        return(True)

    if(len(higher) >= 1):
        lengths = [0,0,0,0,0,0,0,0,0]
        for i in range(len(higher)):
            lengths[len(higher[i])-1] += 1

    for i in range(len(lengths)):
        if(lengths[-1*i] != 0):
            if(lengths[-1*i] == 1):         # synapse is a free face -> synapse is not essential
                return(False)
            if(lengths[-1*i] > 1):          # synapse is essential
                return(True)

    # return(lengths)

def generate_ablation_list(syn_list, simp_list):
    ablations_index = np.random.choice(len(syn_list), int(numabl), replace=False)
    ablations = []
    for i in range(len(ablations_index)):
        ablations.append(syn_list[ablations_index[i]])

    # for i in range(len(ablations)):
    #     for j in range(len(ablations[i])):
    #         ablations[i][j] = str(int(ablations[i][j]) - 1)

    change_hom = []
    alist = []

    for i in range(len(ablations)):
        alist.append("-".join(ablations[i]))
        change_hom.append(check_homology(ablations[i], simp_list))

    for i in range(len(alist)):
        syn = alist[i].split("-")
        neu1 = int(syn[0])-1
        neu2 = int(syn[1])-1
        newsyn = [str(neu1),str(neu2)]
        alist[i] = "-".join(newsyn)

    return(alist,change_hom)

def multiindex(element, lst):
    index_list = []
    for i in range(len(lst)):
        if(lst[i] ==  element):
            index_list.append(i)

    return(index_list)

################################################################################

network = sys.argv[1]
numabl = sys.argv[2]

if(len(numabl) > 0):
    ablation_list = sys.argv[2]
    ablation_list = ablation_list.split(",")
    pickle.dump(ablation_list, open("storeddata/homo.p","wb"))
    print(ablation_list)
else:
    SYNS = getsimps(network)[0]
    SIMPS = getsimps(network)[1]

    AH = generate_ablation_list(SYNS,SIMPS)
    ablation_list = AH[0]
    H = AH[1]
    pickle.dump(H, open("storeddata/homo.p","wb"))
    print(ablation_list)
    print(H)
    print(multiindex(True,H))

command = "python ablate.py " + network

print("---")

qcontinue = raw_input("continue with this ablation sequence? ")
if(qcontinue == "y"):
    os.system(command + " q []")           # just to stabilize the network
    os.system(command + " cont []")        # just to run it once

    for i in range(len(ablation_list)):
        argpassed = "python ablate.py " + network + " cont " + ",".join(ablation_list[:i+1])
        print("Now ablating neuron: " + ablation_list[i])
        os.system(argpassed)


    os.system("python plot.py " + network)
