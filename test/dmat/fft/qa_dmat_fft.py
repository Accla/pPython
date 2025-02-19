from math import log2
import numpy as np
from timeit import default_timer as timer
from scipy.sparse import csr_matrix

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
from dcomplex import *
from cos import *
from sin import *
from transpose_grid import *
from fft import *

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
N = (2**25)*Np  
M = int(N/Np)
# Debug.
# N = (2**4)*Np  
N = (2**20)*Np  
M = int(N/Np)

VALIDATE = 1              # Turn validation on or off.
ErrorRate = np.finfo(float).eps           # Set error to machine precision.

Xmap = 1                  # Serial map.
if PARALLEL:
    Xmap = Dmap([1,Np],{},range(Np))    # Parallel map.

print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))
print('Distributed vector size (words)    = %d'%(N))
print('Distributed vector size (bytes)    = %d'%(N*16))

tic = timer()
X = dcomplex(rand(1,N,map=Xmap),rand(1,N,map=Xmap))    # Create distributed vector.

# print('Initial X:')
# print(local(X))

Xloc = local(X)                     # Get local part.
Xshell = put_local(X,0)             # Create an empty X.

if VALIDATE:
    Xloc[:,:] = complex(0,0)                       # Reset to zero.
    phases = np.floor([3, np.log2(N), np.sqrt(N)]) # Create wave phases.
    for i in range(len(phases)):
        # print(np.array(global_ind(X,1)) )
        # Add one to match with Matlab version
        omega = (2*np.pi*phases[i]/N) * (np.array(global_ind(X,1))+1)  # Compute angle.
        # print(omega)
        Xloc = Xloc + dcomplex(cos(omega),sin(omega))     # Add wave to Xloc.
    # print('After put_local(X,Xloc)')
    # print(Xloc)
    X = put_local(X,Xloc)               # Insert back into X.
    # print(local(X))

# print('Save initial Xglobal, ID=0')
# save_result(X,Pid,0)

# Create twiddle factors
omega = (-2*np.pi*Pid/N) * np.arange(M)
omega = dcomplex(cos(omega),sin(omega))
Talloc = timer()-tic

print('Local vector size (bytes)          = %d'%(len(Xloc)*16))
print('Allocation Time (sec)              = %f'%(Talloc))

tic = timer()
sync = agg(zeros(1, Np, map=Xmap))      # Synchronize start.
Tlaunch = timer()-tic
print('Launch Time (sec)                  = %f'%(Tlaunch))

#####################################################################################
# BEGIN BENCHMARK
tic = timer()
Xloc = np.reshape(Xloc,(Np,int(M/Np)),order='F')            # Reshape local part into a matrix.
# print('Xloc after reshape')
# print(Xloc)

X = put_local(zeros(Np,M,map=Xmap),Xloc)
print('Before reshape: size of Xloc is %s'%(str(Xloc.shape)))
Tcomp = timer()-tic

# Call gridPython fft() for GridDmat
# Default direction, whcih is along the column
X = fft(X)

print('fft in the dimension which is broken onto multiple processors')
X = fft(X,[],1)

print('')
print('')
print('')
print('SUCCESS')
print('')
print('')
print('')


