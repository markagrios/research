from brian2 import *
import networkx as nx
import numpy as np
import math
import cmath
import csv
import time as TIME
import matplotlib.pyplot as plt
import sys


sim = sys.argv[1]

with open("storeddata/" + sim + "-X.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    a = list(readCSV)


v = []
for i in range(len(a)):
    for j in range(len(a[0])):
        v.append(float(a[i][j]))
        a[i][j] = float(a[i][j])


# plt.plot(a[0])
# plt.xlabel('x')
# plt.ylabel('t')
# plt.show()
# print("done.")


simulation = plt.figure(figsize=(17,10))
title = matrix
simulation.subplots_adjust(wspace=0.1,hspace=0.25)
simulation.add_subplot(3,1,1)
for i in range(0,len(a)):
    plt.ylabel("x")
    plt.xlabel("t")
    plt.plot(a[i])

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
