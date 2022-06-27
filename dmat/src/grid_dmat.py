import pyMPI_COMM_WORLD as pyMCW
from MPI_Comm_rank import *

from Dmap import *
from Dmat import *

from gen_pitfalls import *
from get_local_falls import *
from local_dims import *
from get_global_ind import *
from print_pitfalls import *
from print_falls import *

def grid_dmat(m,n=None,q=None,r=None,p=None):
    """Distributed matrix constructor.
    Creates the necessary data structures for the distributed matrix.
 
    NOTE: DMAT does not allocate memory for the distributed matrix
    and should never be called directly.  A distributed matrix should
    always be created with an appropriate constructor (ZEROS, ONES, RAND
    or SPARSE) which will be responsible for allocating memory.
 
    DMAT(N, P) If N is a scalar, creates the necessary data
        structures for an NxN distributed matrix; if N is a vector, 
        creates the necessary structures for an N distributed matrix
    DMAT(M, N, P) Creates the necessary data structures for an MxN
        distributed matrix.
    DMAT(M, N, Q, P) Creates the necessary data structures for an MxNxQ
        distributed array.
    DMAT(M, N, Q, R, P) Creates the necessary data structures for an
        MxNxQxR distributed array.
    
    D:
    D.MAP - processor map onto which the distributed array is mapped.  
    D.DIM - dimension of the distributed array. The dimension of the map has 
        to be consistent with the dimension of the distributed array.
    D.SIZE - size of the distributed array, i.e. number of elements in each
        dimension.
    D.PITFALLS - pitfalls structure that describes the distribution of the
        distributed array among the processors in the map.
    D.FALLS - falls structure that describes the distribution of the
        distributed object on the local processor.
    D.LOCAL - numerical part of the distributed array stored on the local
        processor.  Memory for D.LOCAL will be allocated by constructor
        functions, such as ZEROS, ONES, RAND and SPARSE.
    D.LOCAL_DIM - the size of local part of the distributed array (added with pPython)
    D.GLOBAL_IND - global indices of the distributed array local to the
        current processor.
 
    See also: ONES, ZEROS, RAND, SPARSE.
 
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering grid_dmat')
    
    # form dims vector
    dims = []
    dims.append(m)
    if n:
        dims.append(n)
    if q:
        dims.append(q)
    if r:
        dims.append(r)
    
    if DEBUG:
        print('Dimension of distributed zeros: %d'%(len(dims)))
        print(dims)
    
    if not isinstance(p,Dmap):
        d = np.array(dims)
        return d

    d = Dmat()
    
    if len(dims) == 1: # DMAT(M, P)
        dims = dims + dims

    d.map = p
    d.dim = len(dims)
    # d.size = dims
    d.shape = dims
    if isinstance(p,Dmap) and (p.dim != len(dims)):
        print('ERROR(dmat): Map and distributed object dimensions must match')
        exit()
        
    # create a PITFALLS for each dimension
    pitfalls = []
    for i in range(p.dim):
        if DEBUG:
            print('grid_dmat: axis, i = %d'%(i))
            print(p.grid.shape[i])
            print(p.dist_spec[str(i)])
            print(dims[i])
        if not (p.overlap):
            # p.grid.shape: tuple of the dim length
            # p.dist_spec: a dictionary of dictoary with key in str(dim)
            # print('no overlap')
            pitfalls.append(gen_pitfalls(p.grid.shape[i], p.dist_spec[str(i)], dims[i]))
        elif p.overlap[i]==0:
            # Same as not defined p.overlap
            # print('zero overlap')
            pitfalls.append(gen_pitfalls(p.grid.shape[i], p.dist_spec[str(i)], dims[i]))
        else:
            # non-zero p.overlap is defined.
            if DEBUG:
                print('non-zero overlap')
                print('p.overlap: %d in axis, i = %d'%(p.overlap[i],i))
            pitfalls.append(gen_pitfalls(p.grid.shape[i], p.dist_spec[str(i)], dims[i], p.overlap[i]))

    d.pitfalls = pitfalls
    if DEBUG:
        print(type(pitfalls))
        for i in range(len(pitfalls)):
            pf = pitfalls[i]
            print('grid_mat: pitfalls in axis, i, %d'%(i))
            print_pitfalls(pf)
            
    # get the local rank
    comm = pyMCW.MPI_COMM_WORLD
    my_rank = MPI_Comm_rank(comm)

    # get the local falls
    d.falls = get_local_falls(d.pitfalls, p.grid, my_rank)
    if DEBUG:
        print(p.grid)
        print(my_rank)
        for i in range(len(d.falls)):
            f = d.falls[i]
            print('grid_mat: FALLS in axis, i = %d'%(i))
            print_falls(f)
        
    # figure out local dimensions (d.local_dim added with pPython)
    local_dim = local_dims(d.falls, d.dim);
    d.local_dim = local_dim
  
    # Allocating memory is the responsibility of map functions
    # (e.g. ones, zeros, rand and sparse)
    # d.local = zeros(local_dim);
    d.local = []
  
    # get the local indices for the current processor
    grid_dims = p.grid_spec
    if len(grid_dims)<p.dim:
        for i in range(len(grid_dims),p.dim+1):
            grid_dims.append(0)

    d.global_ind = get_global_ind(d.falls, grid_dims)
    if DEBUG:
        print('--> Exiting grid_dmat')
    
    return d

########################################################
# pMatlab: Parallel Matlab Toolbox
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################

