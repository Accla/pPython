"""
This script implements a basic image convolution
across multiple processors.  It illustrates how to
use overlaping boundaries.
To run in serial without distributed arrays, set
    PARALLEL = 0
At the Python prompt type
    pBlurimage
To run in serial with distributed arrays, set
    PARALLEL = 1
At the Python prompt type
    pBlurimage
To run in parallel with distributed arrays
at the Python prompt type
    pRUN('pBlurimage',2,{})
"""
from timeit import default_timer as timer
import numpy as np
import scipy.signal
import scipy.sparse
import matplotlib.pyplot as plt

import GridPython as GPC
from GridMap import *
from zeros import *
from ones import *
from synch import *
from find import *
from global_ind import *
from local import *
from put_local import *

#  MPI information
comm = GPC.comm
Np = GPC.comm_size
Pid = GPC.my_rank

# Set image size (scaled by numlabs), filter size and blur.
Nx = 2**11*Np;  Ny = 1024; Nk = 2**5;  Nblur = 2
# Nx = 2**9*Np;  # Debug 

PARALLEL = 1   # Set control flag.
CHECK = 1      # Check answer with serial calculation.

Zmap = 1       # Create serial map.
if (PARALLEL):
    Zmap = GridMap([Np,1],{},range(Np),[Nk,0])  # Create parallel map with overlap.

# Create starting image and working images..
if (CHECK):
    im = zeros(Nx,Ny)

Z = zeros(Nx,Ny,dmap=Zmap) + 1.e-4   # Create 2D distributed array.
[ii,jj] = find(scipy.sparse.random(Nx, Ny, density=1.e-4))  # Create non-zeros.
ii = np.array(ii) # Convert as Numpy array for array indexing ops
jj = np.array(jj) # Convert as Numpy array for array indexing ops
for i in range(np.prod(size(ii))):
    Z[ii[i],jj[i]]=1             # Insert non-zeros.

myI = np.array(global_ind(Z,0))  # Get local i indices.
myJ = np.array(global_ind(Z,1))  # Get local j indices.

Z0 = Z         # They are stored in two different memory locations

if (CHECK):
    im = zeros(Nx,Ny) + 1.e-4
    for i in range(np.prod(size(ii))):
        im[ii[i],jj[i]]=1

kernel = ones(Nk,Nk)  # Create kernel.

tic = timer()
Z = synch(Z)   # Synchronize boundary conditions.
Tlaunch = timer() - tic
print('Launch Time (sec)                  = %f'%(Tlaunch))

tic = timer()  # Set start time.

for iblur in range(Nblur):    # Loop over each blur.
    Zloc = local(Z)           # Get local data.
    Zloc[0:-Nk+1,0:-Nk+1] = scipy.signal.convolve(Zloc,kernel,'valid')    # Perform covolution.
    Z = put_local(Z,Zloc)     # Put local back.
    Z = synch(Z)              # Copy overlaping boundaries.
    if (CHECK):
        im[0:-Nk+1,0:-Nk+1] = scipy.signal.convolve(im,kernel,'valid')

Tcompute = timer() - tic      # Get blur time.
print('Compute Time (sec)                 = %f'%(Tcompute))

# Compare results.
if (CHECK):
    maxDiff = np.amax(np.abs(local(Z) - im[myI][:,myJ])) 
    print('Max error                        = %f'%(maxDiff))

totalOps = 2*Nblur*Nk*Nk*Nx*Ny # Number of operations.

# Print compute performance.
gigaflops = totalOps / Tcompute / 1.e9
print('Performance (Gigaflops)            = %f'%(gigaflops))

# Display on leader.
if (Pid == 0):
    pstr = str(PARALLEL)
    npstr = str(Np)
    fig, ax = plt.subplots()
    ax.plot(ii, jj, 'o')
    ax.set_xlim(0, Nx)
    ax.set_ylim(0, Ny)
    ax.set(aspect=1)
    plt.show()

    fig, ax = plt.subplots()
    plt.imshow(np.rot90(local(Z),1), origin = 'lower')
    plt.show()

print('')
print('SUCCESS')
print('')
print('')

