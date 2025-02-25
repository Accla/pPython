"""test_remote_exec.py
    Test pPython distributed array function, remote_exec()

    To run, start Pyhton and type:

        pRun('test_disp.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/test_remote_exec.0.out
        . . . 
        PythonMPI/test_remote_exec.3.out

    pPython
    Dr. Chansup Byun
    MIT Lincoln Laboratory
    cbyun@ll.mit.edu
"""
import os
import numpy as np
from timeit import default_timer as timer


# Import gridPython methods.
# pPython class
import pPython as GPC

from slurm2hostmap import *

# extract QA_PARALLEL environment variable
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

# Create communicator.
# pPython as GPC in gridPython.py
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('Pid: %d'%(Pid))

slurm2hostmap()

print(' ')
print('SUCCESS ')
print(' ')
