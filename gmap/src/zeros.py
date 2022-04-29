from multipledispatch import dispatch
import numpy as np

from GridMap import *
from grid_zeros import *

@dispatch(object)
def zeros(v):
    """grid_zeros() wrapper method.
    """
    n=None
    q=None
    r=None
    if isinstance(v,(np.ndarray)):
        # Extract elements from the list.
        m = v[0]
        if len(v) == 2:
            n = v[1]
        elif len(v) == 3:
            n = v[1]
            q = v[2]
        elif len(v) == 4:
            n = v[1]
            q = v[2]
            r = v[3]
        else:
            print('ERROR(zeros): matrix dimension should be less than or equal to 4.')
            exit()
    elif isinstance(v,(int,np.int64)):
        m=v
        map = 1
    else:
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    dtype = None
    # print('Called zeros(m) where m is an integer or a np.ndarray (vector)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(object,object)
def zeros(v,map):
    """grid_zeros() wrapper method.
    """
    
    if isinstance(v,(np.ndarray)):
        # check if map (the 2nd element) is GridMap object
        if isinstance(map,GridMap):
            # Check if len(v) is equal to map.dim
            if not (len(v) == map.dim):
                print('ERROR(zeros): the dimensions of the given list and the map does not match.')
                exit()
        n=None
        q=None
        r=None

        # Extract elements from the list.
        m = v[0]
        if len(v) == 2:
            n = v[1]
        elif len(v) == 3:
            n = v[1]
            q = v[2]
        elif len(v) == 4:
            n = v[1]
            q = v[2]
            r = v[3]
        else:
            print('ERROR(zeros): matrix dimension should be less than or equal to 4.')
            exit()
    elif isinstance(v,(int,np.int64)):
        m=v
        # check if map (the 2nd element) is GridMap object
        if isinstance(map,GridMap):
            n=None
        else:
            # non-distributed numpy array
            n = map
            map = 1
        q=None
        r=None
    else:
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    dtype = None
    # print('Called zeros(m,map) where m is a np.ndarray (vector)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(object,object,object)
def zeros(m,n,map):
    """grid_zeros() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    q=None
    r=None
    if isinstance(map,str):
        # Assuming map is datatype
        dtype = map
        map = 1
    else:
        dtype = None
    # print('Called zeros(m,n,map)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(object,object,object,object)
def zeros(m,n,q,map):
    """grid_zeros() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(q,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    r=None
    dtype = None
    # print('Called zeros(m,n,q,map)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(object,object,object,object,object)
def zeros(m,n,q,r,map):
    """grid_zeros() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(q,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(r,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    dtype = None
    # print('Called zeros(m,n,q,rmap)')
    return grid_zeros(m,n,q,r,map,dtype)
#
# Use of dtype definition
#
@dispatch(object,type(GridMap()),str)
def zeros(v,map,dtype):
    """grid_zeros() wrapper method.
    """
    
    if isinstance(v,(np.ndarray)):
        # Check if len(v) is equal to map.dim
        if not (len(v) == map.dim):
            print('ERROR(zeros): the dimensions of the given list and the map does not match.')
            exit()
        n=None
        q=None
        r=None
        # Extract elements from the list.
        m = v[0]
        if len(v) == 2:
            n = v[1]
        elif len(v) == 3:
            n = v[1]
            q = v[2]
        elif len(v) == 4:
            n = v[1]
            q = v[2]
            r = v[3]
        else:
            print('ERROR(zeros): matrix dimension should be less than or equal to 4.')
            exit()
    elif isinstance(v,(int,np.int64)):
        m=v
        n=None
        q=None
        r=None
    else:
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()

    # print('Called zeros(m,map) where m is a np.ndarray (vector)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(object,object,type(GridMap()),str)
def zeros(m,n,map,dtype):
    """grid_zeros() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    q=None
    r=None
    # print('Called zeros(m,n,map) with dtype')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(object,object,object,type(GridMap()),str)
def zeros(m,n,q,map,dtype):
    """grid_zeros() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(q,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    r=None
    # print('Called zeros(m,n,q,map) with dtype')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(object,object,object,object,type(GridMap()),str)
def zeros(m,n,q,r,map,dtype):
    """grid_zeros() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(q,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    if not isinstance(r,(int,np.int64)):
        print('ERROR(zeros): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    # print('Called zeros(m,n,q,r,map) with dtype')
    return grid_zeros(m,n,q,r,map,dtype)

