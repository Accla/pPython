from Dmat import *
from size import *

def global_ind(d, dim=None):
    """Returns the global indices of the distributed array D local to 
    the current processor in the specified dimension, DIM.
    
    Usage:
    ------
    local_ind = global_ind(d,dim=None)
    
    D: distributed array
    dim: dimension of the distributed array D. 
        A scalar or list containing the desired dimension axis.
 
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering global_ind')
        
    if dim == None:
        # no dim provided. returns for all dimension
        if DEBUG:
            print('no dim')
        dims = list(range(len(d.shape)))
    else:
        if DEBUG:
            print('provided dim')
        if isinstance(dim,int):
            dims = []
            dims.append(dim)
        else:
            dims = dim

    if isinstance(d,Dmat): 
        #
        # distributed array
        #
        my_inds = d.global_ind
        s = d.shape
        if DEBUG:
            print('my_inds:')
            print(my_inds)
            print('d.shape:')
            print(s)
    
        if len(dims)==1:
            local_ind = my_inds[dims[0]]
        else:
            local_ind = []
            for i in range(len(dims)):
                local_ind.append(my_inds[dims[i]])
    else:
        #
        # non-distributed array
        # 
        my_inds = size(d)
        if len(my_inds) == 1:
            # 1-D array (even if array construct was 2-D)
            local_ind = list(range(my_inds[0]))
        else:
            if len(dims)==1:
                local_ind = list(range(my_inds[dims[0]]))
            else:
                local_ind = []
                for i in range(len(dims)):
                    local_ind.append(list(range(my_inds[dims[i]])))

    if DEBUG:
        print('--> Exiting global_ind')
    return local_ind

