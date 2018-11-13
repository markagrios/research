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


#******************** UTILITY FUNCTIONS ****************************************

# reads in a connectivity matrix and creates synapes in the brian object S
def connect_from_Matrix(matrix):
    with open("../connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for group in ablate:
        for neuron in range(len(group)):
            for i in range(len(a[0])):
                a[i][group[neuron]] = "0"
                a[group[neuron]][i] = "0"
                # for j in range(len(a[0])):
                #     a[j][neuron] = "0"


    # for neuron in range(len(ablate)):
    #     for i in range(len(a[0])):
    #         a[i][neuron] = "0"
    #         for j in range(len(a[0])):
    #             a[j][neuron] = "0"

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


    for group in ablate:
        for neuron in range(len(group)):
            for i in range(len(a[0])):
                a[i][group[neuron]] = "0"
                a[group[neuron]][i] = "0"
                # for j in range(len(a[0])):
                #     a[j][neuron] = "0"

    # for neuron in range(len(ablate)):                                           ###### here it is
    #     for i in range(len(a[0])):
    #         a[i][neuron] = "0"
    #         for j in range(len(a[0])):
    #             a[j][neuron] = "0"

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                n += 1

    return(n)

def scaleToInterval(x,domainMin,domainMax):     # given an interval and value in the interval it scales it to be between 0 and 2pi
    return(((x - domainMin)/(domainMax - domainMin))*cmath.pi)

def list_to_csv(data):
    with open("storeddata/lasttoinit.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)



#******************** |ACTUAL CODE PART| ***************************************


#******************** MAKING BRIAN NETWORK *************************************

start_scope()

matrix = sys.argv[1] + ".csv"

# ablate = raw_input("synapse to ablate (ex: 0-2,3-4): ")
ablate = sys.argv[3]
if(ablate == "[]"):
    ablate = []
else:
    pickle.dump(ablate, open("storeddata/ablation_list.p","wb"))

    ablate = ablate.split("-")
    for i in range(len(ablate)):
        ablate[i] = ablate[i].split(",")

    for i in range(len(ablate)):
        for j in range(len(ablate[i])):
            ablate[i][j] = int(ablate[i][j])              # I'M STARTING TO FREAK ABOUT ABOUT INCREMENTS STARTING FROM 0 OR 1. The homology stuff starts at 1 but matrix stuff starts at 0


N = N_from_Matrix(matrix)                   # number of neurons in network
N_syn = count_connections(matrix)           # number of synapses
duration = 500*ms                          # how long simulations runs

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

M = StateMonitor(G, ['x', 'y', 'z'], record=True)

ix = -0.5*(1+sqrt(5))
init_cond = {'x': ix, 'y': 1-5*ix*ix, 'z': 1.7}
neuron_pars = {'a': 1, 'b': 3.3, 'I': 2, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'xR': -0.5*(1+sqrt(5))}
coupling_pars = {'Vo': 2, 'lam': 10, 'thet': -0.6, 'g': 0.1}        # I've been changing g a lot....

# These set the parameters to be homogeneous
for param,value in neuron_pars.items():
    setattr(G,param,[value for _ in range(N)])

for param,value in coupling_pars.items():
    setattr(S,param,[value for _ in range(N_syn)]) # N_syn is the number of non-zero entries of the connection matrix


#************ Set initial state variables of neurons ***************************

# Puts all the initial conditions in place.

sv_list = ['x', 'y', 'z']
sv_inits = []
perturb = np.random.normal(0,1, (3,N))
for i in range(len(init_cond.items())):
    sv_inits.append(float(init_cond.items()[i][1]))

if(sys.argv[2] != 'cont'):
    # print("State variable initial values (x,y,z):")
    # print(sv_inits)
    # print("Perturbation values:")
    # print(perturb)
    # print("---")
    # # for normal distribution init cond
    # for i in range(3):
    #     setattr(G,sv_list[i],[init_cond[sv_list[i]] + (perturb[i][_]) for _ in range(N)])

    # uncomment this for loop for the other two init cond regimes
    for ic,value in init_cond.items():
        setattr(G,ic,[value for _ in range(N)])

    setattr(G,'z',[1.7+(_*0.1) for _ in range(N)])            # for slightly different init cond
    # setattr(G,'z',[1.7 for _ in range(N)])                  # for uniform init cond
else:
    with open("storeddata/" + "lastvals.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        continits = list(readCSV)
        # print(continits)

    setattr(G,'x',[float(continits[0][_]) for _ in range(N)])
    setattr(G,'y',[float(continits[1][_]) for _ in range(N)])
    setattr(G,'z',[float(continits[2][_]) for _ in range(N)])


start_time = TIME.time()

print("--- running simulation ----")
run(duration)                # http://brian2.readthedocs.io/en/stable/reference/brian2.monitors.statemonitor.StateMonitor.html


num_timesteps = len(M.x[0])
pickle.dump(num_timesteps, open("storeddata/singlerun.p","wb"))

xlast = []
ylast = []
zlast = []
for i in range(N):
        xlast.append(M.x[i][-1])
        ylast.append(M.y[i][-1])
        zlast.append(M.z[i][-1])

lastvals = [xlast,ylast,zlast]

np.savetxt("storeddata/" + "lastvals.csv", lastvals, delimiter=",", fmt='%s')

names = ["storeddata/" + matrix[:-4] + "-X", "storeddata/" + matrix[:-4] + "-Y", "storeddata/" + matrix[:-4] + "-Z"]

if(sys.argv[2] != "cont"):
    for i in range(3):
        pickle.dump(getattr(M,sv_list[i]), open(names[i] + ".p", "wb"))


if(sys.argv[2] == 'cont'):
    for k in range(3):
        Q = pickle.load(open(names[k] + ".p","rb"))
        W = []
        for i in range(len(Q)):
            # W.append(np.append(Q[i],M.x[i]))
            W.append(np.append(Q[i], getattr(M,sv_list[k])[i] ))
        pickle.dump(W, open(names[k] + ".p", "wb"))

















######################## PLOTTING ##############################################


#
# simulation = plt.figure(figsize=(17,10))
# title = matrix[:-4] + " | " + str(duration) + " | "
# simulation.subplots_adjust(wspace=0.1,hspace=0.25)
# simulation.add_subplot(3,1,1)
# for i in range(0,N):
#     plt.ylabel("x")
#     plt.xlabel("t")
#     plot(M.t/ms, M.x[i])
#
# simulation.add_subplot(3,1,2)
# for i in range(0,N):
#     plt.ylabel('z')
#     plt.xlabel("t")
#     plt.ylim(1.8,3.1)
#     plot(M.t/ms, getattr(M,'z')[i])
#
#
# sys.stdout.write('\x1b[1A')
# sys.stdout.write('\x1b[2K')                 # gets rid of some error that ruins my A E S T H E T I C
# print("--- measuring synchrony ---")
#
# num_timesteps = int(str(duration).split(".")[0]) * 100000
# simMinlist = []
# simMaxlist = []
#
# for i in range(N):
#     simMinlist.append(np.min(M[i].z[(num_timesteps/2):]))
#     simMaxlist.append(np.max(M[i].z[(num_timesteps/2):]))
#
# simMin = np.min(simMinlist)
# simMax = np.max(simMaxlist)
# # print(simMin,simMax)                            # I think we should sample from like halfway through the simulation to the end because having the network synchronize screws up the min and max
# # print(scaleToInterval(0,simMin,simMax))
#
# scaledM = []
#
# for i in range(0,N):
#     scaledM.append([])
#     for j in range(0, num_timesteps/10):
#         scaledM[i].append(scaleToInterval(M[i].z[10*j], simMin, simMax))
#
#
# phasic = []
# for i in range(0,len(scaledM[0])):
#     phasic.append(0)
#     for j in range(0,N):
#          phasic[i] += cmath.exp(complex(scaledM[j][i],0)*complex(0,1))
#
#     phasic[i] = abs(phasic[i])/N
#
#
# h = phasic[len(phasic)/3:]
# dhdt = []
# for i in range(1,len(h)):
#     dhdt.append(abs(h[i] - h[i-1]) * 1000)
#
# averagesync = sum(dhdt)/len(dhdt)
# print("Synchronization value: " + str(averagesync))
# title += str('%.4f'%(averagesync))
#
# simulation.add_subplot(3,1,3)
# simulation.suptitle(title)
#
# plt.plot(phasic)
# plt.ylim(ymin = 0, ymax = 1.1)
# plt.ylabel("synchronization")
# plt.xlabel("timestep")
#
# print("   ")
# print("--- %s seconds ---" % (TIME.time() - start_time))
#
# G = make_NX_graph(matrix)
#
# # qwe = array(nx.to_numpy_matrix(G))
# # adj_matrix = np.zeros((N,N), dtype=int)
# # for i in range(0,N):
# #     for j in range(0,N):
# #         adj_matrix[i][j] = int(qwe[i][j])
# #
# # print(adj_matrix)
#
# plt.show(block=False)
#
# savesim = raw_input("save simulation? ")
# if(savesim == 'y'):
#     simname = raw_input("Simulation name: ")
#     if(simname == ''):
#         simname = matrix[:-4]
#     plt.savefig('../simulation_files/XZsync/' + simname + '.png')
#
# # wut...
#
# showgraph = plt.figure()
# # nx.draw_kamada_kawai(G, with_labels=True, font_weight='bold')
# nx.draw_shell(G, with_labels=True, font_weight='bold')
# plt.show(block=False)
#
# savesim = raw_input("save graph? ")
# if(savesim == 'y'):
#     simname = raw_input("network name: ")
#     if(simname == ''):
#         simname = matrix[:-4]
#     plt.savefig('../networks/' + simname + '.png')
