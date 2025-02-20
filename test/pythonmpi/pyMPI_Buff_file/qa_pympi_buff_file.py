"""Test SendMsg/RecvMsg/MPI_Mcast functions
"""

import numpy as np

# import PythonMPI/gridPython
from pyMPI_Buffer_file import *

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
tag = 1004

print('Case 2: 7 arguments')

if Pid == 0:
    buff_file = pyMPI_Buffer_file(0,3,tag,comm,local_fs=1,msg_type='send',innode=0)
else:
    buff_file = pyMPI_Buffer_file(Pid,0,tag,comm,local_fs=1,msg_type='recv',innode=1)

# Verification
print('My buff file name:')
print(buff_file)


print('Case 1: 4 arguments')
if Pid == 0:
    buff_file = pyMPI_Buffer_file(0,3,tag,comm)
else:
    buff_file = pyMPI_Buffer_file(Pid,0,tag,comm)

# Verification
print('My buff file name:')
print(buff_file)


print(' ')
print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')
print(' ')

