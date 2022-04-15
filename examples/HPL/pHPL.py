import numpy as np
import scipy.io
from timeit import default_timer as timer

# Import gridPython methods.
from GridMap import *
import GridPython as GPC
from local import *
from zeros import *
from rand import *
from agg import *
from global_ind import *

from pLUsolve import *

"""
    Implementation of the HPC Challenge Higher Performance Linpack
    benchmark which solve the equation Ax = b.
    To run in serial without distributed arrays, set         
      PARALLEL = 0
    At the Matlab prompt type
      pHPL
    To run in serial with distributed arrays, set         
      PARALLEL = 1
    At the Matlab prompt type
      pHPL
    To run in parallel with distributed arrays
    at the Matlab prompt type 
      eval(pRUN('pHPL',2,{}))
"""

#  MPI information
comm = GPC.comm
Np = GPC.comm_size
Pid = GPC.my_rank

# Turn parallelism on or off.
PARALLEL = 1  # Can be 1 or 0.
VERIFY = 1

Amap = 1                                 # Serial map.
if PARALLEL:
    Amap = GridMap([1,Np],{},range(Np))    # Parallel map.

#N = 2^14  # Largest on a single beta grid node ~600 seconds on 1 cpu.
#N = Np*floor(floor(10000*sqrt(Np))/Np)
#N = Np*floor(floor(12500*sqrt(Np))/Np)
#N = 1500
#N = 2^12
#N = 2^10
#N = Np*floor(floor((2^12)*sqrt(Np))/Np)
N = Np*np.floor(np.floor(5000*np.sqrt(Np))/Np)
N = 24  # Debug

print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))
print('Distributed matrix size            = (%d)^2 words'%(N))
print('Distributed matrix size (bytes)    = %d'%((N**2)*8))

#
# Read in the proble to solve:
#
mat_contents = scipy.io.loadmat('test.mat')
b = mat_contents['b']
myLoc = mat_contents['myLoc']
x = mat_contents['x']

print('The given problem to solve:')
print('A matrix:')
# myLoc = local(A)
print(myLoc)
print('b vector:')
print(b)

zero_clock = timer()
# b = np.random.rand(N,1) - 0.5   # Create a replicated column vector.
# A = rand(N,N,Amap) - 0.5        # Create a distributed matrix.
A = zeros(N,N,Amap)         # Create a distributed matrix.
# A = zeros(N,N,Amap) - 0.5        # Create a distributed matrix.
Talloc = timer()

my_global_ind = global_ind(A)
print('my global index')
print(my_global_ind[0])
print(my_global_ind[1])
myNewLoc = myLoc[0:,my_global_ind[1][0]:my_global_ind[1][-1]+1]
#CB print(myNewLoc)


print('Local matrix size (bytes)          = %d'%(np.prod((local(A)).shape)*8))
print('Allocation Time (sec)              = %f'%(Talloc-zero_clock))

zero_clock = timer()
sync = agg(zeros(1, Np, Amap))   # Synchronize start.
Tlaunch = timer()
print('Launch Time (sec)                  = %f'%(Tlaunch-zero_clock))

# A = put_local(A,myLoc)
A = put_local(A,myNewLoc)
# print('A matrix:')
# print(local(A))

zero_clock = timer()
x2 = pLUsolve(A,b)                # Solve  A x = b.
Trun = timer()
GigaFlops = (2/3*N**3 + 3/2*N**2)/(Trun-zero_clock)/1.e9   # Performance in gigaflops.

print('Run Time (sec)                     = %f'%(Trun-zero_clock))
print('Performance (Gigaflops)            = %f'%(GigaFlops))

print('x2 solution:')
print(x2)

# scipy.io.savemat('test.mat', dict(x=x, b=b, myLoc=myLoc))

print('After pLUsover: A matrix:')
print(local(A))

if (VERIFY):
    # Scaled residuals
    A = agg(A)
    if (Pid == 0):
        eps = np.finfo(float).eps
        # ToDo:  matrix multiplication of a distributed array
        r=np.matmul(A,x2) - b
        normA1 = max(sum(abs(local(A))))
        print('normA1: %f'%(normA1))
        normAInf = max(np.sum(abs(local(A)),1))
        if len(local(r).shape) == 1:
            res0 = max(abs(local(r)))
        else:
            res0 = max(np.sum(abs(local(r)),axis=1))
        print(res0)
        res1 = res0 / (eps * normA1 * N)
        res2 = res0 / (eps * normA1 * np.linalg.norm(x,1))
        res3 = res0 / (eps * normAInf * np.linalg.norm(x,np.inf) * N)
        print('res1,res2,res3: %f,%f,%f'%(res1,res2,res3))

        threshold = 16.
        if max(res1, res2, res3) < threshold:
            print('Verification Passed');
        else:
            print('Failure');

