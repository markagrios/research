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

train = pickle.load(open("storeddata/train.p", "rb"))
N = len(train)

# create list of spike times from raster
spiketimes = []
for n in range(len(train)):
    spiketimes.append([0])
    for t in range(len(train[n])):
        if (train[n][t] >= 0):
            spiketimes[n].append(t)

st = th.make_trains(spiketimes)
th.plot_raster(st)
th.show()

# simulation = plt.figure()
# simulation.add_subplot(3,1,2)
# simulation.suptitle(title)
# for i in range(len(train)):
#     plt.plot(range(len(train[0])),train[i], marker="o", markersize=3, linewidth=0)
#     sys.stdout.write('\x1b[1A')
#     sys.stdout.write('\x1b[2K')
#     print("plotting spikes of neuron " + str(i))
# plt.ylim(ymin = -1, ymax = N+1)
# plt.ylabel("neuron index, 0 to " + str(N))
# plt.xlabel("t")
#
# plt.show()
