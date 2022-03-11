from multipledispatch import dispatch
import numpy as np

@dispatch(int,type(GridMap()))
def zeros(m,map):
    """grid_zeros() wrapper method.
    """
    n=None
    q=None
    r=None
    dtype = None
    # print('Called zeros(m,map) where m is a scalar')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(np.ndarray,type(GridMap()))
def zeros(v,map):
    """grid_zeros() wrapper method.
    """
    
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
        
    dtype = None
    # print('Called zeros(m,map) where m is a np.ndarray (vector)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(int,int,type(GridMap()))
def zeros(m,n,map):
    """grid_zeros() wrapper method.
    """
    q=None
    r=None
    dtype = None
    # print('Called zeros(m,n,map)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(int,int,int,type(GridMap()))
def zeros(m,n,q,map):
    """grid_zeros() wrapper method.
    """
    r=None
    dtype = None
    # print('Called zeros(m,n,q,map)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(int,int,int,int,type(GridMap()))
def zeros(m,n,q,r,map):
    """grid_zeros() wrapper method.
    """
    dtype = None
    # print('Called zeros(m,n,q,rmap)')
    return grid_zeros(m,n,q,r,map,dtype)
#
# Use of dtype definition
#
@dispatch(int,type(GridMap()),str)
def zeros(m,map,dtype):
    """grid_zeros() wrapper method.
    """
    n=None
    q=None
    r=None
    # print('Called zeros(m,map) with m as a scalar & dtype')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(np.ndarray,type(GridMap()),str)
def zeros(v,map,dtype):
    """grid_zeros() wrapper method.
    """
    
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
        
    # print('Called zeros(m,map) where m is a np.ndarray (vector)')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(int,int,type(GridMap()),str)
def zeros(m,n,map,dtype):
    """grid_zeros() wrapper method.
    """
    q=None
    r=None
    # print('Called zeros(m,n,map) with dtype')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(int,int,int,type(GridMap()),str)
def zeros(m,n,q,map,dtype):
    """grid_zeros() wrapper method.
    """
    r=None
    # print('Called zeros(m,n,q,map) with dtype')
    return grid_zeros(m,n,q,r,map,dtype)

@dispatch(int,int,int,int,type(GridMap()),str)
def zeros(m,n,q,r,map,dtype):
    """grid_zeros() wrapper method.
    """
    # print('Called zeros(m,n,q,r,map) with dtype')
    return grid_zeros(m,n,q,r,map,dtype)

