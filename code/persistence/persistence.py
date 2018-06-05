from brian2 import *
import networkx as nx
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/osboxes/gudhi/build/cython/')
import gudhi

# example run:
# > python persistence.py 6weird x 310 s
# Looks at the state variable x at time 310 under the dynamics of the newtork
# labeled 6weird.csv using the symmetric graph not the directed graph


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

    # nx.draw(G)
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

# Given a list of values that are the state variables of the neurons of a clique, this
# returns the Filtration value that is to be assigned to that simplex
def filtmetric(statevariablelist):
    sumdist = 0
    countdist = 0
    for i in range(len(statevariablelist)):
        for j in range(len(statevariablelist)):
            if(i < j):
                sumdist += abs(statevariablelist[i] - statevariablelist[j])
                countdist += 1

    # meandist = sumdist/countdist                # I kinda wish this worked but it doesn't for some reason...
    meandist = sumdist/len(statevariablelist)     # this actually works with the set simplex to lower filt value than faces porblem. Not sure why, but it does
    metric = max(statevariablelist) + meandist

    # print("countdist of " + str(len(statevariablelist)) + ": ",(countdist))
    return(metric)

# Reads in a list of simplices (created by neurotop) and adds them to the Gudhi
# object and returns the simplicial complex
def listofsimps_to_SC(sl,svar,time):
    simpcomp = gudhi.SimplexTree()
    time = time*100
    with open("../connection_matrices/simp_lists/"+sl, 'rU') as p:
        #reads csv into a list of lists
        simp_list = [list(map(int,rec)) for rec in csv.reader(p, delimiter=' ')]

    print("Simplicial Complex of " + sl + ":")
    print(simp_list)

    simpcomp.set_dimension(len(simp_list[-1]))

    dim0list = []
    dimnlist = []
    filtlist = []
    for simp in simp_list:
        if(len(simp) == 1):
            dim0list.append(simp)
        else:
            dimnlist.append(simp)

    for simp in dim0list:
        filtval = getattr(M,svar)[simp[0]-1][time]
        filtlist.append((simp[0],filtval))
        simpcomp.insert(simp, filtval)

    #--------------- what I think should be right.... -------------------------

    for simp in dimnlist:
        listofvals = []
        for i in range(len(simp)):
            listofvals.append(getattr(M,sv)[simp[i]-1][time])       # gets the state variable value for each neuron included in the clique
        filtval = filtmetric(listofvals)      # yayyyy Sarah
        simpcomp.insert(simp, filtval)

    # if Q is an n simplex and is the face P, an m>n simplex, then setting the
    # filtation of P less than Q will set Q to the new value

    return(simpcomp)

#******************** |ACTUAL CODE PART| ***************************************


#******************** MAKING BRIAN NETWORK *************************************

start_scope()

matrix = sys.argv[1] + ".csv"

N = N_from_Matrix(matrix)                   # number of neurons in network
N_syn = count_connections(matrix)           # number of synapses
duration = 1000*ms                          # how long simulations runs


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

# setattr(G,'z',[1.7+(_*0.1) for _ in range(N)])
for i in range(0,N):
    setattr(G,'z',1.7)

run(duration)

#******************** GUDHI PERSISTENCE ****************************************
    # Given a time 't' and our chosen state variable 'sv', change the threshold from
    # 0 to the max value of sv and create a persistence diagram of our newtork.

    # http://gudhi.gforge.inria.fr/python/latest/simplex_tree_ref.html
    # http://gudhi.gforge.inria.fr/python/latest/persistence_graphical_tools_ref.html
    # http://gudhi.gforge.inria.fr/python/latest/rips_complex_user.html

    # neurotop: the program used to create list of simplices from a (un)directed graphs: http://neurotop.gforge.inria.fr/


try:
    time = int(sys.argv[3])
except:
    time = 400

if(sys.argv[4] == 's'):
    simplex_list = sys.argv[1] + "_slist.csv"       # using the clique topology
if(sys.argv[4] == 'd'):
    simplex_list = sys.argv[1] + "_dlist.csv"     # using the directed clique topology

simplex_tree = listofsimps_to_SC(simplex_list,sv,time)

simplex_tree.initialize_filtration()

print("dimension of simplicial complex: " + str(simplex_tree.dimension()))
print("---")

print("Filtration:")
for i in range(len(simplex_tree.get_filtration())):
    print(simplex_tree.get_filtration()[i])

p = simplex_tree.persistence()

print("---")
perscolors = ["red","green","blue","cyan","magenta","yellow","black","maroon","chartreuse?","azure","a very unappealing yellowish green","purple","blue-grey"]
for dim in range(len(simplex_tree.get_filtration()[-1])+3):
    print("Persistence of dim " + str(dim) + " (" + perscolors[dim] + ")" + ": ")
    for i in simplex_tree.persistence_intervals_in_dimension(dim):
        print("   " + str(i))

print("---")
print("Betti numbers: ")
print("   " + str(simplex_tree.betti_numbers()))

######################## PLOTTING ##############################################

simulation = plt.figure(figsize=(12,7))
simulation.subplots_adjust(wspace=0.2, hspace=0.25)

title = matrix.split(".")[0] + ":" + "N=" + str(N) + "," + "g=" + str(coupling_pars['g']) + " | " + sv + "," + str(time) + "," + str(sys.argv[4])

simulation.suptitle(title)

simulation.add_subplot(2,1,1)
for i in range(0,N):
    plt.ylabel(sv)
    plt.xlabel('t')

    plt.axvline(x=time, color='k', linestyle='--')
    plot(M.t/ms, getattr(M,sv)[i])


simulation.add_subplot(2,2,4)
gudhi.plot_persistence_diagram(p)

simulation.add_subplot(2,2,3)
nx.draw_shell(make_NX_graph(matrix),with_labels=True, font_weight='bold')

# show(block=False)
plt.show()

print("---")

for i in range(N):
    print(np.min(M[i].x),np.max(M[i].x))

print("~")
print(np.min(M.x),np.max(M.x))

# ---- This doesn't work because fuck ----

# savesim = raw_input("save simulation? ")
# if(savesim == 'y'):
#     simname = raw_input("Simulation name: ")
#     if(simname == ''):
#         simname = title
#     plt.savefig('simulation_files/' + simname + '.png')

# wut...
