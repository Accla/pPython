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

import pPython as GPC
from Dmap import *
from zeros import *
from ones import *
from synch import *
from find import *
from global_ind import *
from local import *
from put_local import *
from agg import *
from BcastMsg import *

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

# PARALLEL = 1  # Set control flag.
CHECK = 1     # Check answer with serial calculation.

DEBUG = 1

# Set image size (scaled by numlabs), filter size and blur.
Nx = 2**11*Np;  Ny = 1024; Nk = 2**5;  Nblur = 2
Nx = 2**9*Np;  # Debug 
# Nx = 2**6*Np; Nk = 2**3   # Fine Debug.

Zmap = 1      # Create serial map.
if (PARALLEL):
    Zmap = Dmap([Np,1],{},range(Np),[Nk,0])  # Create parallel map with overlap.

# Create starting image and working images..
if (CHECK):
    im = zeros(Nx,Ny)

Z = zeros(Nx,Ny,map=Zmap) + 1.e-4   # Create 2D distributed array.
tag = 1004
if Pid == 0:
    # find the global index and broadcast them
    [ii,jj] = find(scipy.sparse.random(Nx, Ny, density=1.e-4))  # Create non-zeros.
    [ii,jj] = BcastMsg(0,tag,ii,jj)
else:
    ii = jj = None
    [ii,jj] = BcastMsg(0,tag,ii,jj)

if DEBUG:
    print('ii.shape = ',end='')
    print(ii.shape)
    print('jj.shape = ',end='')
    print(jj.shape)
    print('type(ii) = ',end='')
    print(type(ii))
    print('type(jj) = ',end='')
    print(type(jj))

ii = np.array(ii)
jj = np.array(jj)

if DEBUG:
    print('Matlab numel(ii) equivalent: np.prod(size(ii))')
    print(np.prod(size(ii)))
    print('Before Z[ii[i],jj[i]]=1 loop')
    # print('local(Z)')
    # print(local(Z))

#old: myI = np.array(global_ind(Z,0))  # Get local i indices.
#old: myJ = np.array(global_ind(Z,1))  # Get local j indices.
myI = global_ind(Z,0)[0]  # Get local i indices.
myJ = global_ind(Z,1)[0]  # Get local j indices.
if DEBUG:
    print('myI: my global index in 0-direction:')
    print(myI)

for i in range(np.prod(size(ii))):
    if DEBUG>1 and i<5:
        print('i=%d, ii=%d, jj=%d'%(i,ii[i],jj[i]))
    Z[ii[i],jj[i]]=1    # Insert non-zeros.
if DEBUG:
    print('After Z[ii[i],jj[i]]=1 loop')
    # print('local(Z)')
    # print(local(Z))
    Zlocal = local(Z)
    indx = np.argwhere(Zlocal >=  1) 
    print('Local array where Z[i,j] = 1 applied')
    print(indx)

if DEBUG>3:
    exit()


if DEBUG:
    print('myI.shape')
    print(myI.shape)
    print('myJ.shape')
    print(myJ.shape)

Z0 = Z                 # They are stored in two different memory locations
if (CHECK):
    im = zeros(Nx,Ny) + 1.e-4
    for i in range(np.prod(size(ii))):
        im[ii[i],jj[i]]=1

    # im should be exactly the same as agg(Z)
    Zagg = agg(Z)
    if Pid==0:
        diff = Zagg - im
        maxdiff = np.amax(diff)
        print('Max. difference in Zagg - im: %f'%(maxdiff))

kernel = ones(Nk,Nk)  # Create kernel.

tic = timer()
Z = synch(Z)          # Synchronize boundary conditions.
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
    print('local(Z).shape')
    tmp = local(Z)
    print(tmp.shape)
    print('im.shape = ',end='')
    print(im.shape)
    print('myI[-1] = ',end='')
    print(myI[-1])
    print('im[myI,myJ].shape')
    # tmp1 = im[myI,myJ]
    # tmp1 = im[myI]    # select rows given by myI with all columns
    # tmp2 = tmp[:,myJ] # select columns given by myJ with all rows
    # print(tmp.shape)

    maxDiff = np.amax(np.abs(local(Z) - im[myI][:,myJ])) 
    print('Max error                        = %f'%(maxDiff))

totalOps = 2*Nblur*Nk*Nk*Nx*Ny # Number of operations.

# Print compute performance.
gigaflops = totalOps / Tcompute / 1.e9
print('Performance (Gigaflops)            = %f'%(gigaflops))

# Save Zagg for plotting interactively later
pstr = str(PARALLEL)
npstr = str(Np)
Zagg = agg(Z)

# Display on leader.
if (Pid == 0):
    fig, ax = plt.subplots()
    ax.plot(ii, jj, 'o')
    ax.set_xlim(0, Nx)
    ax.set_ylim(0, Ny)
    ax.set(aspect=1)
    plt.show()
    filename = 'blurimage_random_'+pstr+'_'+npstr
    # plt.savefig(filename+'.png')
    # np.savez('ij_location_'+pstr+'_'+npstr+'.npz',ii=ii,jj=jj,Nx=Nx,Ny=Ny)

    fig, ax = plt.subplots()
    plt.imshow(np.rot90(local(Z),1), origin = 'lower')
    plt.show()
    filename = 'blurimage_local_'+pstr+'_'+npstr
    # plt.savefig(filename+'.png')
    # tmp = np.rot90(local(Z),1)
    # np.save('blurimage_data_'+pstr+'_'+npstr+'.npy',tmp)

    # tmp2 = np.rot90(Zagg,1)
    # np.save('whole_plot_for_blurimage_'+pstr+'_'+npstr+'.npy',tmp2)

np.savez('ij_location_'+pstr+'_'+npstr+'-'+str(Pid)+'.npz',ii=ii,jj=jj,Nx=Nx,Ny=Ny)
print('')
print('SUCCESS')
print('')
print('')

