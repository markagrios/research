# http://brian2.readthedocs.io/en/stable/resources/tutorials/2-intro-to-brian-synapses.html
# http://brian2.readthedocs.io/en/2.0.1/user/synapses.html

from brian2 import *
import math

start_scope()

N = 1                   # number of neurons in network
duration = 1000*ms      # how long simulations runs

init_x = -0.5*(1+sqrt(5))
init_y = (1-5*init_x*init_x)
init_z = 2

neuron_pars = {'tau': 1*ms, 'a': 1, 'b': 3.3, 'I': 2, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'xR': -0.5*(1+sqrt(5))}
coupling_pars = {'tau': 1*ms, 'g': 0, 'Vo': 2, 'lam': 10, 'thet': -0.6}

coupling_pars['g'] = 0         # just so I can play with it.

HR_neuron = '''
    dx/dt = (y - a*x*x*x + b*x*x + I - z + couple)/tau : 1
    couple : 1
    dy/dt = (c - d*x*x - y)/tau : 1
    dz/dt = (r*(s*(x-xR)-z))/tau : 1
'''
coupling_model = '''
    # couple_pre = ((-1)*g*(x_pre - Vo)*(1/(1+exp((-1*lam*(x_post - thet)))))) : 1 (summed)
    # couple_pre = ((-1)*g*(x_post - Vo)*(1/(1+exp((-1*lam*(x_pre - thet)))))) : 1 (summed)
    # couple_post = ((-1)*g*(x_pre - Vo)*(1/(1+exp((-1*lam*(x_post - thet)))))) : 1 (summed)
    couple_post = ((-1)*g*(x_post - Vo)*(1/(1+exp((-1*lam*(x_pre - thet)))))) : 1 (summed)    # this seems to synchonize them.. I also think it's the most correct.
'''

G = NeuronGroup(N, model=HR_neuron, method='rk4', namespace=neuron_pars)
S = Synapses(G, G, model=coupling_model, namespace=coupling_pars)

# S.connect(i=1,j=0)
S.connect()
# S.connect(i=np.array([0, 1]), j=np.array([1, 0])) # connect 0->1 and 1->0
# here would be a cool place to input a connectivity matrix and it would generate these expressions.

M = StateMonitor(G, ['x','y','z'], record=True)
# spikemon = SpikeMonitor(G)

G.x = init_x
G.y = init_y
G.z = init_z
G.z[0] = 2.15

run(duration)

# print(spikemon.t[:])

simulation = plt.figure(figsize=(10,6))
simulation.subplots_adjust(wspace=0.3, hspace=0.25)

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
    plt.ylabel('z')
    plt.xlabel('t')
    plot(M.z[0], M.x[i])

show()
# show(block=False)


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
    show()

# visualise_connectivity(S)
