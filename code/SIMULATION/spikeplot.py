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
import pyspike as spk

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

def normalizetan(x):
    return(np.tan(x - 0.5) * math.pi)

###################### Actual Code part #######################################

sim = sys.argv[1]
ablation_list = pickle.load(open("storeddata/ablationlist.p","rb"))

print(ablation_list)

X = pickle.load(open("storeddata/" + sim + "-X.p","rb"))
# Y = pickle.load(open("storeddata/" + sim + "-Y.p","rb"))
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

homo = pickle.load(open("storeddata/homo.p","rb"))
# print(duration/singlerun)
for i in range(2,duration/singlerun):
    if(homo[i-2] == False):
        plt.axvline(x=(i)*singlerun, color='k', linestyle='--')
    elif(homo[i-2] == True):
        plt.axvline(x=(i)*singlerun, color='r', linestyle='--')
    else:
        plt.axvline(x=(i)*singlerun, color='b', linestyle='--')

# simulation.add_subplot(3,1,2)
# for i in range(0,N):
#     plt.ylabel('z')
#     plt.xlabel("t")
#     plt.plot(Z[i])
#
# for i in range(2,duration/singlerun):
#     if(homo[i-2] == False):
#         plt.axvline(x=(i)*singlerun, color='k', linestyle='--')
#     elif(homo[i-2] == True):
#         plt.axvline(x=(i)*singlerun, color='r', linestyle='--')
#     else:
#         plt.axvline(x=(i)*singlerun, color='b', linestyle='--')
#


sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K')                 # gets rid of some error that ruins my A E S T H E T I C
print("--- measuring synchrony ---")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~

spiketrain = []
for i in range(N):
    spiketrain.append([-2])
    for t in range(1,duration):
        if(float(X[i][t]) > 0 and float(X[i][t-1]) < 0):
            if((i in ablation_list) and (t > singlerun*(ablation_list.index(i)+2))):               # if it's after the ablation event
                spiketrain[i].append(-2)
            else:
                spiketrain[i].append(i)

        else:
            spiketrain[i].append(-2)


spiketimes = []
for n in range(len(spiketrain)):
    spiketimes.append([0])
    for t in range(len(spiketrain[n])):
        if (spiketrain[n][t] >= 0):
            spiketimes[n].append(t)

# for i in range(len(spiketimes)):
#     print(spiketimes[i])

# ST = []
# for i in range(len(spiketimes)):
#     ST.append(spk.SpikeTrain(spiketimes[i],duration))
#
# # avrg_isi_profile = spk.isi_profile(ST)
# # avrg_spike_profile = spk.spike_profile(ST)
# # avrg_spike_sync_profile = spk.spike_sync_profile(ST)
#
# isi_distance = spk.isi_distance_matrix(ST)
# print(isi_distance)
# # plt.imshow(isi_distance, interpolation='none')
# # plt.title("ISI-distance")
# # plt.show()

print("--- analyzing spike train ---")

distList = []
matrixList = []
for c in range(duration/singlerun):
    ST = []
    for i in range(len(spiketimes)):
        ST.append(spk.SpikeTrain(spiketimes[i],(c*singlerun, (c+1)*singlerun)))
        # spike_sync = spk.isi_distance_matrix(ST)
        spike_sync = spk.spike_distance_matrix(ST)


    matrixList.append(spike_sync)
    averageDist = np.average(spike_sync)
    distList.append(averageDist)

print(distList)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("--- plotting ---")
print(" ")

simulation.add_subplot(3,1,2)
simulation.suptitle(title)
for i in range(N):
    plt.plot(range(duration),spiketrain[i], marker="o", markersize=3, linewidth=0)
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    print("plotting spikes of neuron " + str(i))
plt.ylim(ymin = -1, ymax = N+1)
plt.ylabel("neuron index, 0 to " + str(N))
plt.xlabel("t")

for i in range(2,duration/singlerun):
    plt.axvline(x=i*singlerun, color='k', linestyle='--')
    plt.plot(i*singlerun, ablation_list[i-2], marker="x", color="black")

simulation.add_subplot(3,1,3)
simulation.suptitle(title)
plt.plot(range(duration/singlerun),distList, marker="o", markersize=3, linewidth=0)
sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K')
plt.ylabel("average ISI distnace" )
plt.xlabel("t")


plt.show(block=False)

# matrixPlot = plt.figure()
# matrixTitle = sim + " | " + str(duration) + " | "
# # matrixPlot.subplots_adjust(wspace=0.1,hspace=0.25)
# for m in range(1,(duration/singlerun)):
#     matrixPlot.add_subplot(1,(duration/singlerun),m)
#     plt.imshow(matrixList[m], interpolation='none')
# plt.show(block=False)

savesim = raw_input("save simulation? ")
if(savesim == 'y'):
    simname = raw_input("Simulation name: ")
    if(simname == ''):
        simname = sim
    plt.savefig('../simulation_files/spiketrain/' + simname + "_" + str(ablation_list) + '.png')

plt.close()
#
# print(phivals)
# print(avgsync)
#
# phivals = phivals[2:]
# avgsync = avgsync[2:]
#
# np.savetxt("../simulation_files/ablation/R2plots/" + sim + "_syncvals" + ".csv", (phivals,avgsync), delimiter=",", fmt='%s')
#
# plt.scatter(phivals,avgsync)
# plt.ylim(ymin = 0, ymax = 1.1)
# # plt.xlim(xmin = 0, xmax = 1.1)
# plt.xlabel("total variation")
# plt.ylabel("average sync value")
#
# for i in range(len(phivals)):
#     plt.annotate(i, (phivals[i],avgsync[i]))
#
# plt.show(block=False)
#
# savesim = raw_input("save simulation? ")
# if(savesim == 'y'):
#     simname = raw_input("Simulation name: ")
#     if(simname == ''):
#         simname = sim
#         ablation_list = pickle.load(open("storeddata/ablation_list.p","rb"))
#     plt.savefig('../simulation_files/ablation/R2plots/' + simname + "_" + ablation_list + '.png')
