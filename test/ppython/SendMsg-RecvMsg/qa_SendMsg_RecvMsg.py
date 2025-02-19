"""Test SendMsg/RecvMsg functions
"""

import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

# import PythonMPI/gridPython
from SendMsg import *
from RecvMsg import *

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


print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')
print(' ')

