from PyDSTool import *


def create_cycle(system, t1=3000):
    DS = system.gensys
    DS.set(tdata=[0, t1])
    return DS.compute('BurstI2')


x1 = -0.5*(1+sqrt(5))
x = x1
y = 1-5*x*x

# pars = {'a': 1, 'b': 3, 'I': 5, 'g': 0, 'Vo': 2, 'lam': 10, 'thet': -0.6, 'c': -3, 'd': 5, 'r': 0.002, 's': 4, 'x1': -1.3}      # these params burst with g=0
pars = {'a': 1, 'b': 3, 'I': 2, 'g': 0, 'Vo': 2, 'lam': 10, 'thet': -0.6, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'x1': -1.6}

icdict = {'x': x, 'y': y, 'z': pars['I']}

auxfndict = {'gam': (['x'], '1/(1+((2.71828)**(-1*lam*(x-thet))))')}

xstr = 'y - a*x*x*x + b*x*x + I - z - g*(x-Vo)*gam(x)'
ystr = 'c - d*x*x - y'
zstr = 'r*(s*(x-x1)-z)'

DSargs = args(name='HindmarshRose')
DSargs.pars = pars
DSargs.varspecs = {'x': xstr, 'y': ystr, 'z': zstr}
DSargs.fnspecs = auxfndict
DSargs.ics = icdict

testDS = Generator.Dopri_ODEsystem(DSargs)
PyCont = ContClass(testDS)

PCargs = args(name='LC1', type='EP-C')   # as many arguments can be supplied here as desired
PCargs.freepars = ['g']                  # rest of the arguments created like a struct
PCargs.StepSize = 1e-3
PCargs.MaxNumPoints = 175
PCargs.MaxStepSize = 1e-2
PCargs.LocBifPoints = 'all'

PyCont.newCurve(PCargs)

PyCont['LC1'].forward()

t_end = 1200
traj = create_cycle(PyCont, t1=t_end)
plotData = traj.sample()

simulation = plt.figure(figsize=(10,6))
simulation.subplots_adjust(wspace=0.3, hspace=0.25)

simulation.add_subplot(2,2,1)
plt.xlabel('t')
plt.ylabel('x')
plot(plotData['t'], plotData['x'])
plt.xlim([0, t_end])

simulation.add_subplot(2,2,2)
plt.xlabel('t')
plt.ylabel('y')
plot(plotData['t'], plotData['y'])
plt.xlim([0, t_end])

simulation.add_subplot(2,2,3)
plt.xlabel('t')
plt.ylabel('z')
plot(plotData['t'], plotData['z'])
plt.xlim([0, t_end])

simulation.add_subplot(2,2,4)
# PyCont['LC1'].display(axes=(1,2,1))
PyCont['LC1'].display()
# PyCont['LC1'].display(('I','b'))
PyCont['LC1'].display(('g','thet'), axes=(1,2,2))
# PyCont.plot.info()
show()
