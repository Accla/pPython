# import Python module
import numpy as np
import os
from timeit import default_timer as timer

# import pPython modules
import pPython as GPC
from pPython.map import Dmap,rand,zeros
from pPython.dmat import local

# import local modules
from matrix_util import write_matrix,read_matrix

"""
This script creates a distributed matrix. Writes it
out in a scalable way and the reads it back in.
To run in serial without distributed arrays, set
    PARALLEL = 0
At the PYthon prompt type
    pIO
To run in serial with distributed arrays, set
    PARALLEL = 1
At the PYthon prompt type
    pIO
To run in parallel with distributed arrays
at the PYthon prompt type
    eval(pRUN('pIO',2,{}))
"""

#  MPI information
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('my_rank: %d'%(Pid))

# Set the problem dimensions and filename.
N = 2**22; M = 128   
N = 2^14 # Debug.

if not os.path.exists(os.path.join(os.getcwd(), 'dat')):
    os.mkdir('dat')
FILE = './dat/pIOvector'

PARALLEL = 1  # Set control flag.
Xmap = 1; Ymap = 1  # Create serial maps.
if (PARALLEL): # Create parallel maps.
    Xmap = Dmap([1,Np],{},range(Np)); Ymap = Xmap

print('Global matrix size: %d x %d'%(N,M))
Xrand = rand(N,M,map=Xmap)    # Create distributed array.
Yrand = zeros(N,M,map=Ymap)   # Create distributed array.
tic = timer()             # Start clock.
write_matrix(Xrand,FILE)   # Save files.
Twrite = timer() - tic    # Stop clock.
print('Write Time (sec)                   = %10.4f'%(Twrite))
tic = timer()             # Start clock.
Yrand = read_matrix(Yrand,FILE)  # Read files.
Tread = timer() - tic     # Stop clock.
print('Read Time (sec)                     = %10.4f'%(Tread))

# Compare results.
max_difference = np.amax(abs( local(Xrand) - local(Yrand) ))

if (max_difference > 0):
    print('ERROR')
    print(max_difference)
else:
    print('')
    print('SUCCESS')
    print('')


