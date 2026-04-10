"""
pBeamformer is an example of a simple parallel beamformer.
The first part generates synthetic data and then passes the data into to 
the second half which processes the data.
To run in serial without distributed arrays, set
    PARALLEL = 0
At the Python prompt type
    pBeamformer
To run in serial with distributed arrays, set
    PARALLEL = 1
At the Python prompt type
    pBeamformer
To run in parallel with distributed arrays at the Python prompt type
    pRUN('pBeamformer',2,{}))
    
Python version: Dr. Chansup Byun
"""
# import numpy as np
from numpy import abs,array,dot,newaxis,save,sqrt,squeeze,sum,transpose
from timeit import default_timer as timer
import matplotlib.pyplot as plt

# Import PythonMPI methods.
import pPython as GPC
from pPython.map import Dmap,rand,zeros
from pPython.dmat import dcomplex,local,global_ind,agg,put_local

# Import auxiliary module
from beamformer_vectors import *

#  MPI information
Np = GPC.Np
Pid = GPC.Pid

# Set number of time snapshots, sensors, beams and frequencies.
Nt = 50   # number of different time snapshots
Ns = 90   # number of sensor elements
Nb = 40   # number of beams 
Nf = 100  # number of frequencies

# Nt = 600 # Performance
Nt = 100 # Performance
Nb = 80  # Plot 

# For BOOK plots
# Nf = 256
# For BOOK timing
# Nf = 512

# For BOOK texts
Nt = 50
Nb = 40

# J.K. parameter for GPU benchmark
Nt = 600; Ns = 90;  Nb = 40; Nf = 100;
Nt = int(16*Nt); Ns = int(256*Ns);  Nb = int(256*Nb); Nf = int(Np*Nf/25);

SAVEFILES = 0

PARALLEL = 1    # Set control flag.
Xmap = 1        # Create serial map.
if (PARALLEL):
    Xmap = Dmap([1,1,Np],{},range(Np))  # Create parallel map.

# ALLOCATE PARALLEL DATA STRUCTURES ---------------------
X0 = zeros(Nt,Nb,Nf,map=Xmap)   # Source array.
X1 = sqrt(Ns)*dcomplex(rand(Nt,Ns,Nf,map=Xmap),rand(Nt,Ns,Nf,map=Xmap))  # Sensor input.
X2 = zeros(Nt,Nb,Nf,map=Xmap)   # Beamformed output.
X3 = zeros(Nt,Nb,Np,map=Xmap)   # Intermediate sum.

myI_f = global_ind(X1,2)[0]   # Get local indices.
# Get local parts of arrays.
X0loc = local(X0)  
X1loc = local(X1)  
X2loc = local(X2)

# CREATE STEERING VECTORS ---------------------

# Pick an arbitrary set of frequencies.
freq0 = 10  
frequencies = freq0 + array(range(Nf))
# Create local steering vector by passing local frequencies.
myV = squeeze(beamformer_vectors(Ns,Nb,frequencies[myI_f]))

# STEP 0: Insert targets ---------------------

# Insert two targets at different angles in X0.
# Subtract one to match with the same index location used by Matlab
X0loc[:,round(0.25*Nb)-1,:] = 1  
X0loc[:,round(0.5*Nb)-1,:] = 1

# STEP 1: CREATE SYNTHETIC DATA. ---------------------
tic = timer()               # Start timer.
# Convert from beams to sensors.
for i_f in range(myI_f.size):  # Loop over local frequencies.
    # X1loc[:, :, i_f] = X1loc[:, :, i_f] + dot(squeeze(X0loc[:, :, i_f]), squeeze(myV[:, :, i_f]).T)
    X1loc[:, :, i_f] += dot(squeeze(X0loc[:, :, i_f]), squeeze(myV[:, :, i_f]).T)

# STEP 2: BEAMFORM AND SAVE DATA. ---------------------

# Convert from sensors back to beams.
for i_f in range(myI_f.size):  # Loop over local frequencies.
    X2loc[:, :, i_f] = abs(dot(squeeze(X1loc[:, :, i_f]), squeeze(myV[:, :, i_f])))**2

if SAVEFILES:
    for i_f in range(myI_f.size):  # Loop over frequencies.
        X_i_f = squeeze(X2loc[:,:,i_f])   # Get a matrix of data.
        filename = 'dat/pBeamformer_freq.'+str(myI_f[i_f])+'.npy'
        save(filename, X_i_f)             # .npy extension is added if not given

Tcompute = timer()-tic
print('Compute Time (sec)                 = %f'%(Tcompute))
print('Compute GFlops                     = %f'%(2*8*Nt*Ns*Nb*Nf/Tcompute/1e9))

# STEP 3: SUM ACROSS FREQUNCY. ---------------------

# Add the missing axis for the broadcast ops in put_local() when sum() reduces X2loc dimension
X3 = put_local(X3,sum(X2loc,2)[:,:,newaxis])   # Sum local part and put into X3.
tic = timer()                        # Start timer.
x3 = squeeze(sum(agg(X3),2))   # Aggregate X3 on leader and complte sum.

Tcomm = timer() - tic
print('Launch+Comm Time (sec)             = %f'%(Tcomm))

# STEP 4: Finalize and display. ---------------------
# Display on leader.
DISPLAY_PLOT=0
if (Pid == 0) and (DISPLAY_PLOT==1):
    pstr = str(PARALLEL)
    npstr = str(Np)
    
    img0 = plt.imshow(abs(squeeze(X0loc[:,:,0])), origin = 'upper')
    # img0.set_cmap('bwr')
    filename = 'beamformer_x0_'+pstr+'_'+npstr+'.png'
    plt.savefig(filename)

    img1 = plt.imshow(abs(squeeze(X1loc[:,:,0])), origin = 'upper')
    # img1.set_cmap('bwr')
    filename = 'beamformer_x1_'+pstr+'_'+npstr+'.png'
    plt.savefig(filename)

    img2 = plt.imshow(abs(squeeze(X2loc[:,:,0])), origin = 'upper')
    # img2.set_cmap('bwr')
    filename = 'beamformer_x2_'+pstr+'_'+npstr+'.png'
    plt.savefig(filename)

    img3 = plt.imshow(x3, origin = 'upper')
    img3.set_cmap('bwr')
    filename = 'beamformer_x3_'+pstr+'_'+npstr+'.png'
    plt.savefig(filename)

    plt.show()

print('')
print('SUCCESS')
print('')

"""
v1=[X0,X0loc,X1,X1loc,X2,X2loc,X3,x3,myI_f,myV]
v2=['X0','X0loc','X1','X1loc','X2','X2loc','X3','x3','myI_f','myV']
whosPy(v1,v2)
"""

