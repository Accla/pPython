import numpy as np

from intersect_mtlb import *

def get_local_ind(global_ind, ind):
    """
    get_local_ind returns a dictionary array of local indices given an array of
    global indices on the current processor and an array of global indices
    that are being referenced.
    
    GET_LOCAL_IND(GLOBAL_IND, IND)
    GLOBAL_IND - a dictionary with numeric string key of length equal to the number of dimensions.
    Each entry in the array specifies the global indices in the i-th
    dimension stored on the current processor.
    
    IND - a dictionary of length equal to the number of dimensions, where each
    entry specifies the global indices being referenced in that
    dimension.
    
    Returns LOCAL_IND:
    len(LOCAL_IND) is equal to the number of dimensions of the distributed object. 
    LOCAL_IND[i] is of the form [ind1 ind2 ind3 ...] where ind_i is a
    local index of the data stored locally.
    
    LOCAL_IND is a python dictionary with the numeric key for each dimension
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """
    
    DEBUG = 1
    if DEBUG:
        print('--> Enterintering get_local_ind')
        print('global_ind & ind')
        print(global_ind)
        print(ind)

    local_ind = dict()
    dim = len(ind)
    if dim <= 4: # number of dimensions of the distributed object is 4 or less
        for i in range(dim):
            local_ind[i] = []
            if global_ind[str(i)] == ':': 
                # dimension i is not distributed
                loc_inds = ind[str(i)]
            else:  
                # dimension i is distributed
                if ind[str(i)] == ':':
                    loc_inds = ':'
                else:
                    # PRESERVES THE ORDERING OF INDICES
                    loc_inds = []
                    #  vvvvv new code vvvvv
                    [vals, i_global, i_ind] = intersect_mtlb(global_ind[str(i)], ind[str(i)])
                    i_ind_sorted = np.argsort(i_ind)
                    ind_sorted = i_ind[i_ind_sorted]
                    loc_inds = i_global[i_ind_sorted]
                    if (len(loc_inds) == 0):
                        loc_inds = []
                    #  ^^^^^ new code ^^^^^
                # dimension i is distributed
            local_ind[i] = loc_inds
    else:  # number of dimensions is greater than 4
        print('localdims: Only objects up to 4-D are supported')
        exit()
        # number of dimensions is greater than 4    

    if DEBUG:
        print('local_ind')
        print(local_ind)
        print('<-- Exiting get_local_ind')
    
    return local_ind

