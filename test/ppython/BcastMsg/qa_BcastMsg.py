"""Test BcastMsg functions
"""

import numpy as np

# import PythonMPI/gridPython
from BcastMsg import *

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
    myMat2 = np.random.rand(N,N)
else:
    myMat = np.zeros((N,N))
    myMat2 = np.zeros((N,N))

print('Case 1: Broadcast one variable.')
tag = 1004
[myMat] = BcastMsg(0,tag,myMat)
# Verification
print('Check myMat:')
print(myMat)

print('Case 2: Broadcast two variables.')
tag = 1005
[myMat,myMat2] = BcastMsg(0,tag,myMat,myMat2)
# Verification
print('Check myMat:')
print(myMat)
print('Check myMat2:')
print(myMat2)


print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')

