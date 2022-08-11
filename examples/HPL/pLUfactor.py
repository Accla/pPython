import numpy as np
from scipy.linalg import lu
from timeit import default_timer as timer

# Import PythonMPI methods.
from pyMPI_Save_messages import *
from SendMsg import *
from RecvMsg import *

# pPython class
import pPython as GPC

from global_block_range import *
from global_block_ranges import *
from local import *
from put_local import *


def pLUfactor(A):
    """Parallel LU factorization on a column distributed NxN matrix A.

    """

    DEBUG = 0
    DEBUG2= 0
    if DEBUG:
        print('--> Entering pLUfactor')

    #  MPI information
    comm = GPC.comm
    Np = GPC.Np
    Pid = GPC.Pid

    N,N = A.shape                           # Get size of distributed array A.  
    # Python index starts from 0. Hene -1
    #                                         global_block_range returns a 2-D array [ 1 or N dimens, 2 (start,end)]
    myJ  = global_block_range(A,1)          # Get the local columns.
    #                                         global_block_ranges returns a 2-D array [ N dimensions, 3 (rank,start,end)]
    allJ = global_block_ranges(A,1)         # Get all the local columns.
    allNloc = allJ[0:,2] - allJ[0:,1] + 1   # Number of local columns., it returns a list of len(Np)
    if DEBUG:
        print('myJ: %s'%(str(myJ)))
        print('allJ: %s'%(str(allJ)))

    Aloc = local(A)                         # Get local part of A.
    Nloc = Aloc.shape[1]                    # Get local number of columns.
    #
    A = put_local(A,0)                    # Zero out local part of A.

    # Turn off message deletion to allow non-blocking broadcasts.
    comm = pyMPI_Save_messages(comm,1)

    pivots = (np.arange(N)).T               # Initialize pivots.

    for p in range(Np):                     # Loop over each Pid.
        if DEBUG:
            print('Pid = %d, Working on rank = %d'%(Pid,p))
        tagHigh = (2*p+1)%128               # High message tag.
        tagLow = (2*p)%128                  # Low message tag.
        if p == Pid:                        # Factor block p.
            i = range(myJ[0][0],N)          # Get rows to work on.
            if DEBUG:
                print('... Figuring out where to send message ...')
            """ 
            if 0:
                #  tic
                AlocSub = Aloc[myJ[0]:N,0:]
                [AlocSub pPivots] = dgetrf(AlocSub)
                Lloc = tril(AlocSub)
                Lloc(eye(numel(i),Nloc)==1) = 1      # Set diagonal to 1.
                #  Tgetrf = toc
            """

            if 1:
                # Get a zero clock.
                # zero_clock = timer()

                # AlocSub = Aloc[myJ[0][0]:N,0:]
                AlocSub = Aloc[i,0:]
                if DEBUG:
                    print('... LU factorization of array size, (%d,%d)'%(AlocSub.shape))
                pmat,AlocSub,Uloc = lu(AlocSub)                 # Factor.
                # Convert pivot matrix into a vector (equivalentt to pMatlab)
                pPivots = np.zeros(len(pmat),dtype=int)
                for k in range(len(pmat)):
                    pPivots[k] = np.where(pmat[0:,k]>0)[0][0]

                AlocSub[0:Nloc,0:] = AlocSub[0:Nloc,0:] + (Uloc - np.eye(Nloc,Nloc))    # Add back upper part.

                Lloc = np.tril(AlocSub)            # Get lower triangle.
                Lloc[np.eye(len(i),Nloc)==1] = 1   # Set diagonal to 1.
                #  Tlu = timer()

            pPivots = pPivots+myJ[0][0]            # Update pivots.

            #  T_after_lu = timer()
            pHigh = range(p+1,Np)            # Higher Pids.
            if DEBUG:
                print('pHIgh = %s'%(str(list(pHigh))))
            if len(pHigh)>0:              
                for pp in pHigh:
                    if DEBUG:
                        print('Called SendMsg when Pid = p to PId, %d'%(pp))
                    SendMsg(pp,tagHigh,Lloc,pPivots) # Send Lloc and pPivots to higher Pids.

            pLow = range(0,p)                # Lower Pids.
            if DEBUG:
                print('pLow = %s'%(str(list(pLow))))
            if len(pLow)>0:                 
                for pp in pLow:
                    if DEBUG:
                        print('Called SendMsg when Pid = p to PId, %d'%(pp))
                    SendMsg(pp,tagLow, pPivots)    # Send pPivots to lower Pids.

            # Tsend = timer()
            Aloc[myJ[0][0]:N,0:] = AlocSub

        elif Pid > p:
            # zero_clock = timer()
            if DEBUG:
                print('Called RecvMsg when Pid > p')
            [Lloc, pPivots] = RecvMsg(p,tagHigh)   # Receive L and pivots.
            # Trecv = timer()
        elif Pid < p:
            # zero_clock = timer()
            if DEBUG:
                print('Called RecvMsg when Pid < p')
            [pPivots] = RecvMsg(p,tagLow)         # Receive pivots.
            # Trecv = timer()

        # zero_clock2 = timer()
        i = range(allJ[p,1],N)                    # Remaining rows.
        pivots[i] = pivots[pPivots]               # Update pivot list.

        if p != Pid:
            Aloc[i,:] = Aloc[pPivots,:]           # Apply pivots everywhere else.
    
        # Apply multipliers to following blocks.
        if Pid > p:
            iL1 = range(allNloc[p])                # Upper rows of Lloc.
            iL2 = range(allNloc[p],Lloc.shape[0])  # Lower rows of Lloc.
            iA1 = range(allJ[p,1],allJ[p,2]+1)     # Current p rows of Aloc.
            iA2 = range(allJ[p,2]+1,N)             # Lower rows of Aloc.
            # Aloc[iA1,:] = Lloc[iL1,:]\Aloc[iA1,:]      # Solve.
            Aloc[iA1,:] = np.linalg.solve(Lloc[iL1,:], Aloc[iA1,:])         # Solve.
            Aloc[iA2,:] = Aloc[iA2,:] - np.matmul(Lloc[iL2,:],Aloc[iA1,:])  # Update.
        # Tapply = timer()

    # zero_clock2 = timer()
    # Turn  message deletion back on.
    # This shouldn't be necessary, but it is a good habit.
    comm = pyMPI_Save_messages(comm,0)

    Lloc = np.tril(Aloc, -(myJ[0][0]+1))         # Get lower triangle.
    i = range(myJ[0][0],myJ[0][1]+1)       # Get local rows.
    Lloc[i,:] = Lloc[i,:] + np.eye(Nloc,Nloc)    # Add ones to diagonal.

    L = put_local(A,Lloc)                        # Put into distributed array.
    Uloc = np.triu( Aloc, -(myJ[0][0]))          # Get upper triangle.
    U = L.copy()
    U = put_local(U,Uloc)                        # Insert into U.

    # Tput = timer()
    if DEBUG:
        print('<-- Exiting pLUfactor')
    return L,U,pivots

