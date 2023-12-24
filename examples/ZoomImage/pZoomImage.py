# Import NumPy and timer modules.
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

import pPython as GPC
from pPython.map import Dmap,zeros
from pPython.dmat import put_local,agg,find,global_ind

from reference_frame import *
from zoom_frames import *

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
    pRUN('pZoomImage',2,{})
"""

#  MPI information
Np = GPC.Np
Pid = GPC.Pid

# Set image size, number frames, start and stop scale.
N = 512;  Ns  = 16; Sstart = 24; Send = 1
N = 256   # Debug.

sigma  = 0.5     # Width of blur kernel.

PARALLEL = 1     # Set control flag.
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

S = np.linspace(Sstart,Send,Ns)  # Compute scale factors.
print('Zooming frames...')
tic = timer()                    # Start clock.
Z0 = reference_frame(N,0.1,0.8)  # Create reference frame.
# Compute local frames.
Zloc = zoom_frames(Z0,S[np.array(global_ind(Z,2))],sigma)
Tcompute = timer()-tic           # Stop Clock.
print('Compute Time (sec)                 = %f'%(Tcompute))
Z  = put_local(Z,Zloc)           # Insert into distributed  array.
tic = timer()                    # Start Clock.
Zagg = agg(Z)                    # Aggregate on leader.
Tcomm = timer()-tic              # Stop Clock.
print('Launch+Comm Time (sec)             = %f'%(Tcomm))

# Compute gigaflops.
N_k = np.ceil(S*(5*sigma))
totalOps = 2*np.sum((N_k**2))*(N**2)
GigaFlops = 1.e-9*totalOps/Tcompute
print('Performance (Gigaflops)            = %f'%(GigaFlops))

# Display on leader.
PLOT_IMAGE = 0
if (Pid == 0) and (PLOT_IMAGE == 1):
    f = dict()
    for frameIndex in range(Ns):
        print('Frame index: %d'%(frameIndex))
        pimg = np.squeeze(Zagg[:,:,frameIndex])
        f[frameIndex] = plt.figure(frameIndex,figsize=(1,1))
        ax = plt.Axes(f[frameIndex], [0., 0., 1., 1.])
        ax.set_axis_off()
        f[frameIndex].add_axes(ax)
        img = ax.imshow(pimg, origin = 'upper')
        img.set_cmap('bwr')
        filename = 'zoom_frame_'+str(frameIndex)
        plt.savefig(filename+'.png')
    # The following will keep the leader process running until all the figures are closed.
    plt.show()
    
print('')
print('SUCCESS')
print('')
print('')

