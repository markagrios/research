
""" EXAMPLE: Hindmarsh-Rose

    Drew LaMar, July 2006
"""

from PyDSTool import *
from datetime import datetime

def create_fast_subsystem():
    x1 = -0.5*(1+sqrt(5))
    x = x1
    y = 1-5*x*x

    print("1: Enter the paramters in the form 'param=value' separated by commas.")
    print("Default:")
    print("a=1,b=3.3,I=2,g=0,Vo=2,lam=10,thet=-0.6,c=1,d=5,r=0.001,s=4")

    user_pars = raw_input("")
    pars = {'a': 1, 'b': 3.3, 'I': 2, 'g': 1, 'Vo': 2, 'lam': 10, 'thet': -0.6, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'x1': x1, 'z': 0.}

    try:
        user_pars = user_pars.split(",")
        for i in range(len(user_pars)):
            pars[user_pars[i].split("=")[0]] = user_pars[i].split("=")[1]
    except:
        pars = {'a': 1, 'b': 3.3, 'I': 2, 'g': 1, 'Vo': 2, 'lam': 10, 'thet': -0.6, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'x1': x1, 'z': 0.}


    icdict = {'x': x, 'y': y}

    auxfndict = {'gam': (['x'], '1/(1+((2.71828)**(-1*lam*(x-thet))))')}

    xstr = 'y - a*x*x*x + b*x*x + I - z - g*(x-Vo)*gam(x)'
    ystr = 'c - d*x*x - y'

    DSargs = args(name='HindmarshRoseFast')
    """DSargs.fnspecs = {'Jacobian': (['t', 'x', 'y'], [-3*x*x + 6*x, 1.0],
                                                        [-10*x, -1.0]])}"""
    DSargs.pars = pars
    DSargs.varspecs = {'x': xstr, 'y': ystr}
    DSargs.fnspecs = auxfndict
    DSargs.ics = icdict
    DSargs.pdomain = {'z': [-14, 14]}

    testDS = Generator.Vode_ODEsystem(DSargs)
    # testDS = Generator.Radau_ODEsystem(DSargs)

    # Set up continuation class
    return ContClass(testDS)

def create_fast_diagram(HR_fast):
    PCargs = args(name='EQ1', type='EP-C')
    PCargs.freepars = ['z']
    PCargs.StepSize = 2e-3
    PCargs.MaxNumPoints = 450
    PCargs.MaxStepSize = 1e-1
    PCargs.LocBifPoints = 'all'
    PCargs.StopAtPoints = 'B'
    PCargs.SaveEigen = True
    PCargs.verbosity = 2
    HR_fast.newCurve(PCargs)

    print('Computing curve...')
    start = clock()
    HR_fast['EQ1'].forward()
    HR_fast['EQ1'].backward()
    print('done in %.3f seconds!' % (clock()-start))

    PCargs.name = 'LC1'
    PCargs.type = 'LC-C'
    PCargs.freepars = ['z']
    PCargs.initpoint = 'EQ1:H2'
    PCargs.MinStepSize = 1e-4
    PCargs.MaxStepSize = 0.1
    PCargs.StepSize = 0.1
    PCargs.MaxNumPoints = 240
    PCargs.LocBifPoints = []
    PCargs.NumIntervals = 200
    PCargs.NumCollocation = 6
    PCargs.NumSPOut = 30;
    PCargs.SolutionMeasures = 'all'
    PCargs.SaveEigen = True
    HR_fast.newCurve(PCargs)

    print('Computing LC-C from H1...')
    start = clock()
    HR_fast['LC1'].forward()
    print('done in %.3f seconds!' % (clock()-start))

def plot_fast_subsystem(HR_fast):
    """HR_fast['EQ1'].display(figure='new', coords=('z', 'x'), stability=True)
    HR_fast['LC1'].display(figure='fig1', coords=('z','x_max'), stability=True)
    HR_fast['LC1'].display(figure='fig1', coords=('z','x_min'), stability=True)"""

    HR_fast.plot.toggleAll('off', bytype='P')

    #HR_fast['LC1'].plot_cycles(figure='new', cycles='RG7', tlim='10T')     this is the plot we don't care about

def create_system():
    x1 = -0.5*(1+sqrt(5))
    x = x1
    y = 1-5*x*x

    print("2: Enter the paramters in the form 'param=value' separated by commas.")
    print("Default:")
    print("a=1,b=3.3,I=2,g=0,Vo=2,lam=10,thet=-0.6,c=1,d=5,r=0.001,s=4")

    user_pars = raw_input("")
    pars = {'a': 1, 'b': 3.3, 'I': 2, 'g': 1, 'Vo': 2, 'lam': 10, 'thet': -0.6, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'x1': x1}

    try:
        user_pars = user_pars.split(",")
        pars = {'a': 1, 'b': 3.3, 'I': 2, 'g': 1, 'Vo': 2, 'lam': 10, 'thet': -0.6, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'x1': x1}
        for i in range(len(user_pars)):
            pars[user_pars[i].split("=")[0]] = user_pars[i].split("=")[1]
    except:
        pars = {'a': 1, 'b': 3.3, 'I': 2, 'g': 1, 'Vo': 2, 'lam': 10, 'thet': -0.6, 'c': 1, 'd': 5, 'r': 0.001, 's': 4, 'x1': x1}


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
                      #'Jacobian_pars': (['t', 'I', 'r', 's', 'x1'],
                      #      """[[1.0, 0.0, 0.0, 0.0],
                      #          [0.0, 0.0, 0.0, 0.0],
                      #          [0.0, s*(x-x1)-z, r*(x-x1), -1*r*s]]""")}

    DSargs.pars = pars
    DSargs.varspecs = {'x': xstr, 'y': ystr, 'z': zstr}
    DSargs.fnspecs = auxfndict
    DSargs.ics = icdict
    DSargs.pdomain = {'g': [0., 6.]}
    DSargs.algparams = {'max_pts': 1000000}
    #DSargs.algparams = {'max_pts': 1000000, 'init_step': 1e-5, 'max_step': 1e-5}

    testDS = Generator.Vode_ODEsystem(DSargs)
    # testDS = Generator.Radau_ODEsystem(DSargs)


    return ContClass(testDS),pars

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

def fast_subsystem():
    # Bifurcation diagram for fast subsystem
    HR_fast = create_fast_subsystem()
    create_fast_diagram(HR_fast)
    #plot_fast_subsystem(HR_fast)

    # Create full HR system, compute cycle and plot over bifurcation diagram
    HR = create_system()
    HR_system = HR[0]
    HR_pars = HR[1]
    t_end = 1000
    HRtraj = create_HR_cycle(HR_system, t1=t_end)
    plotData = HRtraj.sample()
    #plt.figure(HR_fast.plot.fig1.fig.number)

    simulation = plt.figure(figsize=(10,6))
    simulation.subplots_adjust(wspace=0.3, hspace=0.25)
    title = ''
    for i in HR_pars:
        title += i + ":" + str(HR_pars[i]) + ", "

    print(title)
    simulation.suptitle(title)

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
    plt.xlabel('z')
    plt.ylabel('x')
    plot(plotData['z'], plotData['x'])
    plt.xlim([1.5, 2.4])
    plt.ylim([-1.8, 2])
    #need to find a way to zoom fit this curve and not the bification curve.

    HR_fast['EQ1'].display(coords=('z', 'x'), stability=True)
    HR_fast['LC1'].display(coords=('z','x_max'), stability=True)
    HR_fast['LC1'].display(coords=('z','x_min'), stability=True)

    return HR_fast

def full_system():
    # 9 spikes: I <= 2.131; 10 spikes: I >= 2.132 (AUTO: 10 spikes > 2.131891)
    # AGREEMENT WITH Radau, i.e. I = 2.131891 = 9 spikes, I = 2.131892 = 10 spikes
    HR.gensys.pars['g'] = 2.1373
    HRtraj2 = create_HR_cycle(HR)
    plotData2 = HRtraj2.sample()
    plot(plotData2['t'], plotData2['y'])
    HR.gensys.pars['g'] = 2.

    # Play with bifurcation diagram in HR system

    HR = create_system()[0]
    HRtraj = create_HR_cycle(HR)
    plotData = HRtraj.sample()
    cycle = plotData[4067:5421]
    cycle[-1] = cycle[0]
    t0 = 1310
    T0 = 452.84
    T = findApproxPeriod(HRtraj, t0, t0+T0, v='z', rtol=0.015)
    cycle = HRtraj.sample(dt=.01, tlo=t0, thi=t0+T)

    create_diagram(HR, cycle=cycle, EQ=False, LC=False)

    return HR

if __name__ == '__main__':
    HR = fast_subsystem()

    show(block=False)

    savesim = raw_input("save simulation? ")
    if(savesim == 'y'):
        simname = raw_input("Simulation name: ")
        if(simname == ''):
            simname = datetime.now().strftime('%Y.%m.%d|%H:%M:%S')
        plt.savefig('simulation_files/' + simname + '.png')
