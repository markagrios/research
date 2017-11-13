# http://brian2.readthedocs.io/en/stable/resources/tutorials/2-intro-to-brian-synapses.html
# http://brian2.readthedocs.io/en/2.0.1/user/synapses.html
# http://brian2.readthedocs.io/en/2.0a/user/synapses.html
# http://brian2.readthedocs.io/en/2.0rc/reference/brian2.synapses.synapses.Synapses.html

from brian2 import *
import math
import csv
import sys

#******************** UTILITY FUNCTIONS ****************************************

def connect_from_Matrix(matrix):
    with open("connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                S.connect(i=ri,j=ci)

def N_from_Matrix(matrix):
    with open("connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    return(len(a))

def count_connections(matrix):
    n = 0
    with open("connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                n += 1

    return(n)


def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')
    show(block=False)

#******************** ACTUAL CODE PART *****************************************

start_scope()

# matrix = raw_input("Please enter an adjacency matrix: \n>>")
# if matrix == "":
#     matrix = "di-fourpath.csv"
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

M = StateMonitor(G, ['x','y','z'], record=True)     # we might not need all of these, just x probably, it might run faster...?
# M = StateMonitor(G, ['x'], record=True)

ix = -0.5*(1+sqrt(5))
init_cond = {'x': ix, 'y': 1-5*ix*ix, 'z': 2}
neuron_pars = {'a': 1, 'b': 3.3, 'I': 2, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'xR': -0.5*(1+sqrt(5))}
coupling_pars = {'Vo': 2, 'lam': 10, 'thet': -0.6, 'g': 0.2}

# Puts all the initial conditions in place.
for ic,value in init_cond.items():
    setattr(G,ic,[value for _ in range(N)])

# These set the parameters to be homogeneous
for param,value in neuron_pars.items():
    setattr(G,param,[value for _ in range(N)])

for param,value in coupling_pars.items():
    setattr(S,param,[value for _ in range(N_syn)]) # N_syn is the number of non-zero entries of the connection matrix

# If you want the initial z value to be different
# setattr(G,'z',[2+rand()*0.5-0.25 for _ in range(N)])

# G.a = [1,1]
# S.g = [1,1,1]

run(duration)

simulation = plt.figure(figsize=(10,6))
simulation.subplots_adjust(wspace=0.3, hspace=0.25)

title = matrix.split(".")[0] + ":" + "N=" + str(N) + "," + "g=" + str(coupling_pars['g'])

simulation.suptitle(title)

for i in range(0,N):
    simulation.add_subplot(2,2,1)
    plt.ylabel('x')
    plt.xlabel('t')
    plot(M.t/ms, M.x[i])

    simulation.add_subplot(2,2,2)
    plt.ylabel('y')
    plt.xlabel('t')
    plot(M.t/ms, M.y[i])

    simulation.add_subplot(2,2,3)
    plt.ylabel('z')
    plt.xlabel('t')
    plot(M.t/ms, M.z[i])

    simulation.add_subplot(2,2,4)
    plt.ylabel('x')
    plt.xlabel('z')
    plot(M.z[i], M.x[i])

show(block=False)

savesim = raw_input("save simulation? ")
if(savesim == 'y'):
    simname = raw_input("Simulation name: ")
    if(simname == ''):
        simname = title
    plt.savefig('simulation_files/' + simname + '.png')
