import numpy as np
import os
from timeit import default_timer as timer

# from pPython_all import *
import pPython as GPC
from Dmap import *
from local import *
from zeros import *
from agg import *

"""
This script implements a simple parallel stream benchmark.  It times the
following operations:
   COPY          C(i) = A(i)
   SCALE         B(i) = q*C(i)
   ADD           C(i) = A(i) + B(i)
   TRIAD         A(i) = B(i) + q*C(i)

For parallel systems, we impose the constraint that the size of A, B, and C
should take up at least half of the total system memory.

Parameters:
   * PARALLEL - Enable the pMatlab library.

   * N - Length of vectors A, B, and C in number of elements.  Can set this
      value directly or use lgN.

   * lgN - Used to set N, where N = 2^lgN.

   * NTRIALS - Number of trials to perform for each operation.


To run in serial without distributed arrays, set
   PARALLEL = 0
At the Matlab prompt type
   pStream
To run in serial with distributed arrays, set
   PARALLEL = 1
At the Matlab prompt type
   pStream
To run in parallel with distributed arrays
at the Matlab prompt type
   eval(pRUN('pStream',2,{}))

"""

# Create communicator.
comm = GPC.comm
Np = GPC.comm_size
Pid = GPC.my_rank

# Print rank.
print('size: %d'%(Np))
print('my_rank: %d'%(Pid))

# PARAMETERS (OK to change)
# Turn parallelism on or off
PARALLEL = 1  # Can be 1 or 0.

# Set number of trials to perform for each operation
NTRIALS = 10

# Scale data size by number of cpus size
lgN = 25
lgN = 20 # Debug.
N = np.power(2,lgN)
#N = math.floor(1.6 * np.power(2,lgN))  # Largest on 1 TX-2500 node.
#N = Np * np.power(2,lgN)
#N = Np * math.floor(1.6 * np.power(2,lgN))   # Largest on Np TX-2500 nodes.

# SETUP

# Pick initial values.
A0 = 1.0 
B0 = 2.0 
C0 = 0.0  
q = 3.14

# Compute final values.
ANm1 = (np.power((2*q + q**2),(NTRIALS-1)))*A0
AN = (np.power((2*q + q**2),NTRIALS))*A0
BN = q*ANm1
CN = (1+q)*ANm1

# Create maps
ABCmap = 1
SyncMap = 1
if (PARALLEL):
    # Create map.
    ABCmap  = Dmap([1,Np], {},range(Np))
    SyncMap = Dmap([Np,1], {},range(Np))

# Allocate data structures
tic = timer()
Aloc = local(zeros(1, N, map=ABCmap)) + A0
Bloc = local(zeros(1, N, map=ABCmap)) + B0
Cloc = local(zeros(1, N, map=ABCmap)) + C0

Talloc = timer()
print('Allocation Time (sec)              = %f'%(Talloc - tic))

Nloc = Cloc.size

# Perform barrier synchronization with agg().
#!!!!! DO WE NEED THIS?
tic
sync = agg(zeros(Np, 1, map=SyncMap))
Tlaunch = timer()
print('Launch  Time (sec)                 = %f'%(Tlaunch - Talloc))

#
# BEGIN PROGRAM
TsumCopy=0.0 
TsumScale=0.0 
TsumAdd=0.0 
TsumTriad=0.0

for i_trial in range(NTRIALS):

    # COPY
    tic = timer()
    Cloc[:,:] = Aloc
    TsumCopy = TsumCopy + (timer() - tic)

    # SCALE
    tic = timer()
    Bloc[:,:] = q*Cloc
    TsumScale = TsumScale + (timer() - tic)

    # ADD
    tic = timer()
    Cloc[:,:] = Aloc + Bloc
    TsumAdd = TsumAdd + (timer() - tic)

    # TRIAD
    tic = timer()
    Aloc[:,:] = Bloc + q*Cloc
    TsumTriad = TsumTriad + (timer() - tic)

# Check results.
Aerr = np.amax(abs(Aloc-AN))
Berr = np.amax(abs(Bloc-BN))
Cerr = np.amax(abs(Cloc-CN))


# Compute performance.
copy_BW  = 16*Nloc*NTRIALS / TsumCopy
scale_BW = 16*Nloc*NTRIALS / TsumScale
add_BW   = 24*Nloc*NTRIALS / TsumAdd
triad_BW = 24*Nloc*NTRIALS / TsumTriad

# printLAY RESULTS
print('A, B, C errors                     = %f,%f,%f'%(Aerr,Berr,Cerr))
print('Np                                 = %d'%(Np))
print('Pid                                = %d'%(Pid))
print('Global Array size (elem)           = %d'%(N))
print('Global Array size (bytes)          = %d'%(N*8))
print('Global memory required (bytes)     = %d'%(N*24))
print('Local Array size (elem)            = %d'%(Nloc))
print('Local Array size (bytes)           = %d'%(Nloc*8))
print('Local memory required (bytes)      = %d'%(Nloc*24))
print('Number of trials                   = %d'%(NTRIALS))
print('Local Copy Bandwidth (MB/sec)      = %f'%(copy_BW/1e6))
print('Local Scale Bandwidth (MB/sec)     = %f'%(scale_BW/1e6))
print('Local Add Bandwidth (MB/sec)       = %f'%(add_BW/1e6))
print('Local Triad Bandwidth (MB/sec)     = %f'%(triad_BW/1e6))
print('Global Copy Bandwidth (MB/sec)     ~ %d'%(Np*copy_BW/1e6))
print('Global Scale Bandwidth (MB/sec)    ~ %f'%(Np*scale_BW/1e6))
print('Global Add Bandwidth (MB/sec)      ~ %f'%(Np*add_BW/1e6))
print('Global Triad Bandwidth (MB/sec)    ~ %f'%(Np*triad_BW/1e6))

print('')
print('')
print('')
print('SUCCESS')
print('')
print('')
print('')

