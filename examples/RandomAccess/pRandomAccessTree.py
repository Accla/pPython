import numpy as np
from math import floor
from sympy import factorint

from pPython.utils import SendMsg,RecvMsg
from pPython.dmat import put_local

from RandomAccessRand import *

def pRandomAccessTree(VALIDATE,Np,Pid,myBLOCK,mask,ranStarts,allX,myX,Xloc,X):
    """
    Core of RandomAccess benchmark using Tree communication pattern
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering pRandomAccessTree')

    ran = ranStarts  # Initialize random sequence (retrun from RandomAccessStart())
    tag = 0 # Initialize message tag.

    # Factor processors into a tree.
    # factorint returns a dictionary with the key as the prime number & value as frequency
    if Np == 1:
        tree = [1]
    else:
        tree = [key for key, val in factorint(Np).items() for _ in range(val)]

    # Loop over all update blocks.
    for ib in myBLOCK:
        #  print('Update block #%d' %(ib))
        tag = (tag + 1)%32   # Increment messsage tag.

        # Create random numbers using official HPC Challenge RandomAccess
        # random number generator
        ran = RandomAccessRand(ran)

        ranRecv = ran  # Init input.

        # Initialize values for computing splits.
        midP = Np / tree[0]   
        modP = Np   
        k = 0

        # Loop over nodes of tree.
        #  for i=0:(numel(tree)-1)
        while (modP > 1):

            # Compute Pid to exchange info with.
            pairPid = int( (Pid + midP)%modP + floor(Pid/modP)*modP )

            # Compute Pid for splitting data.
            splitPid = int( midP + floor(Pid/modP)*modP )

            # Compute indices of all values.
            Xi = np.float64(np.bitwise_and(ranRecv,mask))

            # Find values above and below split.
            if DEBUG:
                print('Pid,pairPid,splitPid=%d,%d,%d'%(Pid,pairPid,splitPid))

            hi = ranRecv[Xi >= (allX[splitPid][1])]
            lo = ranRecv[Xi <  (allX[splitPid][1])]

            # Exchange hi/lo data.
            if (Pid < pairPid):
                SendMsg(pairPid,tag,hi)
                [t1] = RecvMsg(pairPid,tag)
                ranRecv = np.concatenate((lo,t1),axis=0,dtype=np.uint64)
            elif (Pid > pairPid):
                SendMsg(pairPid,tag,lo)
                [t1] = RecvMsg(pairPid,tag)
                ranRecv = np.concatenate((hi,t1),axis=0,dtype=np.uint64)

            # Update values for computing splits.
            midP = int(midP/tree[k])   
            modP = int(modP/tree[k])   
            k=k+1

        # Select low bits for local table index.
        # Convert to double/add one for Matlab/Fortran style indexing.
        Xi = np.float64(np.bitwise_and(ranRecv,mask)) - (myX[0][0])
        Xi = Xi.astype(int)

        if (not(VALIDATE)): # Fast update.
            if DEBUG:
                print('Fast update')
                t1 = Xloc[Xi]
                print('length: Xi,Xloc,ranRecv,t1 = %d,%d,%d,%d'%(len(Xi),len(Xloc),len(ranRecv),len(t1)))
            Xloc[Xi] = np.bitwise_xor(Xloc[Xi],ranRecv)
        else:    # Slow error free update.
            if DEBUG:
                print('Slow error free update')
            for j in range(len(ranRecv)):
                Xloc[Xi[j]] = np.bitwise_xor(Xloc[Xi[j]], ranRecv[j])

    # Insert local values back into global table.
    if (VALIDATE):
        X = put_local(X,Xloc)


    if DEBUG:
        print('<-- Exiting pRandomAccessTree')
    DEBUG = 0

