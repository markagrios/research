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

matrix = sys.argv[1]
train = pickle.load(open("storeddata/" + matrix + "-train.p", "rb"))
singlerun = pickle.load(open("storeddata/" + matrix + "-singlerun.p","rb"))
duration = len(train[0])
N = len(train)
betas = pickle.load(open("storeddata/betas.p", "rb"))
homXS = pickle.load(open("storeddata/homXS.p", "rb"))


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
simulation.add_subplot(3,1,1)
th.plot_raster(st)

# histogram for spikes
simulation.add_subplot(3,1,2)
spikeHist = th.psth(st, duration/1000)
plt.plot(spikeHist[0])
sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K')
plt.ylabel("PST histogram")
# plt.ylim(ymax= 0.07)
plt.xlabel("t")

# betti number plot
simulation.add_subplot(3,1,3)
plt.plot(betas[0], linestyle="--", marker="o", label="beta 0")
plt.plot(betas[1], linestyle="--", marker="o", label="beta 1")
plt.plot(betas[2], linestyle="--", marker="o", label="beta 2")
plt.legend(loc='upper right')


plt.show(block=False)

savesim = raw_input("save simulation? ")
if(savesim == 'y'):
    simname = raw_input("Simulation name: ")
    if(simname == ''):
        simname = matrix + str(homXS)
    plt.savefig('../simulation_files/SPIKE/' + simname + '.png')

plt.close()
