"""Test SendMsg/RecvMsg/MPI_Mcast functions
"""

import numpy as np

# import PythonMPI/gridPython
from MPI_Bcast import *

# Import gridPython methods.
# pPython class
import pPython as GPC

# Create communicator.
# pPython as GPC in gridPython.py
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Create a random 2-D array
N = 3
if Pid == 0:
    myMat = np.random.rand(N,N)
else:
    myMat = np.zeros((N,N))

tag = 1004
[myMat] = MPI_Bcast(0,tag,comm,myMat)

# Verification
print('Check myMat:')
# print('Type: %s'%(type(myMat)))
print(myMat)


print(' ')
print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')
print(' ')

