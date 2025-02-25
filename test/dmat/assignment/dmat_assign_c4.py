import numpy as np
from timeit import default_timer as timer

# Import gridPython methods.
import pPython as GPC
from pPython.map import Dmap,rand,zeros
from pPython.dmat import agg,local

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
    Amap = Dmap([Np,1,1,1],{},range(Np))    # Parallel map.
    Bmap = Dmap([1,Np,1,1],{},range(Np))    # Parallel map.

N = 8  # Debug
N2 = 2  # Debug

print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))
print('Distributed matrix size            = (%d)^2 words'%(N))
print('Distributed matrix size (bytes)    = %d'%((N**2)*8))

zero_clock = timer()
A = rand(N,N,N2,N2,map=Amap)         # Create a distributed matrix.
B = zeros(N,N,N2,N2,map=Bmap)         # Create a distributed matrix.
Talloc = timer()

# Check the distributed z matrix
print('my size:')
print(A.shape)

print('Local matrix size (bytes)          = %d'%(np.prod((local(A)).shape)*8))
print('Allocation Time (sec)              = %f'%(Talloc-zero_clock))

print('Assign DMAT A to B when A and B are two different distributed arrays with different map.')
B[:,:,:,:] = A

GA = agg(A)
GB = agg(B)

if Pid == 0:
    # compare two global arrays
    GC = GA - GB
print('Check global matrix of both A and B:')
for m1 in range(N2):
    for l1 in range(N2):
        print('--- For plane with (:,:,M,L) where M = %d, L = %d'%(m1,l1))
        print('global portion of A:')
        print(GA[:,:,m1,l1])
        print('global portion of B:')
        print(GB[:,:,m1,l1])
        if Pid == 0:
            print('global portion of C:')
            print(GC[:,:,m1,l1])
            print(' ')

print(' ')
print('SUCCESS')
print(' ')
print(' ')

