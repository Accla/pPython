import numpy as np
from timeit import default_timer as timer
from math import ceil
import matplotlib.pyplot as plt

import pPython as GPC
from Dmap import *
from zeros import *
from put_local import *
from agg import *
from global_ind import *

from reference_frame import *
from zoom_frames import *

# for debugging
from size import *

"""
ZoomImage: zoom in on an image.

To run in serial without distributed arrays, set
    PARALLEL = 0
At the Python prompt type
    pZoomImage
To run in serial with distributed arrays, set
    PARALLEL = 1
At the Python prompt type
    pZoomImage
To run in parallel with distributed arrays at the Python prompt type
    eval(pRUN('pZoomImage',2,{}))
"""

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

# Set image size, number frames, start and stop scale.
N = 512;  Ns  = 16; Sstart = 32; Send = 1
N = 256   # Debug.

sigma  = 0.5     # Width of blur kernel.

# PARALLEL = 1     # Set control flag.
Zmap = 1         # Create serial map.
if (PARALLEL):
    Zmap = Dmap([1, 1, Np],{},range(Np))  # Create parallel map.
    #  1-D Cyclic Distribution:
    #  dist = dict()
    #  dist['0']=dict(); dist['0']['dist']='b'
    #  dist['1']=dict(); dist['1']['dist']='b'
    #  dist['2']=dict(); dist['2']['dist']='c'
    #  Zmap = Dmap([1, 1, Np],dist,range(Np))

Z = zeros(N,N,Ns,map=Zmap)           # Create distributed array.
if DEBUG:
    print('size(Z)')
    print(size(Z))

S = np.linspace(Sstart,Send,Ns)  # Compute scale factors.
if DEBUG > 1:
    print('S.shape and S itself')
    print(S.shape)
    print(S)

print('Zooming frames...')
tic = timer()                    # Start clock.
Z0 = reference_frame(N,0.1,0.8)  # Create reference frame.
# Compute local frames.
if DEBUG:
    print('global_ind(Z,2)[0]')
    print(global_ind(Z,2)[0])
    indx = S[np.array(global_ind(Z,2)[0])]
    print('S[np.array(global_ind(Z,2][0])]')
    print(indx.shape)
    print(indx)

Zloc = zoom_frames(Z0,S[np.array(global_ind(Z,2)[0])],sigma)
if DEBUG:
    print('Zloc[:,:,0]')
    print(Zloc[:,:,0])

Tcompute = timer()-tic           # Stop Clock.
print('Compute Time (sec)                 = %f'%(Tcompute))
Z  = put_local(Z,Zloc)           # Insert into distributed  array.
tic = timer()                    # Start Clock.
Zagg = agg(Z)                    # Aggregate on leader.
Tcomm = timer()-tic              # Stop Clock.
print('Launch+Comm Time (sec)             = %f'%(Tcomm))

# Save Zagg for plotting interactively later
pstr = str(PARALLEL)
npstr = str(Np)
np.save('frames_for_zoom_'+pstr+'_'+npstr+'.npy',Zagg)

# Compute gigaflops.
N_k = np.ceil(S*(5*sigma))
totalOps = 2*np.sum((N_k**2))*(N**2)
GigaFlops = 1.e-9*totalOps/Tcompute
print('Performance (Gigaflops)            = %f'%(GigaFlops))


# Display on leader.
if (Pid == 0):
    # set(gcf,'Name','Simulated Frames','DoubleBuffer','on','NumberTitle','off')
    for frameIndex in range(Ns):
        pimg = np.squeeze(Zagg[:,:,frameIndex])
        plt.imshow(pimg, origin = 'lower')
        filename = 'zoom_frame_'+pstr+'_'+npstr+'-'+str(frameIndex)
        # plt.savefig(filename+'.png')
        # np.save(filename+'.npy',pimg)
    

print('')
print('SUCCESS')
print('')
print('')

