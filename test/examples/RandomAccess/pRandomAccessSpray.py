import numpy as np

from SendMsg import *
from RecvMsg import *

from put_local import *

from RandomAccessRand import *
"""
Core of RandomAccess benchmark using Spray communication pattern
"""
DEBUG = 0
if DEBUG:
    print('--> Entering pRandomAccessSpray')

ran = ranStarts  # Initialize random sequence.
tag = 0 # Initialize message tag.

# Set optimal send and receive order to minimize communication contention.
mySendOrder = np.roll(list(range(Pid)) + list(range(Pid+1,Np)),-Pid)
myRecvOrder = np.flipud(mySendOrder)

# Loop over all update blocks.
for ib in myBLOCK:
    #  print('Update block #%d'%(ib))
    tag = (tag + 1)%32     # Increment messsage tag.

    # Create random numbers using official HPC Challenge RandomAccess
    # random number generator
    ran = RandomAccessRand(ran)
    Xi = np.float64(np.bitwise_and(ran,mask))   # Compute global table index.

    for p in mySendOrder:       # Find and send updates.
        ranSend = ran[ np.logical_and((Xi >= allX[p,1]),(Xi <= allX[p,2])) ]
        SendMsg(p,tag,ranSend)

    # Get local updates.
    if DEBUG:
        print('myX[0][0],myX[0][1] = %d,%d'%(myX[0][0],myX[0][1]))
        print('len(ran) = %d'%(len(ran)))
        print('len(Xi >= myX[0][0) & len(Xi <= myX[0][1]): %d,%d'%(len(Xi >= myX[0][0]),len(Xi <= myX[0][1])))

    ranRecv = ran[ np.logical_and((Xi >= myX[0][0]),(Xi <= myX[0][1])) ]

    for p in myRecvOrder:       # Receive updates.
        # Append receives.
        [t1] = RecvMsg(p,tag)
        ranRecv = np.concatenate((ranRecv,t1),axis=0,dtype=np.uint64)

    # Compute local index.
    Xi = np.float64(np.bitwise_and(ranRecv,mask)) - (myX[0][0])
    Xi = Xi.astype(int)

    if (not(VALIDATE)):     # Fast update.
        Xloc[Xi] = np.bitwise_xor(Xloc[Xi],ranRecv)
    else:    # Slow error free update.
        for j in range(len(ranRecv)):
            Xloc[Xi[j]] = np.bitwise_xor(Xloc[Xi[j]], ranRecv[j])

# Insert local values back into global table.
if (VALIDATE):
    X = put_local(X,Xloc)

if DEBUG:
    print('<-- Exiting pRandomAccessSpray')
DEBUG = 0

