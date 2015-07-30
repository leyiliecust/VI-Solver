import time
import numpy as np

from VISolver.Domains.Lienard import Lienard

# from VISolver.Solvers.Euler import Euler
# from VISolver.Solvers.Extragradient import EG
# from VISolver.Solvers.AcceleratedGradient import AG
# from VISolver.Solvers.HeunEuler import HeunEuler
# from VISolver.Solvers.AdamsBashforthEuler import ABEuler
# from VISolver.Solvers.CashKarp import CashKarp
from VISolver.Solvers.Euler_LEGS import Euler_LEGS
from VISolver.Solvers.CashKarp_LEGS import CashKarp_LEGS

# from VISolver.Projection import IdentityProjection, LyapunovGSRProjection
from VISolver.Solver import Solve
from VISolver.Options import (
    DescentOptions, Miscellaneous, Reporting, Termination, Initialization)
from VISolver.Log import PrintSimResults, PrintSimStats

from matplotlib import pyplot as plt

from IPython import embed


def Demo():

    #__CLOUD_SERVICES__##################################################

    # Define Network and Domain
    Domain = Lienard()

    # Set Method
    # Method = Euler(Domain=Domain,P=LyapunovGSRProjection())
    # Method = EG(Domain=Domain,P=IdentityProjection())
    # Method = AG(Domain=Domain,P=IdentityProjection())
    # Method = HeunEuler(Domain=Domain,P=IdentityProjection(),Delta0=1e-5)
    # Method = ABEuler(Domain=Domain,P=IdentityProjection(),Delta0=1e-4)
    # Method = CashKarp(Domain=Domain,P=LyapunovGSRProjection(),Delta0=1e-6)
    # Method = Euler_LEGS(Domain=Domain)
    Method = CashKarp_LEGS(Domain=Domain,Delta0=1e-6,Delta0_L=1e-4,
                           GrowthLimit=2,MinStep=1e-3,MaxStep=1)

    # Initialize Starting Point (includes psi)
    # Start = np.array([0,-1.0,1,0,0,1])
    Start = np.array([0,-1.0e-0])
    # Start = np.array([0,-2.0e-0])
    # Start = np.array([1.05151222,2.11233182])
    # Start = np.array([0,0])

    # Set Options
    Init = Initialization(Step=1e-3)
    # Init = Initialization(Step=0.1)
    Term = Termination(MaxIter=1e5)
    Repo = Reporting(Requests=['Step','Data','Lyapunov','L-Step'])
    Misc = Miscellaneous()
    Options = DescentOptions(Init,Term,Repo,Misc)

    # Print Stats
    PrintSimStats(Domain,Method,Options)

    # Start Solver
    tic = time.time()
    Lienard_Results = Solve(Start,Method,Domain,Options)
    toc = time.time() - tic

    # Print Results
    PrintSimResults(Options,Lienard_Results,Method,toc)

    # T_elapsed = sum(Lienard_Results.PermStorage['Step'])
    # print(Domain.Lyapunov/T_elapsed)

    # X,Y = np.meshgrid(np.arange(-1.5,1.5,.05),np.arange(-1.5,1.5,.05))
    # U,V = np.empty_like(X), np.empty_like(Y)
    # for i in xrange(X.shape[0]):
    #     for j in xrange(Y.shape[1]):
    #         print((i,j))
    #         dat = np.array([X[i,j],Y[i,j]])
    #         grad = Domain.F(dat)
    #         U[i,j], V[i,j] = grad[0], grad[1]
    # plt.figure()
    # Q = plt.quiver(X[::3, ::3],Y[::3, ::3],U[::3, ::3],V[::3, ::3],
    #                pivot='mid', color='r', units='inches')
    # qk = plt.quiverkey(Q, 0.5, 0.03, 1, r'$1 \frac{m}{s}$',
    #                    fontproperties={'weight ': 'bold'})
    # plt.plot(X[::3, ::3],Y[::3, ::3],'k.')
    # plt.axis([-1.5, 1.5, -1.5, 1.5])
    # plt.title("pivot='mid'; every third arrow; units='inches'")
    # plt.show()

    iters = Lienard_Results.thisPermIndex

    Lyapunov = np.zeros((iters+1,Start.size))
    T_elapsed = np.cumsum(Lienard_Results.PermStorage['Step'])
    for idL,L in enumerate(Lienard_Results.PermStorage['Lyapunov']):
        if idL == 0:
            Lyapunov[idL,:] = L
        else:
            Lyapunov[idL,:] = L/T_elapsed[idL-1]
        # Lyapunov[idL,:] = L/max(1,idL)
    print(Lyapunov[-1])
    # embed()

    data = np.zeros((iters+1,2))
    for idx,x in enumerate(Lienard_Results.PermStorage['Data']):
        data[idx,:] = x[0:2]
    plt.plot(data[:,0],data[:,1])
    ax = plt.gca()
    ax.set_xlim([-3,3])
    ax.set_ylim([-3,3])
    plt.show()

    plt.plot(Lyapunov)
    plt.show()

    Step_L = Lienard_Results.PermStorage['L-Step']
    plt.plot(Step_L)
    plt.show()

    Step = Lienard_Results.PermStorage['Step']
    plt.plot(Step)
    plt.show()

    # embed()

if __name__ == '__main__':
    Demo()
