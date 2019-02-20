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
import thorns as th
import pyspike as spk

matrix = sys.argv[1]
train = pickle.load(open("storeddata/" + matrix + "-train.p", "rb"))
N = len(train)
betas = pickle.load(open("storeddata/" + matrix + "-betas.p", "rb"))
homXS = pickle.load(open("storeddata/" + matrix + "-homXS.p", "rb"))
duration = len(train[0])
singlerun = duration/(len(homXS)+2)

print("--- plotting ---")

# create list of spike times from raster
spiketimes = []
for n in range(len(train)):
    spiketimes.append([0])
    for t in range(len(train[n])):
        if (train[n][t] >= 0):
            spiketimes[n].append(t)

st = th.make_trains(spiketimes)

simulation = plt.figure(figsize=(17,10))
simulation.add_subplot(4,1,1)
th.plot_raster(st)
for i in range(2,duration/singlerun):
    if(homXS[i-2][1] == 'X'):
        plt.axvline(x=(i)*singlerun, color='g', linestyle='--')
    elif(homXS[i-2][1] == 'S'):
        plt.axvline(x=(i)*singlerun, color='r', linestyle='--')
    else:
        plt.axvline(x=(i)*singlerun, color='b', linestyle='--')

    plt.plot(i*singlerun, int(homXS[i-2][0]), marker="x", color="black")
plt.xlabel('')



# histogram for spikes
simulation.add_subplot(4,1,2)
spikeHist = th.psth(st, duration/1000)
plt.plot(spikeHist[0])
sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K')
plt.ylabel("PST histogram")
plt.xlim(xmin= 0,xmax=1000)
plt.xticks([])

# betti number plot
difbetas = []
for i in range(len(betas)):
    difbetas.append([])
    for c in range(len(betas[i])-1):
        difbetas[i].append(betas[i][c+1]-betas[i][c])

homdec = []
for b in range(len(difbetas)):
    homdec.append([])
    for i in range(len(difbetas[b])+1):
        homdec[b].append(sum(difbetas[b][:i]))

print(homdec[0])
print(homdec[1])
print(homdec[2])

simulation.add_subplot(4,1,3)
plt.ylabel("Change in Betti numbers")
plt.plot(homdec[0], linestyle="--", marker="o", label="beta 0")
plt.plot(homdec[1], linestyle="--", marker="o", label="beta 1")
plt.plot(homdec[2], linestyle="--", marker="o", label="beta 2")
plt.legend(loc='upper right')
plt.xlim(xmin=-1.5,xmax=len(homdec[0])-0.5)


# synchrony
simulation.add_subplot(4,1,4)
plt.ylabel("synchronization")

chunk = duration/singlerun
# print(chunk)
slices = []
for c in range(1,chunk+1):
    # print(c)
    section = []
    for n in range(len(spiketimes)):
        section.append([])
        subint = [x for x in spiketimes[n] if x >= ((c-1)*singlerun) and x <= (c*singlerun)]
        section[n] = spk.SpikeTrain(subint, (0,singlerun))

    slices.append(section)

sync = []
for c in range(len(slices)):
    # sync.append(np.var(spk.spike_sync_matrix(slices[c])))
    sync.append(np.linalg.norm(spk.spike_sync_matrix(slices[c])))

plt.plot(sync, linestyle="-", marker="o", markersize="7")
# plt.hlines(15, 0, len(homXS), linewidth=0.3)
plt.grid(which='both', axis='y')
plt.xlim(xmin=-0.5,xmax=len(homXS)+1.5)
for i in range(len(sync)):
    plt.text(i, sync[i]-0.3, str(round(sync[i],2)))





plt.show(block=False)

savesim = raw_input("save simulation? ")
if(savesim == 'y'):
    simname = raw_input("Simulation name: ")
    if(simname == ''):
        simname = matrix + str(homXS)
    plt.savefig('../simulation_files/SPIKE/' + simname + '.png')

plt.close()
