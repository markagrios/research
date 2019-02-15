from brian2 import *
import networkx as nx
import numpy as np
import math
import cmath
import csv
import ast
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
for c in range(1,len(slices)):
    sync.append(round(float(np.linalg.norm(spk.spike_sync_matrix(slices[c]))),3))

difsync = []
for i in range(1,len(sync)):
    difsync.append(round(sync[i] - sync[i-1],3))

bettichange = []
for i in range(len(difbetas[0])):
    bettichange.append([difbetas[i][0],difbetas[i][1],difbetas[i][2]])


block = []
for i in range(len(difsync)):
    block.append([matrix,bettichange[i],difsync[i]])

# print(block)
# ast.literal_eval("[0,-2,-1]") = [0,-2,-1]

with open('output_data/data.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerows(block)
