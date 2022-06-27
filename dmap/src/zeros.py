import numpy as np

from Dmap import *
from dmat import *
from pitfalls import *

def zeros(*array_sizes, **keywords):
    """
    Zeros distributed array.

    Input:
        array_sizes: array sizes 
        keywords: 
            'dmap': 1 or distributed map, Dmap object
            'dtype': data type of array element

    
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
           p = Dmap([1,Ncpus], {}, range(Ncpus))
           x = zeros(100, 10, dmap=p, dtype=int8)
 
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    Python porting: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering zero')
    #
    m = n = q = r = None
    # Construct the array sizes:
    ndim = len(array_sizes)
    if ndim>4:
        print('ERROR(zeros): array dimension larger than 4-D is not supported')
        exit()
    # form dims vector
    if isinstance(array_sizes[0],list):
        ndim = len(array_sizes[0])
        dims = array_sizes[0]
    else:
        dims = []
        dims.append(array_sizes[0])
        if ndim>1:
            dims.append(array_sizes[1])
        if ndim>2:
            dims.append(array_sizes[2])
        if ndim>3:
            dims.append(array_sizes[3])
    if DEBUG:
        print('Dimension of distributed zeros: %d'%(len(dims)))
        print(array_sizes)
        print(dims)
        
    dmap = None
    if 'dmap' in keywords:
        if isinstance(keywords['dmap'], Dmap):
            dmap = keywords['dmap']
        elif isinstance(keywords['dmap'], int):
            dmap = 1

    dtype = np.float64
    if 'dtype' in keywords:
        dtype = keywords['dtype']

    if not isinstance(dmap,Dmap):
        d = np.zeros(dims, dtype)
        return d

    if len(dims) < 5:
        d = dmat(dims, dmap)
    else:
        print('ERROR(map/zeros): Incorrect number of inputs')

    # Figure out local dimensions of dmat
    # NOTE: This is recomputing information already computed within
    # @dmat/dmat. Is there a cleaner way of getting this information?
    # comm = my_MCW.MPI_COMM_WORLD
    # my_rank = MPI_Comm_rank(comm)
    
    if DEBUG:
        # print('zeros: my_rank = %d'%(my_rank))
        print(d.pitfalls)
        print(pitfalls(d))
    
    # falls = get_local_falls(pitfalls(d), p.grid, my_rank)
    # local_dims = localdims(falls, p.dim);

    # Allocating memory for the distributed matrix is no longer done
    # by @dmat/dmat.

    # Allocate a zeros matrix for the local portion of the dmat
    # Determine Matlab version

    d.local = np.zeros(d.local_dim, dtype)

    if DEBUG:
        print('<-- Exiting zero')
    return d

    """
    pPython: Dr. Chansup Byun (cbyun@ll.mit.edu)

    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

