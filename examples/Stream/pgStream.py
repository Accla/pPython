import os
import numpy as np
from timeit import default_timer as timer

import pPython as GPC
from pPython.map import Dmap,zeros
from pPython.dmat import local,agg

################################################################################
# This script implements a simple parallel stream benchmark.  It times the
# following operations:
#   COPY          C(i) = A(i)
#   SCALE         B(i) = q*C(i)
#   ADD           C(i) = A(i) + B(i)
#   TRIAD         A(i) = B(i) + q*C(i)
#
# For parallel systems, we impose the constraint that the size of A, B, and C
# should take up at least half of the total system memory.
#
# Parameters:
#   * PARALLEL - Enable the pMatlab library.
#
#   * N - Length of vectors A, B, and C in number of elements.  Can set this
#      value directly or use lgN.
#
#   * lgN - Used to set N, where N = 2^lgN.
#
#   * NTRIALS - Number of trials to perform for each operation.
#
################################################################################
# To run in serial without distributed arrays, set         
#   PARALLEL = 0
# At the Matlab prompt type
#   pStream
# To run in serial with distributed arrays, set         
#   PARALLEL = 1
# At the Matlab prompt type
#   pStream
# To run in parallel with distributed arrays
# at the Matlab prompt type 
#   eval(pRUN('pStream',2,{}))
######################################################

# Identify total number of pPython processes and my rank
Np = GPC.Np
Pid = GPC.Pid

################################################################################
# PARAMETERS (OK to change)

# Turn parallelism on or off
PARALLEL = 1;  # Can be 1 or 0.

# Turn GPU on or off (controlled by launch script)
GPU = 0;  # Can be 1 or 0.
GPU = (int(os.getenv('GPU',str(GPU))) == 1)

# Round-robin assign each Pid to a GPU.
if GPU: 
    # gpudev = cp.cuda.Device(Pid%cp.cuda.runtime.getDeviceCount())
    # embedded in pPython
    gpudev = GPC.gpu_device

# Set number of trials to perform for each operation (controlled by launch script)
NTRIALS = 10;
NTRIALS = int(os.getenv('NTRIALS',str(NTRIALS)))

# Scale data size by number of cpus size (controlled by launch script)
lgN = 30;
lgN = int(os.getenv('LOGN',str(lgN)))
print('Runtime input: GPU = %d, lgN = %d, NTRIALS = %d'%(GPU,lgN,NTRIALS))

#lgN = 20; # Debug.
#N = 2.^lgN;
N = Np * 2 ** lgN

################################################################################
# SETUP

# Pick initial values.
A0 = 1.0; B0 =2.0; C0 = 0.0;  q = np.sqrt(2) - 1;

# Compute final values.
ANm1 = ((2*q + q**2)**(NTRIALS-1))*A0;
AN = ((2*q + q**2)**(NTRIALS))*A0;
BN = q*ANm1;
CN = (1+q)*ANm1;

# Create maps
ABCmap = 1;
SyncMap = 1;
if (PARALLEL):
    # Create map.
    ABCmap = Dmap([1, Np], {}, range(Np))
    SyncMap = Dmap([Np, 1], {}, range(Np))

# Allocate data structures
# Not sure if this is needed with CuPy: if GPU, wait(gpudev), end
tic = timer()

Aloc = local(zeros(1, N, map=ABCmap, gpu=GPU)) + A0
Bloc = local(zeros(1, N, map=ABCmap, gpu=GPU)) + B0
Cloc = local(zeros(1, N, map=ABCmap, gpu=GPU)) + C0

if GPU:
    gpudev.synchronize()

Talloc = timer() - tic;
print('Allocation Time (sec)              = %f'%(Talloc));
Nloc = Cloc.size

# Perform barrier synchronization with agg().
tic = timer()
sync = agg(zeros(Np, 1, map=SyncMap));
Tlaunch = timer() - tic;
print('Launch Time (sec)                  = %f'%(Tlaunch));

################################################################################
# BEGIN PROGRAM
TsumCopy=0.0; TsumScale =0.0; TsumAdd=0.0; TsumTriad=0.0;

for i_trial in range(NTRIALS):   # note, i_trial starts from 0 instead of 1 with Matlab

    # COPY
    if GPU:
        gpudev.synchronize()
    tic = timer()
    Cloc[:,:] = Aloc;
    if GPU:
        gpudev.synchronize()
    TsumCopy = TsumCopy + (timer()-tic);

    # SCALE
    if GPU:
        gpudev.synchronize()
    tic = timer()
    Bloc[:,:] = q*Cloc;
    if GPU:
        gpudev.synchronize()
    TsumScale = TsumScale + (timer()-tic);

    # ADD
    if GPU:
        gpudev.synchronize()
    tic = timer()
    Cloc[:,:] = Aloc + Bloc;
    if GPU:
        gpudev.synchronize()
    TsumAdd = TsumAdd + (timer()-tic);

    # TRIAD
    if GPU:
        gpudev.synchronize()
    tic = timer()
    Aloc[:,:] = Bloc + q*Cloc;
    if GPU:
        gpudev.synchronize()
    TsumTriad = TsumTriad + (timer()-tic);

print('Computation Time (sec)              = %f'%(TsumCopy+TsumScale+TsumAdd+TsumTriad))

# Check results.
Aerr = np.amax(abs(Aloc-AN))
Berr = np.amax(abs(Bloc-BN))
Cerr = np.amax(abs(Cloc-CN))


# Compute performance.
copy_BW = 16*Nloc*NTRIALS / TsumCopy;
scale_BW = 16*Nloc*NTRIALS / TsumScale;
add_BW = 24*Nloc*NTRIALS / TsumAdd;
triad_BW = 24*Nloc*NTRIALS / TsumTriad;

# DISPLAY RESULTS
print('A, B, C errors                     = %f %f %f'%(Aerr, Berr, Cerr))
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

print('Global Copy Bandwidth (MB/sec)     ~ %f'%(Np*copy_BW/1e6))
print('Global Scale Bandwidth (MB/sec)    ~ %f'%(Np*scale_BW/1e6))
print('Global Add Bandwidth (MB/sec)      ~ %f'%(Np*add_BW/1e6))
print('Global Triad Bandwidth (MB/sec)    ~ %f'%(Np*triad_BW/1e6))

