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
# debugging
from scipy.io import loadmat

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

DEBUG = 1

# Set number of time snapshots, sensors, beams and frequencies.
Nt = 600 
Ns = 90  
Nb = 40 
Nf = 100

Nt = 100 # Debug.

# PARALLEL = 1  # Set control flag.
Xmap = 1        # Create serial map.
if (PARALLEL):
    Xmap = Dmap([1,1,Np],{},range(Np))  # Create parallel map.

# ALLOCATE PARALLEL DATA STRUCTURES ---------------------
print('Xmap:')
print(Xmap)

X0 = zeros(Nt,Nb,Nf,map=Xmap)   # Source array.
X1 = np.sqrt(Ns)*dcomplex(rand(Nt,Ns,Nf,map=Xmap),rand(Nt,Ns,Nf,map=Xmap))  # Sensor input.
print('X1global.shape')
#
# Load from the pMatlab saved data
#
m_r_path = '/home/gridsan/CH21778/examples/pMATLAB_book/Beamformer/'
m_r_file = m_r_path+'X1global.mat'
# Load the results
mat = loadmat(m_r_file)
X1global = mat['X1global']
print('X1global.shape')
print(X1global.shape)
print('X1global datatype:')
print(X1global[0,0,0])

if not PARALLEL:
    print('Not a parallel run, update X1 with X1global from pMatlab')
    X1 = X1global
else:
    if Np == 1:
        print('A parallel run with Np=1, update X1.local with X1global from pMatlab')
        X1.local = X1global
    else:
        print('A parallel run with Np>1, update X1.local with the corresponding sub-matrix of X1global from pMatlab')
        mg = global_ind(X1)   # Get local indices.
        print('X1.local.shape')
        print(X1.local.shape)
        tmp1 = X1global[mg[0][0]:mg[0][-1]+1,mg[1][0]:mg[1][-1]+1,mg[2][0]:mg[2][-1]+1]
        print('X1global[mg[0],mg[1],mg[2]].shape')
        print(tmp1.shape)
        print('X1global[0,0,0]')
        print(tmp1[0,0,0])
        X1 = put_local(X1,tmp1)
        #
        # Confirm if X1global complex array is correctly distributed 
        X1newg = agg(X1)
        print('X1 new global shape: %s'%(str(X1newg.shape)))
        print('the following should match with X1global[0,0,0]')
        print(X1newg[0,0,0])
        diff = X1global[0,0,0] - X1newg[0,0,0]
        if np.abs(diff) > 0:
            print(np.abs(diff))
            print('Incorrect agg() results with complex matrix')

# sync among the processes
sync = agg(zeros(1,1,Np, map=Xmap))


X2 = zeros(Nt,Nb,Nf,map=Xmap)  # Beamformed output.
X3 = zeros(Nt,Nb,Np,map=Xmap)  # Intermediate sum.
#CB global_ind() returns a list, Should make it return a numpy array?
# old: myI_f = np.array(global_ind(X1,2))   # Get local indices.
myI_f = global_ind(X1,2)[0]   # Get local indices.
# Get local parts of arrays.
X0loc = local(X0)  
X1loc = local(X1)  
X2loc = local(X2)

print('X1loc[:,0,:]')
print(X1loc[:,0,:])

# CREATE STEERING VECTORS ---------------------

# Pick an arbitrary set of frequencies.
freq0 = 10  
frequencies = freq0 + np.array(range(Nf))
# Create local steering vector by passing local frequencies.
print('frequencies[myI_f]')
print(frequencies[myI_f])
myV = np.squeeze(beamformer_vectors(Ns,Nb,frequencies[myI_f]))
print('myI_f')
print(myI_f)
np.save('myV.npy', myV)    # .npy extension is added if not given

# STEP 0: Insert targets ---------------------

# Insert two targets at different angles.
print('round(0.25*Nb)')
print(round(0.25*Nb))
#CB subtract by one to match with the same index location used by Matlab
X0loc[:,round(0.25*Nb)-1,:] = 1  
X0loc[:,round(0.5*Nb)-1,:] = 1


# STEP 1: CREATE SYNTHETIC DATA. ---------------------
tic = timer()              # Start timer.

if DEBUG:
    print('myI_f')
    print(myI_f)

    print('myV.shape')
    print(myV.shape)
    print('myV[0,:,0]')
    print(myV[0,:,0])
    print('X1loc[0,:,0]')
    print(X1loc[0,:,0])

if DEBUG:
    print('X0loc.shape')
    print(X0loc.shape)
for i_t in range(Nt):      # Loop over time snapshots.
    for i_f in range(np.prod(size(myI_f))):  # Loop over local frequencies.
        # Convert from beams to sensors.
        # X1loc[i_t,:,i_f] = X1loc[i_t,:,i_f].' + (squeeze(myV(:,:,i_f]) * squeeze(X0loc[i_t,:,i_f]).')
        if DEBUG and (i_t==0 and i_f==0):
            print('X1loc.shape')
            print(X1loc.shape)
            tmp2 = X1loc[i_t,:,i_f]
            print('X1loc[i_t,:,i_f].shape')
            print(tmp2.shape)
            tmp3 = np.transpose(np.squeeze(X0loc[i_t,:,i_f]))
            print('=== shape of np.transpose(np.squeeze(X0loc[i_t,:,i_f])) ===')
            print(tmp3.shape)

            # tmp1 = (np.dot(np.squeeze(myV[:,:,i_f]),np.squeeze(np.transpose(X0loc[i_t,:,i_f]))))
            # tmp1 = (np.squeeze(myV[:,:,i_f])*np.transpose(np.squeeze(X0loc[i_t,:,i_f])))
            tmp1 = np.dot(np.squeeze(myV[:,:,i_f]),np.transpose(np.squeeze(X0loc[i_t,:,i_f])))
            print('(np.squeeze(myV[:,:,i_f])*np.squeeze(X0loc[i_t,:,i_f])).shape')
            print(tmp1.shape)
        X1loc[i_t,:,i_f] = X1loc[i_t,:,i_f] + np.dot(np.squeeze(myV[:,:,i_f]),np.transpose(np.squeeze(X0loc[i_t,:,i_f])))
        if DEBUG > 2:
            if i_t==0 and i_f==0:
                print('X1loc[i_t,:,i_f]')
                print(X1loc[i_t,:,i_f])
                print(X1loc[i_t,:,i_f].shape)

# STEP 2: BEAMFORM AND SAVE DATA. ---------------------

for i_t in range(Nt):      # Loop over time snapshots.
    for i_f in range(np.prod(size(myI_f))):  # Loop over local frequencies.
        # Convert from sensors back to beams.
        if DEBUG > 2:
            print('X2loc.shape')
            print(X2loc.shape)
            tmp2 = X1loc[i_t,:,i_f]
            print('X1loc[i_t,:,i_f].shape')
            print(tmp2.shape)
            tmp1 = np.squeeze(X1loc[i_t,:,i_f])
            tmp2 = np.squeeze(myV[:,:,i_f])
            tmp3 = np.dot(np.transpose(np.squeeze(X1loc[i_t,:,i_f])), np.squeeze(myV[:,:,i_f]))
            print('np.squeeze(X1loc[i_t,:,i_f]).shape')
            print(tmp1.shape)
            print('np.squeeze(myV[:,:,i_f]).shape')
            print(tmp2.shape)
            print('np.dot(np.transpose(np.squeeze(X1loc[i_t,:,i_f])), np.squeeze(myV[:,:,i_f])).shape')
            print(tmp3.shape)
            print('size(tmp3)')
            print(size(tmp3))
        # Matlab automatically transpose vector as 1xN but not with Python, whcih needs explicit transpose()
        # ValueError: could not broadcast input array from shape (40,) into shape (40,1)
        # X2loc[i_t,:,i_f] = np.abs(np.dot(np.transpose(np.squeeze(X1loc[i_t,:,i_f])), np.squeeze(myV[:,:,i_f])))**2
        # 
        # Somehow X2loc has different behavior depending on distributed array or not.
        # i.e., Xmap is Dmap or not
        tmp = np.abs(np.dot(np.transpose(np.squeeze(X1loc[i_t,:,i_f])), np.squeeze(myV[:,:,i_f])))**2
        if i_t==0 and i_f==0:
            print('np.abs(np.dot(np.transpose(np.squeeze(X1loc[i_t,:,i_f])), np.squeeze(myV[:,:,i_f])))**2 .shape')
            print(tmp.shape)
            print(' . . .  . now assign to X2loc[i_t,:,i_f] . . . ')
        # if PARALLEL:
        X2loc[i_t,:,i_f] = tmp
        # else:
        #     X2loc[i_t,:,i_f] = np.reshape(tmp,(len(tmp),1))

for i_f in range(np.prod(size(myI_f))):  # Loop over frequencies.
    X_i_f = np.squeeze(X2loc[:,:,i_f])   # Get a matrix of data.
    filename = 'dat/pBeamformer_freq.'+str(myI_f[i_f])+'.npy'
    np.save(filename, X_i_f)    # .npy extension is added if not given
    #To load: X_i_f = np.load(filename)

Tcompute = timer()-tic
print('Compute Time (sec)                 = %f'%(Tcompute))

# STEP 3: SUM ACROSS FREQUNCY. ---------------------

print('X2loc.shape')
print(X2loc.shape)
#CB:  np.sum(X2loc,2) returns 2-D array. So add the 3rd axis to make the broadcast work in put_local() 
X3 = put_local(X3,np.sum(X2loc,2)[:,:,np.newaxis])   # Sum local part and put into X3.
if DEBUG:
    tmp = np.sum(X2loc,2)
    print('np.sum(X2loc,2) .shape')
    print(tmp.shape)
tic = timer()                        # Start timer.
X3agg = agg(X3)
print('X3agg.shape')
print(X3agg.shape)
x3 = np.squeeze(np.sum(agg(X3),2))   # Aggregate X3 on leader and complte sum.
print('x3.shape')
print(x3.shape)
print(x3)
#convert dtype for imshow
# x3 = np.asarray(x3, dtype = np.float, order ='F')
x3 = np.asarray(x3, dtype = float, order ='C')

Tcomm = timer() - tic
print('Launch+Comm Time (sec)             = %f'%(Tcomm))

# STEP 4: Finalize and display. ---------------------
# Display on leader.
if (Pid == 0):
    pstr = str(PARALLEL)
    npstr = str(Np)
    filename = 'X0loc_final.npy'
    X0loc_final = np.abs(np.squeeze(X0loc[:,:,0]))
    np.save(filename, X0loc_final) 
    plt.imshow(np.abs(np.squeeze(X0loc[:,:,0])), origin = 'lower')
    filename = 'beamformer_x0_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

    filename = 'X1loc_final.npy'
    X1loc_final = np.abs(np.squeeze(X1loc[:,:,0]))
    np.save(filename, X1loc_final) 
    plt.imshow(np.abs(np.squeeze(X1loc[:,:,0])), origin = 'lower')
    filename = 'beamformer_x1_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

    filename = 'X2loc_final.npy'
    X2loc_final = np.abs(np.squeeze(X2loc[:,:,0]))
    np.save(filename, X2loc_final) 
    plt.imshow(np.abs(np.squeeze(X2loc[:,:,0])), origin = 'lower')
    filename = 'beamformer_x2_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

    filename = 'x3_final.npy'
    np.save(filename, x3) 
    plt.imshow(x3)
    filename = 'beamformer_x3_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

print('')
print('SUCCESS')
print('')
print('')

