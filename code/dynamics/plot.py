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

sim = sys.argv[1]

# with open("storeddata/" + sim + "-X.csv") as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     a = list(readCSV)

X = pickle.load(open("storeddata/" + sim + "-X.p","rb"))
Y = pickle.load(open("storeddata/" + sim + "-Y.p","rb"))
Z = pickle.load(open("storeddata/" + sim + "-Z.p","rb"))

for i in range(len(X)):
    plt.plot(X[i])

plt.show()


# simulation = plt.figure(figsize=(17,10))
# title = matrix
# simulation.subplots_adjust(wspace=0.1,hspace=0.25)
# simulation.add_subplot(3,1,1)
# for i in range(0,len(X)):
#     plt.ylabel("x")
#     plt.xlabel("t")
#     plt.plot(X)

# simulation.add_subplot(3,1,2)
# for i in range(0,N):
#     plt.ylabel('z')
#     plt.xlabel("t")
#     plt.ylim(1.8,3.1)
#     plot(M.t/ms, getattr(M,'z')[i])


sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K')                 # gets rid of some error that ruins my A E S T H E T I C

plt.show()
print("done.")
