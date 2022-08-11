import numpy as np
import os
from timeit import default_timer as timer

import pPython as GPC
from Dmap import *
from rand import *
from zeros import *
from local import *

from write_parallel_matrix import *
from read_parallel_matrix import *

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
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('my_rank: %d'%(Pid))

# Set the problem dimensions and filename.
N = 2^16   
M = 128   

if not os.path.exists(os.path.join(os.getcwd(), 'dat')):
    os.mkdir('dat')
FILE = './dat/pIOvector_'+str(Pid)+'.npz'

N = 2^14      # Debug.
PARALLEL = 1  # Set control flag.
Xmap = 1  
Ymap = 1      # Create serial maps.
if (PARALLEL):
    Xmap = Dmap([1,Np],{},range(Np))  
    Ymap = Xmap           # Create parallel maps.

Xrand = rand(N,M,map=Xmap)    # Create distributed array.
Yrand = zeros(N,M,map=Ymap)   # Create distributed array.
tic = timer()             # Start clock.
write_parallel_matrix(Xrand,FILE)   # Save files.
Twrite = timer() - tic    # Stop clock.
print('Write Time (sec)                   = %f'%(Twrite))
tic = timer()             # Start clock.
Yrand = read_parallel_matrix(Yrand,FILE)  # Read files.
Tread = timer() - tic     # Stop clock.
print('ead Time (sec)                     = %f'%(Tread))

# Compare results.
# max_difference = np.amax(np.amax(abs( local(Xrand) - local(Yrand) )))
max_difference = np.amax(abs( local(Xrand) - local(Yrand) ))

if (max_difference > 0):
    print('ERROR')
    print(max_difference)
else:
    print('')
    print('')
    print('SUCCESS')
    print('')
    print('')


