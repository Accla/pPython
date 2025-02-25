import numpy as np
from timeit import default_timer as timer

# Import PythonMPI methods.
from SendMsg import *
from RecvMsg import *

# pPython class
import pPython as GPC
from global_block_range import *
from global_block_ranges import *
from local import *
from put_local import *

from pLUfactor import *

def pLUsolve(A,b):
    """Solves A x = b on a column distributed NxN matrix A
    using parallel LU factorization.
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering pLUsolve')

    #  MPI information
    comm = GPC.comm
    Np = GPC.Np
    Pid = GPC.Pid

    [N,N] = list(A.shape)                       # Get size of distributed array A.  
    # Python index starts from 0. Hene -1
    # global_block_range returns a 2-D array [ 1 or N dimens, 2 (start,end)]
    myJ  = global_block_range(A,2-1)     # Get the local columns.

    # zero_clock = timer()
    L,U,pivots = pLUfactor(A)       # Call parallel LU.
    # TpLUfactor = timer()

    Lloc = local(L)                   # Get local L.
    Uloc = local(U)                   # Get local U.
    x = b[pivots,:]                   # Pivot rows of b.

    for p in range(Np):               # Loop up over each Pid.
        if DEBUG:
            print('Loop over Np: p = %d'%(p))
        tag = p%32                    # Set message tag.
        if Pid == p:
            i = list(range((myJ[0][1]+1),N))          # Upper block of rows.
            j = list(range((myJ[0][1]-myJ[0][0]+1)))  # Lower block of columns.
            k = list(range(myJ[0][0],myJ[0][1]+1))    # Middle block of rows.
            # Python way to extract sub-matrix
            temp_Lloc = Lloc[k[0]:k[-1]+1,j[0]:j[-1]+1]
            if DEBUG:
                # print('Permuted lower matrix, Lloc:')
                # print(temp_Lloc)
                print('Permuted vector, x:')
                print(x[k,:])

            x[k,:] = np.linalg.solve(temp_Lloc,x[k,:]) # Solve L x' = x.
            # Python way to extract sub-matrix
            if len(i)>0:
                temp_Lloc = Lloc[i[0]:i[-1]+1,j[0]:j[-1]+1]
                x[i,:] = x[i,:] - np.matmul(temp_Lloc,x[k,:])
            if p < Np-1:
                if DEBUG:
                    print('Called SendMsg: Send x to the higher Pid, %d'%(p+1))
                SendMsg(p+1,tag,x)    # Send x to the higher Pid.
        elif Pid == p+1:
            if DEBUG:
                print('Called RecvMsg: Recv x from the lower Pid, %d'%(p))
            [x] = RecvMsg(p,tag)      # Recv x from the lower Pid.
                           
    if DEBUG:
        print('Processed vector, x:')
        print('Length of x = %d'%(len(x)))
        print(x[k,:])

    for p in range((Np-1),-1,-1):        # Loop down over each Pid.
        if DEBUG:
            print('Loop over Np: p = %d'%(p))
        tag = p%32                        # Set message tag.
        if Pid == p:
            i = list(range(myJ[0][0]))                 # Upper block of rows.
            j = list(range((myJ[0][1]-myJ[0][0]+1)))   # Lower block of columns.
            k = list(range(myJ[0][0],myJ[0][1]+1))     # Middle block of rows.
            if DEBUG:
                print('len(i) = %d'%(len(i)))
                print(i)
                print('len(j) = %d'%(len(j)))
                print(j)
                print('len(k) = %d'%(len(k)))
                print(k)
                print('Length of x = %d'%(len(x)))
            # Python way to extract sub-matrix
            temp_Uloc = Uloc[k[0]:k[-1]+1,j[0]:j[-1]+1]
            if DEBUG:
                # print('Permuted upper matrix, Uloc:')
                # print(temp_Uloc)
                print('Permuted vector, x:')
                print('Length of x = %d'%(len(x)))
                print(x.shape)
                print(k)
                # print(x[k,:])

            x[k,:] = np.linalg.solve(temp_Uloc,x[k,:]) # Solve U x' = x.
            if len(i)>0:
                temp_Uloc = Uloc[i[0]:i[-1]+1,j[0]:j[-1]+1]
                x[i,:] = x[i,:] - np.matmul(temp_Uloc,x[k,:])
            if p > 0:
                SendMsg(p-1,tag,x)        # Send x to the lower Pid.
        elif Pid == p-1:
            [x] = RecvMsg(p,tag)            # Recv x from the higher Pid.

    tag = 3                               # Reset message tag.
    if Pid == 0:
        p_higher = list(range(1,Np))
        if len(p_higher)>0:
            # SendMsg(p_higher,tag,x)    # Send x to all other Pids.
            for pp in p_higher:
                if DEBUG:
                    print('Called SendMsg: Send Lloc and pPivots to higher Pid, %d'%(pp))
                SendMsg(pp,tag,x)        # Send Lloc and pPivots to higher Pids.
    else:
        if DEBUG:
            print('Called RecvMsg: Received x from lower Pids.')
        [x] = RecvMsg(0,tag)               # Received x from lower Pids.

    # TpLUsolve = timer
    if DEBUG:
        print('<-- Exiting pLUsolve')

    return x

