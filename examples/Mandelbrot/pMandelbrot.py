import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

# Import PythonMPI methods.
import pPython as GPC
from GridMap import *
from zeros import *
from local import *
from put_local import *
from find import *
from agg import *
from global_ind import *

"""
Computes the Mandelbrot set in parallel.
To run in serial without distributed arrays, set
    PARALLEL = 0
At the Python prompt type
    pMandelbrot
To run in serial with distributed arrays, set
    PARALLEL = 1
At the Python prompt type
    pMandelbrot
To run in parallel with distributed arrays at the Python prompt type
    eval(pRUN('pMandelbrot',2,{}))
"""

#  MPI information
comm = GPC.comm
Np = GPC.comm_size
Pid = GPC.my_rank

# Set number of iterations, mesh size and threshold.
N=2400  
Niter=20  
epsilon = 0.001

N=800  # Debug

PARALLEL = 1                   # Set control flag.
Wmap = 1                       # Create serial map.
if (PARALLEL):
    Wmap = GridMap([Np,1],{},range(Np))        # Create parallel map.
    # dist = dict()
    # dist['0'] = {'dist':'c'}
    # dist['1'] = {'dist':'b'}
    # Wmap = map([Np,1],dist,range(Np))  # Cyclic distribution in the 1st dimension.

W = zeros(N,N,dmap=Wmap)            # Create distributed array
Wloc = local(W)                # Get local part.
myI = global_ind(W,0)          # Get local i indices.
myJ = global_ind(W,1)          # Get local j indices.

[ReC,ImC] = np.meshgrid(np.array(myJ)/(N/2) -1.6, np.array(myI)/(N/2) -1,indexing='xy')
Cloc = np.vectorize(complex)(ReC,ImC)        # Initialize C.
Zloc = np.vectorize(complex)(ReC,ImC)        # Initialize Z.
ieps = np.array(range(Wloc.size),dtype=int)  # Initialize indices.
tic = timer()                  # Start clock.
# Flatten arrays for the iteration
Cloc = Cloc.flatten('F')
Zloc = Zloc.flatten('F')
save_shape = Wloc.shape
Wloc = Wloc.flatten('F')
for i in range(Niter):         #  Compute Mandelbrot set.
    Zloc[ieps] = Zloc[ieps] * Zloc[ieps]  + Cloc[ieps]  # Numpy always use elementwise multiplication.
    Wloc[ieps] = np.exp(-np.absolute(Zloc[ieps]))
    # ieps = ieps[ find(Wloc[ieps] > epsilon) ]
    ieps = ieps[ tuple(find(Wloc[ieps] > epsilon)) ]

# Recover Wloc in the original shape before aggregation
Wloc = np.reshape(Wloc,save_shape,order='F')
W = put_local(W,Wloc)         # Put back into W

Tcompute = timer() - tic      # Stop clock.
print('Compute Time (sec)                 = %f'%(Tcompute))

tic = timer()                  # Start Clock.
W1 = agg(W)                    # Aggregate back to leader.
Tcomm = timer() - tic          # Stop clock.
print('Launch+Comm Time (sec)             = %f'%(Tcomm))

# Display on leader.
if (Pid == 0):
    # Show output in a figure
    plt.imshow(W1, origin = 'lower',  extent = [0, 10, 0, 10])
    pstr = str(PARALLEL)
    npstr = str(Np)
    filename = 'mandelbrot_'+pstr+'_'+npstr
    plt.savefig(filename+'.png')

print('')
print('')
print('SUCCESS')
print('')
print('')


