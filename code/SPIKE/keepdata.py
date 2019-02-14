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

print("--- storing data ---")

# create list of spike times from raster
spiketimes = []
for n in range(len(train)):
    spiketimes.append([0])
    for t in range(len(train[n])):
        if (train[n][t] >= 0):
            spiketimes[n].append(t)

st = th.make_trains(spiketimes)

difbetas = []
for i in range(len(betas)):
    difbetas.append([])
    for c in range(len(betas[i])-1):
        difbetas[i].append(betas[i][c+1]-betas[i][c])


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
    sync.append(np.linalg.norm(spk.spike_sync_matrix(slices[c])))

plt.plot(sync, linestyle="-", marker="o", markersize="7")
# plt.hlines(15, 0, len(homXS), linewidth=0.3)
plt.grid(which='both', axis='y')
plt.xlim(xmin=-0.5,xmax=len(homXS)+1.5)
for i in range(len(sync)):
    plt.text(i+0.3, sync[i]+0.3, str(round(sync[i],2)))





plt.show(block=False)

savesim = raw_input("save simulation? ")
if(savesim == 'y'):
    simname = raw_input("Simulation name: ")
    if(simname == ''):
        simname = matrix + str(homXS)
    plt.savefig('../simulation_files/SPIKE/' + simname + '.png')

plt.close()
