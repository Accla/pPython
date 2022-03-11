import numpy as np

from Falls import *

def local_dims(falls, dim):
    """Given the local FALLS and object dimension, calculates
    a vector of local dimensions of the distributed object.
    
    Usage:
    ------
    local_size = local_dims(falls, dim)
    
    FALLS: an array of FALLS structures for each dimension of
        the distributed object, i.e. FALLS(i) is a FALLS
        representation of the i-th dimension
    DIM: dimension of the distributed object (2, 3, or 4)
 
    LOCAL_SIZE:
        length(LOCAL_SIZE)is equal to the number of dimensions of the
        distributed object.
 
    Author: Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    if dim <= 4:
        # local_falls = falls;
        # compute local dimensions from the local FALLS
        # !!!NOTE: The following calculation works only if data on processor
        # RANK can be represented by a single FALLS.
        local_size = []
        if isinstance(falls[0], type(Falls())):
            for i in range(dim):
                # local size is just the local_len field of the local falls
                local_size = local_size + [falls[i].local_len]
        else: # no local data
            local_size = np.zeros(dim,dtype='int')
    else:
        print('ERROR(local_dims): Only objects up to 4-D are supported')
        # exit()
    return local_size

