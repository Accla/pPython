"""Test SendMsg/RecvMsg/MPI_Mcast functions
"""

import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

# import PythonMPI/gridPython
from SendMsg import *
from RecvMsg import *
from MPI_Mcast import *

# Import gridPython methods.
# pPython class
import pPython as GPC
from Dmap import *
from zeros import *
from global_ind import *
from local import *
from put_local import *
from synch import *
from agg import *

# Create communicator.
# pPython as GPC in gridPython.py
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Create a random 2-D array
N = 3

# Case 1: SendMsg and RecvMsg (point-to-point communication)
print('\n1. SendMsg and RecvMsg (point-to-point communication)\n')
# Send myMat to the last MPI process
if Pid == 0:
    myMat = np.random.rand(N,N)
else:
    myMat = np.zeros((N,N))
tag = 1004
if Pid == 0:
    SendMsg(Np-1,tag,myMat)
elif Pid == Np-1:
    [myMat] = RecvMsg(0,tag)

# Verification
print('Check myMat:')
# print('Type: %s'%(type(myMat)))
print(myMat)


# Case 2: MPI_Mcast with SendMsg (multi-cast)
print('\n2. MPI_Mcast with SendMsg (multi-cast)\n')
if Pid == 0:
    myMat = np.random.rand(N,N)

destination = list(range(Np))
tag += 1
if Pid == 0: 
    SendMsg(destination,tag,myMat)
else:
    [myMat] = RecvMsg(0,tag)

# Verification
print('Check myMat:')
# print('Type: %s'%(type(myMat)))
print(myMat)

# Case 3: SendMsg and RecvMsg with multiple messages as argument (point-to-point communication)
print('\n3. SendMsg and RecvMsg with multiple messages as argument (point-to-point communication)\n')
# Send myMat to the last MPI process
if Pid == 0:
    myMat = np.random.rand(N,N)
    myMat2 = np.random.rand(N,N)
else:
    myMat = np.zeros((N,N))
    myMat2 = np.zeros((N,N))
tag = 1004
if Pid == 0:
    SendMsg(Np-1,tag,myMat,myMat2)
elif Pid == Np-1:
    myMat,myMat2 = RecvMsg(0,tag)

# Verification
print('Check myMat:')
print(myMat)
print('Check myMat2:')
print(myMat2)


# Case 4: MPI_Mcast for multiple messages with SendMsg (multi-cast)
print('\n4. MPI_Mcast for multiple messages with SendMsg (multi-cast)\n')
if Pid == 0:
    myMat = np.random.rand(N,N)
    myMat2 = np.random.rand(N,N)

destination = list(range(Np))
tag += 1
if Pid == 0: 
    SendMsg(destination,tag,myMat,myMat2)
else:
    [myMat,myMat2] = RecvMsg(0,tag)

# Verification
print('Check myMat:')
print(myMat)
print('Check myMat2:')
print(myMat2)

print(' ')
print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')
print(' ')

