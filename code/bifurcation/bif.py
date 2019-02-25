from PyDSTool import *
from datetime import datetime


def create_diagram(HR, cycle=None, EQ=True, LC=True, initpoint='H1'):
    PCargs = args(name='EQ1', type='EP-C')
    PCargs.freepars = ['g']
    PCargs.StepSize = 2e-3
    PCargs.MaxNumPoints = 450
    PCargs.MaxStepSize = 1e-1
    PCargs.LocBifPoints = 'all'
    PCargs.StopAtPoints = 'B'
    PCargs.SaveEigen = True
    PCargs.verbosity = 2
    HR.newCurve(PCargs)

    if EQ:
        print('Computing curve...')
        start = clock()
        HR['EQ1'].forward()
        HR['EQ1'].backward()
        print('done in %.3f seconds!' % (clock()-start))

    PCargs.name = 'LC1'
    PCargs.type = 'LC-C'
    PCargs.freepars = ['g']
    if cycle is not None:
        PCargs.initcycle = cycle
    else:
        PCargs.initpoint = 'EQ1:' + initpoint
    PCargs.MinStepSize = 1e-4
    PCargs.MaxStepSize = 1e-1
    PCargs.StepSize = 1e-2
    PCargs.MaxNumPoints = 100
    PCargs.LocBifPoints = []
    PCargs.NumIntervals = 350
    PCargs.NumCollocation = 4
    PCargs.NumSPOut = 20;
    PCargs.SolutionMeasures = 'all'
    PCargs.SaveEigen = True
    PCargs.SaveFlow = True
    PCargs.SaveJacobian = True
    HR.newCurve(PCargs)

    if LC:
        print('Computing LC-C from H1...')
        start = clock()
        HR['LC1'].forward()
        print('done in %.3f seconds!' % (clock()-start))

def create_HR_cycle(HR, t1=3000):
    DS = HR.gensys
    DS.set(tdata=[0, t1])
    return DS.compute('BurstI2')

################################################################################

x1 = -0.5*(1+sqrt(5))
x = x1
y = 1-5*x*x

pars = {'a': 1, 'b': 3.3, 'I': 2, 'g': 0, 'Vo': 2, 'lam': 10, 'thet': -0.6, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'x1': x1}


icdict = {'x': x, 'y': y, 'z': pars['I']}

auxfndict = {'gam': (['x'], '1/(1+((2.71828)**(-1*lam*(x-thet))))')}

xstr = 'y - a*x*x*x + b*x*x + I - z - g*(x-Vo)*gam(x)'
ystr = 'c - d*x*x - y'
zstr = 'r*(s*(x-x1)-z)'


DSargs = args(name='HindmarshRose')
"""DSargs.fnspecs = {'Jacobian': (['t', 'x', 'y', 'z'],
                        [[-3*x*x + 6*x, 1.0, -1.0],
                            [-10*x, -1.0, 0.0],
                            [r*s, 0.0, -1*r]])}"""

DSargs.pars = pars
DSargs.varspecs = {'x': xstr, 'y': ystr, 'z': zstr}
DSargs.fnspecs = auxfndict
DSargs.ics = icdict

testODE = Vode_ODEsystem(DSargs)
P = ContClass(testODE)

PCargs = args(name='test', type='EP-C')
PCargs.freepars = ['g']
PCargs.StepSize = 1e-3
PCargs.MaxNumPoints = 800
PCargs.MaxStepSize = 1e-2

P.newCurve(PCargs)
P['test'].forward()

sol = P['test'].sol

print "There were %i points computed" % len(sol)
# solution points:
print sol




HR_system = P
HR_pars = pars
t_end = 1000
HRtraj = create_HR_cycle(HR_system, t1=t_end)
plotData = HRtraj.sample()

simulation = plt.figure(figsize=(10,6))
simulation.subplots_adjust(wspace=0.3, hspace=0.25)

simulation.add_subplot(1,1,1)

HR_system['EQ1'].display(coords=('z', 'x'), stability=True)
HR_system['LC1'].display(coords=('z','x_max'), stability=True)
HR_system['LC1'].display(coords=('z','x_min'), stability=True)

show()


#
# HRtraj = create_HR_cycle(P)
# plotData = HRtraj.sample()
# cycle = plotData[4067:5421]
# cycle[-1] = cycle[0]
# t0 = 1310
# T0 = 452.84
# # T = findApproxPeriod(HRtraj, t0, t0+T0, v='z', rtol=0.015)
# T = findApproxPeriod(HRtraj, t0, t0+T0, rtol=0.015)
# cycle = HRtraj.sample(dt=.01, tlo=t0, thi=t0+T)
# create_diagram(P, cycle=cycle, EQ=False, LC=False)
# show()
