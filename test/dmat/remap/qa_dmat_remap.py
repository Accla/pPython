from math import log2
import numpy as np
from timeit import default_timer as timer

# Import PythonMPI methods.
import pPython as GPC
from Dmap import *
from rand import *
from zeros import *
from agg import *
from global_ind import *
from global_block_range import *
from global_block_ranges import *

# newly introduced
# from ll_grid import *
from size import *
from remap import *

"""
This script implements a simple 1D FFT benchmark using a 2D approach, which is
the most common way of implementing a 1D FFT in parallel.  
This benchmark contains a parallel implementation of this algorithm.

Parameters:
* PARALLEL - Enable the pPython library.
* VALIDATE - Enable validation of FFT result.
* ERROR_LIMIT - Error limit used in validation.
* N - length of vector to FFT, must be divisible by Np**2.

To run in serial without distributed arrays, set
    PARALLEL = 0
At the Python prompt type
    pFFT
To run in serial with distributed arrays, set
    PARALLEL = 1
At the Python prompt type
    pFFT
To run in parallel with distributed arrays
at the Python prompt type
    eval(pRUN('pFFT',2,{}))
"""

#  MPI information
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# PARAMETERS (OK to change)
# extract QA_PARALLEL environment variable
# Turn parallelism on or off.
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0
# PARALLEL=1                # Turn parallelism on and off.

# Set vector/matrix dimensions.
M = Np
N = 15

xmap = 1
if PARALLEL:
    xmap = Dmap([Np, 1],{},range(Np))

X = rand(M,N,map=xmap)
print(' ')
xmap.show()
print(' ')
#
Xglobal = agg(X)
print('Distributed global array:')
print(Xglobal)
#
print('Local array:')
print(local(X))


print('WARNING: @dmat/fft: The matrix is not mapped along the appropriate dimension, remapping along columns.')
print('REMAPPING CODE')
g = grid(X)
grid_dims = size(g)
grid_spec = [1, grid_dims[0]*grid_dims[1]]
old_map = X.map
dist_spec = old_map.dist_spec
proc_list = list(g.flatten('F'))
new_map = Dmap(grid_spec, dist_spec, proc_list)
new_map.show()
X = remap(X,new_map)

print('Re-distributed global array:')
Xglobal = agg(X)
print(Xglobal)
#
print('Local array:')
print(local(X))

print('')
print('')
print('')
print('SUCCESS')
print('')
print('')
print('')


