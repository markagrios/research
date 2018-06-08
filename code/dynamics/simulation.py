from brian2 import *
import networkx as nx
import numpy as np
import math
import cmath
import csv
import time as TIME
import matplotlib.pyplot as plt
import sys

# example run:
# > python persistence.py 6weird x
# Looks at the state variable x

#******************** UTILITY FUNCTIONS ****************************************

# reads in a connectivity matrix and creates synapes in the brian object S
def connect_from_Matrix(matrix):
    with open("../connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                S.connect(i=ri,j=ci)

# plots the graph using networkx
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

# returns the number of nodes from a given connection matrix
def N_from_Matrix(matrix):
    with open("../connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    return(len(a))

# counts the number of connections in a connection matrix....wow
def count_connections(matrix):
    n = 0
    with open("../connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                n += 1

    return(n)

def scaleToInterval(x,domainMin,domainMax):     # given an interval and value in the interval it scales it to be between 0 and 2pi
    return(((x - domainMin)/(domainMax - domainMin))*cmath.pi)

#******************** |ACTUAL CODE PART| ***************************************


#******************** MAKING BRIAN NETWORK *************************************

start_scope()

matrix = sys.argv[1] + ".csv"

N = N_from_Matrix(matrix)                   # number of neurons in network
N_syn = count_connections(matrix)           # number of synapses
duration = 500*ms                          # how long simuldurations runs

tau_param = {'tau': 1*ms}

HR_neuron = '''
    a : 1
    b : 1
    I : 1
    c : 1
    d : 1
    r : 1
    s : 1
    xR : 1

    dx/dt = (y - a*x*x*x + b*x*x + I - z + couple)/tau : 1
    couple : 1
    dy/dt = (c - d*x*x - y)/tau : 1
    dz/dt = (r*(s*(x-xR)-z))/tau : 1
'''
coupling_model = '''
    Vo : 1
    lam : 1
    thet : 1
    g : 1

    couple_post = ((-1)*g*(x_post - Vo)*(1/(1+exp((-1*lam*(x_pre - thet)))))) : 1 (summed)
'''

G = NeuronGroup(N, model=HR_neuron, method='rk4', namespace=tau_param, dt=0.01*ms)
S = Synapses(G, G, model=coupling_model) # Synapses can also have a dt argument....?

connect_from_Matrix(matrix)

sv = sys.argv[2]

M = StateMonitor(G, sv, record=True)

ix = -0.5*(1+sqrt(5))
init_cond = {'x': ix, 'y': 1-5*ix*ix, 'z': 2}
neuron_pars = {'a': 1, 'b': 3.3, 'I': 2, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'xR': -0.5*(1+sqrt(5))}
coupling_pars = {'Vo': 2, 'lam': 10, 'thet': -0.6, 'g': 0.4}

# Puts all the initial conditions in place.
for ic,value in init_cond.items():
    setattr(G,ic,[value for _ in range(N)])

# These set the parameters to be homogeneous
for param,value in neuron_pars.items():
    setattr(G,param,[value for _ in range(N)])

for param,value in coupling_pars.items():
    setattr(S,param,[value for _ in range(N_syn)]) # N_syn is the number of non-zero entries of the connection matrix


#************ Set initial state variables of neurons ***************************

setattr(G,'z',[1.7+(_*0.1) for _ in range(N)])        # for slightly different init cond
# setattr(G,'z',[1.7 for _ in range(N)])                  # for uniform init cond

start_time = TIME.time()

run(duration)                # http://brian2.readthedocs.io/en/stable/reference/brian2.monitors.statemonitor.StateMonitor.html
# store()
# S.connect(i=0,j=3)
# restore()
# run(duration/2)


######################## PLOTTING ##############################################


simulation = plt.figure(figsize=(17,10))
simulation.subplots_adjust(wspace=0.1,hspace=0.25)
title = matrix
simulation.suptitle(title)
simulation.add_subplot(3,1,1)
for i in range(0,N):
    plt.ylabel(sv)
    plt.xlabel("t")
    plot(M.t/ms, getattr(M,sv)[i])

print("---")

# for i in range(N):
#     print(np.min(M[i].x),np.max(M[i].x))

simMin = np.min(M.x)
simMax = np.max(M.x)
# print(simMin,simMax)
# print(scaleToInterval(0,simMin,simMax))

scaledM = []

for i in range(0,N):
    scaledM.append([])
    for j in range(0, int(str(duration).split(".")[0]) * 100000):
        scaledM[i].append(scaleToInterval(M[i].x[j], simMin, simMax))


phasic = []
for i in range(0,len(scaledM[0])):
    phasic.append(0)
    for j in range(0,N):
         phasic[i] += cmath.exp(complex(scaledM[j][i],0)*complex(0,1))

    phasic[i] = abs(phasic[i])/N

simulation.add_subplot(3,1,2)
plt.plot(phasic)
plt.ylim(ymin = 0, ymax = 1.1)

simulation.add_subplot(3,2,6)
G = make_NX_graph(matrix)
nx.draw_shell(G, with_labels=True, font_weight='bold')

print("--- %s seconds ---" % (TIME.time() - start_time))

qwe = array(nx.to_numpy_matrix(G))
adj_matrix = np.zeros((N,N), dtype=int)
for i in range(0,N):
    for j in range(0,N):
        adj_matrix[i][j] = int(qwe[i][j])

print(adj_matrix)

plt.show(block=False)

savesim = raw_input("save simulation? ")
if(savesim == 'y'):
    simname = raw_input("Simulation name: ")
    if(simname == ''):
        simname = title
    plt.savefig('../simulation_files/' + simname + '.png')

# wut...
