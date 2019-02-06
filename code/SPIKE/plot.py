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

simulation.add_subplot(2,1,2)
spikeHist = th.psth(st, duration/1000)
# spikeHist = th.psth(st, singlerun)
plt.plot(spikeHist[0])
sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K')
plt.ylabel("PST histogram")
# plt.ylim(ymax= 0.07)
plt.xlabel("t")



plt.show()
