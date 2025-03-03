import numpy as np
from timeit import default_timer as timer

# Import gridPython methods.
import pPython as GPC
from ll_map import Dmap,rand,zeros
from ll_dmat import agg,local,size

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
    Amap = Dmap([Np,1],{},range(Np))    # Parallel map.
    Bmap = Dmap([1,Np,1],{},range(Np))    # Parallel map.

N = 8  # Debug
N2 = 2  # Debug

print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))
print('Distributed matrix size            = (%d)^2 words'%(N))
print('Distributed matrix size (bytes)    = %d'%((N**2)*8))

zero_clock = timer()
A = rand(N,N,map=Amap)             # Create a distributed 2D array.
B = zeros(N,N,N2,map=Bmap)         # Create a distributed 3D array.
Talloc = timer()

# Check the distributed z matrix
print('my size:')
print(A.shape)
print(size(A))

print('Local matrix size (bytes)          = %d'%(np.prod((local(A)).shape)*8))
print('Allocation Time (sec)              = %f'%(Talloc-zero_clock))

print('Assign DMAT A to B when A and B are two different distributed arrays with different map.')
# Dmat is not scripable error: 
B[:,:,0] = A
#    B[2:3,2:3,1] = A[2:3,2:3,1]
# B[:,:,1] = A[:,:,1]

GA = agg(A)
GB = agg(B)

print('Check global matrix of both A and B:')
print('global portion of A:')
print(GA[:,:])
print('global portion of B:')
print(GB[:,:,0])

print(' ')
print('2nd plane:')
print('global portion of B:')
print(GB[:,:,1])

print(' ')
print('SUCCESS')
print(' ')
print(' ')

