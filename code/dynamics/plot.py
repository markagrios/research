from brian2 import *
import networkx as nx
import numpy as np
import math
import cmath
import csv
import time as TIME
import matplotlib.pyplot as plt
import sys
import cPickle as pickle

def make_NX_graph(matrix):
    with open("../connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    G = nx.DiGraph()
    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                G.add_edge(ri,ci)

    # nx.draw_shell(G, with_labels=True)
    # plt.show()

    return(G)

def scaleToInterval(x,domainMin,domainMax):     # given an interval and value in the interval it scales it to be between 0 and 2pi
    return(((x - domainMin)/(domainMax - domainMin))*cmath.pi)

###################### Actual Code part #######################################

sim = sys.argv[1]

X = pickle.load(open("storeddata/" + sim + "-X.p","rb"))
Y = pickle.load(open("storeddata/" + sim + "-Y.p","rb"))
Z = pickle.load(open("storeddata/" + sim + "-Z.p","rb"))

duration = len(X[0])
N = len(X)
singlerun = pickle.load(open("storeddata/singlerun.p","rb"))

simulation = plt.figure(figsize=(17,10))
title = sim + " | " + str(duration) + " | "
simulation.subplots_adjust(wspace=0.1,hspace=0.25)
simulation.add_subplot(3,1,1)
for i in range(0,N):
    plt.ylabel("x")
    plt.xlabel("t")
    plt.plot(X[i])

for i in range(1,duration/singlerun):
    plt.axvline(x=i*singlerun, color='k', linestyle='--')

simulation.add_subplot(3,1,2)
for i in range(0,N):
    plt.ylabel('z')
    plt.xlabel("t")
    plt.plot(Z[i])

for i in range(1,duration/singlerun):
    plt.axvline(x=i*singlerun, color='k', linestyle='--')


sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K')                 # gets rid of some error that ruins my A E S T H E T I C
print("--- measuring synchrony ---")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sections = []
for i in range(0,duration/singlerun):
    sections.append([])

for i in range(len(sections)):
    for j in range(N):
        sections[i].append(Z[j][singlerun*i:singlerun*(i+1)])

mins = []
maxs = []

for section in range(len(sections)):
    simMinlist = []
    simMaxlist = []

    for i in range(N):
        simMinlist.append(np.min(sections[section][i]))
        simMaxlist.append(np.max(sections[section][i]))

    mins.append(np.min(simMinlist))
    maxs.append(np.max(simMaxlist))
    # print(simMin,simMax)                            # I think we should sample from like halfway through the simulation to the end because having the network synchronize screws up the min and max
    # print(scaleToInterval(0,simMin,simMax))

runningsync = []
phivals = []
for section in range(len(sections)):
    scaledM = []

    for i in range(0,N):
        scaledM.append([])
        for j in range(0, singlerun/10):
            # scaledM[i].append(scaleToInterval(Z[i][10*j], simMin, simMax))
            scaledM[i].append(scaleToInterval(sections[section][i][10*j], mins[section], maxs[section]))


    phasic = []
    for i in range(0,len(scaledM[0])):
        phasic.append(0)
        for j in range(0,N):
             phasic[i] += cmath.exp(complex(scaledM[j][i],0)*complex(0,1))

        phasic[i] = abs(phasic[i])/N

    runningsync = np.append(runningsync,phasic)
    # h = phasic
    dhdt = []
    for i in range(1,len(phasic)):
        dhdt.append(abs(phasic[i] - phasic[i-1]) * 1000)

    averagesync = sum(dhdt)/len(dhdt)
    phivals.append(averagesync)


print(phivals)
for i in range(len(phivals)):
    title += " : " + str('%.4f'%(phivals[i]))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
simulation.add_subplot(3,1,3)
simulation.suptitle(title)

# for i in range(1,duration/singlerun):
#     plt.axvline(x=i*singlerun, color='k', linestyle='--')

plt.plot(runningsync)
plt.ylim(ymin = 0, ymax = 1.1)
plt.ylabel("synchronization")
plt.xlabel("timestep")


# G = make_NX_graph(matrix)

# qwe = array(nx.to_numpy_matrix(G))
# adj_matrix = np.zeros((N,N), dtype=int)
# for i in range(0,N):
#     for j in range(0,N):
#         adj_matrix[i][j] = int(qwe[i][j])
#
# print(adj_matrix)

plt.show(block=False)

savesim = raw_input("save simulation? ")
if(savesim == 'y'):
    simname = raw_input("Simulation name: ")
    if(simname == ''):
        simname = sim
    plt.savefig('../simulation_files/XZsync/' + simname + '.png')

# wut...

# showgraph = plt.figure()
# # nx.draw_kamada_kawai(G, with_labels=True, font_weight='bold')
# nx.draw_shell(G, with_labels=True, font_weight='bold')
# plt.show(block=False)
#
# savesim = raw_input("save graph? ")
# if(savesim == 'y'):
#     simname = raw_input("network name: ")
#     if(simname == ''):
#         simname = sim
#     plt.savefig('../networks/' + simname + '.png')
