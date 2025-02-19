import numpy as np
from timeit import default_timer as timer

# Import gridPython methods.
from Dmap import *
import pPython as GPC
from local import *
from print_falls import *
from rand import *
from ones import *

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
Bmap = 1                                 # Serial map.
if PARALLEL:
    Amap = Dmap([1,Np],{},range(Np))    # Parallel map.
    Bmap = Dmap([1,Np],{},range(Np))    # Parallel map.

N = 14  # Debug

print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))
print('Distributed matrix size            = (%d)^2 words'%(N))
print('Distributed matrix size (bytes)    = %d'%((N**2)*8))

zero_clock = timer()
b = np.random.rand(N,1) - 0.5   # Create a replicated column vector.
A = rand(N,N,map=Amap)         # Create a distributed matrix.
B = ones(N,N,map=Amap)         # Create a distributed matrix.
C = ones(N,N,map=Bmap)         # Create a distributed matrix.
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

print('Case 1: A == B, which should be different in most of the elements')
LC = (A == B)
print(local(LC))

print('Case 2: C == B, which should be same in all of the elements')
LD = (C == B)
print(local(LD))

print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')

