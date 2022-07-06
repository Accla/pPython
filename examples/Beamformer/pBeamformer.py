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
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

# Import PythonMPI methods.
import pPython as GPC
from Dmap import *
from dcomplex import *
from local import *
from size import *
from rand import *
from global_ind import *
from agg import *
from put_local import *

from beamformer_vectors import *

#  MPI information
comm = GPC.comm
Np = GPC.comm_size
Pid = GPC.my_rank

# Set number of time snapshots, sensors, beams and frequencies.
Nt = 600 
Ns = 90  
Nb = 40 
Nf = 100

Nt = 100 # Debug.

PARALLEL = 0    # Set control flag.
Xmap = 1        # Create serial map.
if (PARALLEL):
    Xmap = Dmap([1,1,Np],{},range(Np))  # Create parallel map.

# ALLOCATE PARALLEL DATA STRUCTURES ---------------------
X0 = zeros(Nt,Nb,Nf,map=Xmap)   # Source array.
X1 = np.sqrt(Ns)*dcomplex(rand(Nt,Ns,Nf,map=Xmap),rand(Nt,Ns,Nf,map=Xmap))  # Sensor input.
X2 = zeros(Nt,Nb,Nf,map=Xmap)   # Beamformed output.
X3 = zeros(Nt,Nb,Np,map=Xmap)   # Intermediate sum.
#CB global_ind() returns a list, Should make it return a numpy array?
myI_f = np.array(global_ind(X1,2))   # Get local indices.
# Get local parts of arrays.
X0loc = local(X0)  
X1loc = local(X1)  
X2loc = local(X2)

# CREATE STEERING VECTORS ---------------------

# Pick an arbitrary set of frequencies.
freq0 = 10  
frequencies = freq0 + np.array(range(Nf))
# Create local steering vector by passing local frequencies.
myV = np.squeeze(beamformer_vectors(Ns,Nb,frequencies[myI_f]))

# STEP 0: Insert targets ---------------------

# Insert two targets at different angles.
# Subtract one to match with the same index location used by Matlab
X0loc[:,round(0.25*Nb)-1,:] = 1  
X0loc[:,round(0.5*Nb)-1,:] = 1

# STEP 1: CREATE SYNTHETIC DATA. ---------------------
tic = timer()               # Start timer.
for i_t in range(Nt):       # Loop over time snapshots.
    for i_f in range(np.prod(size(myI_f))):  # Loop over local frequencies.
        # Convert from beams to sensors.
        X1loc[i_t,:,i_f] = X1loc[i_t,:,i_f] + np.dot(np.squeeze(myV[:,:,i_f]),np.transpose(np.squeeze(X0loc[i_t,:,i_f])))

# STEP 2: BEAMFORM AND SAVE DATA. ---------------------

for i_t in range(Nt):      # Loop over time snapshots.
    for i_f in range(np.prod(size(myI_f))):  # Loop over local frequencies.
        # Convert from sensors back to beams.
        # Matlab automatically transpose vector as 1xN but not with Python, whcih needs explicit transpose()
        X2loc[i_t,:,i_f] = np.abs(np.dot(np.squeeze(X1loc[i_t,:,i_f]).T, np.squeeze(myV[:,:,i_f])))**2

for i_f in range(np.prod(size(myI_f))):  # Loop over frequencies.
    X_i_f = np.squeeze(X2loc[:,:,i_f])   # Get a matrix of data.
    filename = 'dat/pBeamformer_freq.'+str(myI_f[i_f])+'.npy'
    np.save(filename, X_i_f)             # .npy extension is added if not given

Tcompute = timer()-tic
print('Compute Time (sec)                 = %f'%(Tcompute))

# STEP 3: SUM ACROSS FREQUNCY. ---------------------

# Add the missing axis for the broadcast ops in put_local() when np.sum() reduces X2loc dimension
X3 = put_local(X3,np.sum(X2loc,2)[:,:,np.newaxis])   # Sum local part and put into X3.
tic = timer()                        # Start timer.
x3 = np.squeeze(np.sum(agg(X3),2))   # Aggregate X3 on leader and complte sum.

Tcomm = timer() - tic
print('Launch+Comm Time (sec)             = %f'%(Tcomm))

# STEP 4: Finalize and display. ---------------------
# Display on leader.
if (Pid == 0):
    pstr = str(PARALLEL)
    npstr = str(Np)
    plt.imshow(np.abs(np.squeeze(X0loc[:,:,0])), origin = 'lower')
    filename = 'beamformer_x0_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

    plt.imshow(np.abs(np.squeeze(X1loc[:,:,0])), origin = 'lower')
    filename = 'beamformer_x1_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

    plt.imshow(np.abs(np.squeeze(X2loc[:,:,0])), origin = 'lower')
    filename = 'beamformer_x2_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

    plt.imshow(x3, origin = 'lower')
    filename = 'beamformer_x3_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

print('')
print('SUCCESS')
print('')
print('')

