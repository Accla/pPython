from multipledispatch import dispatch
import numpy as np

from GridDmat import *
from grid_global_ind import *

dmat_type = type(GridDmat())

#
# For np.ndarray type variables
#

@dispatch(np.ndarray)
def global_block_ranges(d):
    """Returns the range of indices in the specified dimension along with its rank
    
    Usage:
    ------
    ind = global_block_ranges(D) 
    
    d: a DOUBLE.
    ind: an array containing index range boundary for all dimensions along with its rank
    
    One of the functions that mimics the parallel library behavior on
    non-distributed arrays.
 
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun

    """
    
    dims = []
    for i in range(len(d.shape)):
        dims.append(i)

    return global_block_ranges(d, dims)


@dispatch(np.ndarray,int)
def global_block_ranges(d, dim):
    """Returns the range of indices in the specified dimension.
    
    Usage:
    ------
    ind = global_block_ranges(D, dim) 
    
    d: a DOUBLE.
    dim: an integer from range(max. dimension)
    ind: an array containing index range boundary for given dimension
    
    One of the functions that mimics the parallel library behavior on
    non-distributed arrays.
 
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun

    """
    
    dims = []
    dims.append(dim)
        
    return global_block_ranges(d, dims)


@dispatch(np.ndarray,list)
def global_block_ranges(d, dims):
    """Returns the range of indices in the specified dimension.
    
    Usage:
    ------
    ind = global_block_ranges(D, dims=None) 
    
    d: a DOUBLE.
    dims: a list of dimension or dimensions
    ind: an array containing index range boundary for given list
    
    One of the functions that mimics the parallel library behavior on
    non-distributed a rrays.
 
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun

    """
    
    ind = np.zeros((len(dims),3),int)
    # 1st: its rank (for serial)
    # 2nd: starting index, which is always 0
    # 3rd: ending index (N-1)
    my_inds = list(d.shape)
    # print(my_inds)
    
    for i in range(len(dims)):
        # For python, index ranges from 0 to N-1
        # print(dims[i])
        ind[i,2] = my_inds[dims[i]]-1
        
    return ind

#
# For distributed array type (GridDmat) variables
#

@dispatch(dmat_type)
def global_block_ranges(d):
    """Returns the global index range of the distributed array D for all processors in 
    all dimensions of D.
    
    Usage:
    ------
    ind = global_block_ranges(D) 
            
    d: a distributed array.

    For each dimension, the following is the format of the indices returned:
        Array size: NUM_PROCS_IN_GRIDx3. Each line of the returned array M, 
        M(i,:) contains the follwing information 
        [PROCESSOR_RANK START_INDEX END_INDEX]

    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun
    
    """

    dims = []
    for i in range(len(d.shape)):
        dims.append(i)

    return global_block_ranges(d, dims)


@dispatch(GridDmat,int)
def global_block_ranges(d, dim):
    """Returns the global index ranges of the distributed array D for all processors in the 
    specified dimension, DIM.
    
    Usage:
    ------
    ind = global_block_ranges(D) 
            
    d: a distributed array.

    For each dimension, the following is the format of the indices returned:
        Array size: NUM_PROCS_IN_GRIDx3. Each line of the returned array M, 
        M(i,:) contains the follwing information 
        [PROCESSOR_RANK START_INDEX END_INDEX]

    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun
    
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering global_block_ranges, signature: (GridDmat,int)')

    dims = []
    dims.append(dim)
        
    if DEBUG:
        print('<-- Exiting calling global_block_ranges, signature: (GridDmat,List)')
    return global_block_ranges(d, dims)


@dispatch(GridDmat,list)
def global_block_ranges(d, dims):
    """Returns the global index ranges of the distributed array D for all processors in the 
    specified dimension, DIMS.
    
    Usage:
    ------
    ind = global_block_ranges(D, dims) 
    
    For each dimension, the following is the format of the indices returned:
        Array size: NUM_PROCS_IN_GRIDx3. Each line of the returned array ind, 
        ind(i,:) contains the follwing information 
        [PROCESSOR_RANK START_INDEX END_INDEX]
    
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun
    
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering global_block_ranges')

    # processor grid on which the object is distributed
    grid = d.map.grid
    grid_dims = list(grid.shape)
    dim = len(grid_dims)

    # Obtain global index information for all processor grid
    global_ind = grid_global_ind(d)
    
    my_inds = d.global_ind
    """
    global_ind is a dictionary such as {'0': [0, 1, 2, 3], '1': [0, 1, 2]}
    """
    s = d.shape
    
    if len(dims)>1:
        ind = []

    for i in range(len(dims)):
        num_procs = np.prod(grid_dims)  # total number of grid processors
        if DEBUG:
            print('num_procs = %d'%(num_procs))
            print(grid_dims)
        temp = np.zeros((num_procs,3),int)   # create array to store indices for dim i
        proc_count = 0                  # keep track of the number of processors

        if dim==2: #2D array
            for g1 in range(grid_dims[0]): #grid cols
                for g2 in range(grid_dims[1]): #grid rows
                    curr_inds = global_ind[str(g1)][str(g2)]
                    # print(curr_inds)
                    dim_inds = curr_inds[str(dims[i])]
                    temp[proc_count,0:] = [grid[g1,g2], dim_inds[0], dim_inds[-1]] 
                    proc_count = proc_count+1 
        elif dim==3: #3D array
            for g1 in range(grid_dims[0]):
                for g2 in range(grid_dims[1]):
                    for g3 in range(grid_dims[2]):
                        curr_inds = global_ind[str(g1)][str(g2)][str(g3)]
                        dim_inds = curr_inds[str(dims[i])]
                        temp[proc_count,0:] = [grid[g1,g2,g3], dim_inds[0], dim_inds[-1]] 
                        proc_count = proc_count+1 
        elif dim==4: #4D array
            for g1 in range(grid_dims[0]):
                for g2 in range(grid_dims[1]):
                    for g3 in range(grid_dims[2]):
                        for g4 in range(grid_dims[3]):
                            curr_inds = global_ind[str(g1)][str(g2)][str(g3)][str(g4)]
                            dim_inds = curr_inds[str(dims[i])]
                            temp[proc_count,0:] = [grid[g1,g2,g3,g4], dim_inds[0], dim_inds[-1]] 
                            proc_count = proc_count+1 
        if len(dims)>1:
            ind.append(temp)
        else:
            ind = temp
    
    if DEBUG:
        print('<-- Exiting global_block_ranges')
    return ind

    """
    Python conversion: Dr. Chansup Byun (cbyun@ll.mit.edu)
    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

