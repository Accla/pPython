import numpy as np
from timeit import default_timer as timer

# Import gridPython methods.
from Dmap import *
import pPython as GPC
from local import *
from print_falls import *
from rand import *
from zeros import *
from rand import *

#  MPI information
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# extract QA_PARALLEL environment variable
# Turn parallelism on or off.
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

Amap = 1                                 # Serial map.
if PARALLEL:
    Amap = Dmap([1,Np],'c',range(Np))    # Parallel map.

N = 16  # Debug

print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))
print('Distributed matrix size            = (%d)^2 words'%(N))
print('Distributed matrix size (bytes)    = %d'%((N**2)*8))

zero_clock = timer()
b = np.random.rand(N,1) - 0.5   # Create a replicated column vector.
A = rand(N,N,map=Amap)         # Create a distributed matrix.
Z = zeros(N,N,map=Amap)        # Create a distributed matrix.
Talloc = timer()

# Check the distributed z matrix
if PARALLEL:
    print('Local portion of global indices on Pid = %d:'%(Pid))
    print(A.global_ind)
    print('my local length:')
    for i  in range(len(A.falls)):
        print_falls(A.falls[i])
print('my size:')
print(A.shape)

print('Local matrix size (bytes)          = %d'%(np.prod((local(A)).shape)*8))
print('Allocation Time (sec)              = %f'%(Talloc-zero_clock))

print('Assign DMAT A to Z')
Z[:,:] = A
print('Add 1.0 to DMAT A')
A = A + 1.0
print('Check local matrix of both A and Z:')
print('Local portion of A:')
print(local(A))
print('Local portion of Z:')
print(local(Z))

print(' ')
print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')
print(' ')
print(' ')

