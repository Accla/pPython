from scipy.sparse import csr_matrix
from math import floor
import numpy as np

# pPython class
import pPython as GPC
from Dmat import *
from Dmap import *
from dmat import *
from get_local_falls import *
from local_dims import *
from StopExecution import *

def sparse(*argv,**kwargs):
    """
    SPARSE Convert a full distributed matrix to a sparse distributed matrix or 
    Create a sparse distributed matrix.
    
    S = SPARSE(X) converts a sparse or full distributed matrix to sparse
    form by squeezing out any zero elements.
    
    S = SPARSE(I,J,S,M,N,NZMAX,map=P) generates an M-by-N sparse distributed
    matrix distributed according map P with space allocated for NZMAX
    nonzeros (note that NZMAX applies to the overall distributed matrix,
    not to individual processors.  NZMAX will be distributed as evenly
    as possible over all processors).
    
    The rows of [I,J,S] are intended to use to initialize the non-zero
    values of the matrix.  However, SPARSE currently does not support the
    use of I, J and S they are kept to remain consistent with the SPARSE
    function built into Matlab.
    
    There are four ways that SPARSE can be called:
    
    S = SPARSE([],[],[],M,N,NZMAX,map=P)
    
    S = SPARSE([],[],[],M,N,map=P) uses NZMAX = 0.
    
    S = SPARSE([],[],[],map=P) uses M = 0 and N = 0.  This generates the
    ultimate sparse matrix, an M-by-N all zero matrix.
    
    S = SPARSE(M,N,map=P) abbreviates SPARSE([],[],[],M,N,0,P).  This also
    generates an M-by-N all zero matrix.
    
    The recommended method of creating a sparse distributed matrix is
    with SPALLOC.
    
    See also SPALLOC    
    
    Author:   Hahn Kim
    Python version: Dr. Chansup Byun
    """
    DEBUG = 1
    if DEBUG:
        print('--> Entering sparse')
    
    # check number of input arguments
    nargin = len(argv)
    if DEBUG:
        print('Number of arguments: %d'%(nargin))
    
    if nargin==1:
        d = argv[0]
        if isinstance(d,Dmat):
            d.local = csr_matrix(d.local)
        else:
            print('Error: input argument is not a disbributed matrix or array.')
            raise StopExecution
        return d
    
    # Check if map is proivded
    p = None # default is an empty map P
    for key, value in kwargs.items():
        if key == 'map':
            p = value

    if not isinstance(p,Dmap):
        print('@map/sparse: At least 1 argument must be a map')
        raise StopExecution
        
    # SPARSE(M,N,P)
    if nargin==2:
        ii    = []          # Row indices for values stored in s
        jj    = []          # Column indices for values stored in s
        s     = []          # Non-zero values used to initialize the distributed
        # sparse matrix
        m     = argv[0] # Number of rows
        n     = argv[1] # Number of cols
        nzmax = 0           # Number of non-zero values to allocate space for
    
    # SPARSE(I,J,S,P)
    elif nargin==3:
        ii    = argv[0]
        jj    = argv[1]
        s     = argv[2]
        m     = max(ii)
        n     = max(jj)
        nzmax = len(s)
    
    # SPARSE(I,J,S,M,N,P)
    elif nargin==5:
        ii    = argv[0]
        jj    = argv[1]
        s     = argv[2]
        m     = argv[3]
        n     = argv[4]
        nzmax = length(s)
    
    # SPARSE(I,J,S,M,N,NZMAX,P)
    elif nargin==6:
        ii    = argv[0]
        jj    = argv[1]
        s     = argv[2]
        m     = argv[3]
        n     = argv[4]
        nzmax = argv[5]

    # For now, sparse only works when ii, jj, and s are [].  Specifying
    # values for ii, jj and s will be implemented in the future.
    if (len(ii) != 0 or len(jj) !=  0 or len(s) != 0):
        print('@map/sparse: Specifying initial values for sparse '
              'distributed matrices is not supported, yet.')
    
    # Create the 2D distributed object
    d = Dmat(m, n, map=p)
    
    # Figure out local dimensions of dmat
    
    # NOTE: This is recomputing information already computed within
    # @dmat/dmat. Is there a cleaner way of getting this information?
    falls = get_local_falls(d.pitfalls, p.grid, GPC.Pid)
    local_size = local_dims(falls, p.dim)
    
    # What if the user specifies values for ii, jj and s AND a value
    # for nzmax, such that on a processor's local portion of the sparse
    # dmat, nzmax_local is too small?  Maybe only do this when values
    # for i,j and s are specified?  Otherwise, evenly distribute nzmax?
    # For now, evenly distribute nzmax across all processors
    nzmax_local = floor(nzmax / GPC.Np)
    nzmax_rem   = nzmax - nzmax_local * GPC.Np
    if (GPC.Pid < nzmax_rem):
        nzmax_local = nzmax_local + 1
    
    # Allocate a sparse matrix for the local portion of the dmat
    # Python does not have a function equivalent to MATLAB spalloc
    # The following codes is trying to mimick spalloc
    # s.local = spalloc(local_size[0], local_size[1], nzmax_local)
    s = np.zeros(nzmax_local)
    ii = []
    jj = []
    for k in range(nzmax_local):
        ii = ii + [ k%local_size[0] ]
        jj = jj + [ floor(k/local_size[0]) ]
    if DEBUG:
        print('nzmax_local: %d'%(nzmax_local))
        print('Length of row: %d'%(len(ii)))
        print('Length of col: %d'%(len(jj)))
        print('Length of data: %d'%(len(s)))
        print('Sparse matrix shape: (%d, %d)'%(local_size[0],local_size[1]))

    d.local = csr_matrix((s, (ii, jj)), shape=(local_size[0], local_size[1]), dtype=np.float64)

    if DEBUG:
        print('<-- Exiting sparse')
    return d

