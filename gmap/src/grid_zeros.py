import numpy as np

from GridMap import *
from dmat import *
from pitfalls import *

def grid_zeros(m,n=None,q=None,r=None,p=None,dtype=None):
    """Zeros distributed array.
    
    NOTE: DIMENSION OF THE DISTRIBUTED ARRAY MUST BE CONSISTENT WITH THE
        DIMENSION OF THE MAP.
        
    ZEROS(N, P) If N is scalar, an N by N distributed matrix of
        zeros mapped according to the map specified by P; if N is a vector
        (numpy array), a distributed matrix with dimensions specified by N
        mapped according to P.
    ZEROS(M, N, P) M by N distributed matrix of zeros mapped according to the
        map specified by P.
    ZEROS(M, N, Q, P) MxNxQ distributed array of zeros mapped according to
        the map specified by P.
    ZEROS(M, N, Q, R, P) MxNxQxR distributed array of zeros mapped according to
        the map specified by P.
    ZEROS(M, N, ..., P, TYPE) MxNx... distributed array of zeros of datatype
        TYPE mapped according to the map specified by P.
 
    Example:
           Create a 100x10 dmat of 8-bit signed integers
           p = map([1 Ncpus], {}, 0:Ncpus-1)
           x = zeros(100, 10, p, 'int8')
 
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    Python porting: Dr. Chansup Byun
    """

    DEBUG = 0
    
    # form dims vector
    dims = []
    dims.append(m)
    if n:
        dims.append(int(n))
    if q:
        dims.append(int(q))
    if r:
        dims.append(int(r))
    
    if DEBUG:
        print('Dimension of distributed zeros: %d'%(len(dims)))
        print(dims)
    
    if not dtype:
        dtype = np.float64

    if not isinstance(p,GridMap):
        d = np.zeros(dims, dtype)
        return d

    if len(dims) < 5:
        d = dmat(dims, p)
    else:
        print('ERROR(map/zeros): Incorrect number of inputs')

    # Figure out local dimensions of dmat
    # NOTE: This is recomputing information already computed within
    # @dmat/dmat. Is there a cleaner way of getting this information?
    # comm = my_MCW.MPI_COMM_WORLD
    # my_rank = MPI_Comm_rank(comm)
    
    if DEBUG:
        # print('grid_zeros: my_rank = %d'%(my_rank))
        print(d.pitfalls)
        print(pitfalls(d))
    
    # falls = get_local_falls(pitfalls(d), p.grid, my_rank)
    # local_dims = localdims(falls, p.dim);

    # Allocating memory for the distributed matrix is no longer done
    # by @dmat/dmat.

    # Allocate a zeros matrix for the local portion of the dmat
    # Determine Matlab version

    d.local = np.zeros(d.local_dim, dtype)

    return d

