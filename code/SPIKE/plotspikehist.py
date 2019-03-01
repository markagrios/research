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
duration = len(train[0])

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
simulation.add_subplot(2,1,1)
th.plot_raster(st)


# histogram for spikes
simulation.add_subplot(2,1,2)
bin = 10000
spikeHist = th.psth(st, bin)
# spikeHist = th.psth(st, duration/1000)
plt.plot(spikeHist[0])
sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K')
plt.ylabel("PST histogram")
# plt.xlim(xmin= 0, xmax=duration/1000)
plt.xlim(xmin= 0)
plt.xticks([])

plt.show(block=False)

savesim = raw_input("save simulation? ")
if(savesim == 'y'):
    simname = raw_input("Simulation name: ")
    if(simname == ''):
        simname = matrix
    plt.savefig('../simulation_files/SPIKE/' + simname + "-spikehist" + '.png')

plt.close()
