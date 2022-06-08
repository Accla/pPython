from math import log2
import numpy as np
from timeit import default_timer as timer
from scipy.fftpack import fft
from scipy.sparse import csr_matrix

# Import PythonMPI methods.
import GridPython as GPC
from GridMap import *
from rand import *
from zeros import *
from agg import *
from global_ind import *
from global_block_range import *
from global_block_ranges import *
from grid_complex import *
from cos import *
from sin import *
from transpose_grid import *

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
Np = GPC.comm_size
Pid = GPC.my_rank

PARALLEL=1                           # Turn parallelism on and off.

# Set vector/matrix dimensions.
N = (2**25)*Np  
N = (2**23)*Np  
M = int(N/Np)
# Debug.
# N = (2**20)*Np  
# M = int(N/Np)

VALIDATE = 1                         # Turn validation on or off.
ErrorRate = np.finfo(float).eps      # Set error to machine precision.

Xmap = 1                             # Serial map.
if PARALLEL:
    Xmap = GridMap([1,Np],{},range(Np)) # Parallel map.

print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))
print('Distributed vector size (words)    = %d'%(N))
print('Distributed vector size (bytes)    = %d'%(N*16))

tic = timer()
X = grid_complex(rand(1,N,Xmap),rand(1,N,Xmap)) # Create distributed vector.
Xloc = local(X)                      # Get local part.
Xshell = put_local(X,0)              # Create an empty X.

if VALIDATE:
    Xloc[:,:] = complex(0,0)                       # Reset to zero.
    phases = np.floor([3, np.log2(N), np.sqrt(N)]) # Create wave phases.
    for i in range(len(phases)):
        # Add one to index values to match with Matlab version
        omega = (2*np.pi*phases[i]/N) * (np.array(global_ind(X,1))+1) # Compute angle.
        Xloc = Xloc + grid_complex(cos(omega),sin(omega))             # Add wave to Xloc.
    X = put_local(X,Xloc)           # Insert back into X.

# Create twiddle factors
omega = (-2*np.pi*Pid/N) * np.arange(M)
omega = grid_complex(cos(omega),sin(omega))
Talloc = timer()-tic

print('Local vector size (bytes)          = %d'%(len(Xloc)*16))
print('Allocation Time (sec)              = %f'%(Talloc))

tic = timer()
sync = agg(zeros(1, Np, Xmap))       # Synchronize start.
Tlaunch = timer()-tic
print('Launch Time (sec)                  = %f'%(Tlaunch))

#####################################################################################
# BEGIN BENCHMARK
tic = timer()
Xloc = np.reshape(Xloc,(Np,int(M/Np)),order='F') # Reshape local part into a matrix.
X = put_local(zeros(Np,M,Xmap),Xloc)
Tcomp = timer()-tic

print('Begin 1st CornerTurn')
tic = timer()
X = transpose_grid(X)                # Redistribute along 1st dimension.
Xloc = local(X)
Tcomm = timer()-tic

print('Begin FFT of 2nd Dimension')
tic = timer()
Xloc = fft(Xloc,axis=1)              # FFT 2nd dimension.
Xloc = omega * Xloc                  # Multiply by twiddle factors.
X = put_local(X,Xloc)
Tcomp = Tcomp + timer()-tic

print('Begin 2nd CornerTurn');
tic = timer()
X = transpose_grid(X)                # Redistribute along 2nd dimension.
Xloc = local(X) 
Tcomm = Tcomm + timer()-tic

tic = timer()
Xloc = fft(Xloc,len(Xloc),0)         # FFT 1st dimension. Needs len(Xloc)
X = put_local(X,Xloc)
Tcomp = Tcomp + timer()-tic

tic = timer()
X = transpose_grid(X)                # Redistribute along 1st dimension.
Xloc = local(X)
X = put_local(Xshell,Xloc)           # Insert back into vector.
Tcomm = Tcomm + timer()-tic
Trun = Tcomp + Tcomm;

GigaFlops = 5*N*log2(N)/Trun/1.e9    # Performance in gigaflops
GigaByteSec = 3*16*N/Tcomm/1.e9      # Communication bandwidth.

print('Compute time (sec)                 = %f'%(Tcomp))
print('Communication time (sec)           = %f'%(Tcomm))
print('Run time (sec)                     = %f'%(Trun))
print('Performance (Gigaflops)            = %f'%(GigaFlops))
print('Bandwidth (Gigabytes/sec)          = %f'%(GigaByteSec))

if VALIDATE:
    myX = global_block_range(X,1)[0] # Get global index.
    iphase = phases                  # Get phase index. Remove 1 to reflect Python index start from 0
    myiphase = iphase[np.logical_and((myX[0] <= iphase),(iphase <= myX[1]))] - myX[0]
    Errloc = np.amax(abs(Xloc))/(N**1.5)

    if myiphase.size>0:
        # Zloc = sparse(myiphase,1,N,M,1)
        j = np.zeros(len(myiphase),dtype=int)
        v = np.zeros(len(myiphase),dtype=int)
        v[:] = N
        Zloc = csr_matrix((v, (myiphase, j)), shape=(M, 1))
        Errloc = np.amax(abs(np.transpose(abs(Xloc)) - Zloc))/(N**1.5)

    print('Max local error                    = %f'%(Errloc))
    Err = put_local(zeros(1,Np,Xmap),Errloc)
    Erragg = agg(Err)
    if (Pid == 0):
        maxErr = np.amax(Erragg)
        print('Max error                          = %f'%(maxErr))
        if (maxErr > ErrorRate):
            print('Validation Failed')
        else:
            print('Validation Passed')

print('')
print('SUCCESS')
print('')

