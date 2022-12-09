import numpy as np

from dcomplex import *
from size import *
from zeros import *

def remap(x, new_map):
    """
    REMAP Remaps a distributed array.
    
    REMAP(X, NEW_MAP) X is of class DMAT, NEW_MAP is of class MAP.
    Takes a distributed numerical array X and redistributes it according to
    the specified map NEW_MAP.
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering remap')

    s = size(x)
    if DEBUG:
        print('size(dmat): %s'%(str(s)))
    is_complex = 0
    if (np.iscomplex(local(x))).any():
        is_complex = 1

    if len(s) == 2: # 2D array, 2D map
        if is_complex:
            temp = dcomplex(zeros(s[0], s[1], map=new_map),zeros(s[0], s[1], map=new_map))
            temp[:,:] = x
            x = temp
        else:
            temp = zeros(s[0], s[1], map=new_map)
            if DEBUG:
                if isinstance(temp,Dmat):
                    print('local array shape of temp: %s'%(str(temp.local.shape)))
                    print('local array shape of x: %s'%(str(x.local.shape)))
                else:
                    print('local array shape of temp: %s'%(str(temp.shape)))
                    print('local array shape of x: %s'%(str(x.shape)))
            temp[:,:] = x
            x = temp
    elif len(s) == 3: #3 D array, 3D map
        temp = zeros(s[0], s[1], s[2], map=new_map)
        temp[:,:,:] = x
        x = temp
    elif len(s) == 4: # 4D array, 4D map
        temp = zeros(s[0], s[1], s[2], s[3], map=new_map)
        temp[:,:,:,:] = x
        x = temp
    else:
        print('ERROR (remap): REMAP can only be applied to arrays with 4 dimensions or less.')
        exit()
    
    if DEBUG:
        print('<-- Exiting remap')
    return x

