from multipledispatch import dispatch
import numpy as np

from grid_rand import *
from GridMap import *

@dispatch(int,int)
def rand(m,imap):
    """grid_rand() wrapper method for imap = 1 (int)
    """
    # print('Called rand(m,n,imap) where m and n are int')
    return np.rand((m,m))

@dispatch(int,int,int)
def rand(m,n,imap):
    """grid_rand() wrapper method for imap = 1 (int)
    """
    # print('Called rand(m,n,imap) where m and n are int')
    return np.random.rand(m,n)

@dispatch(int,type(GridMap()))
def rand(m,map):
    """grid_rand() wrapper method.
    """
    n=None
    q=None
    r=None
    dtype = None
    # print('Called rand(m,map) where m is a scalar')
    return grid_rand(m,n,q,r,map)

@dispatch(np.ndarray,type(GridMap()))
def rand(v,map):
    """grid_rand() wrapper method.
    """
    
    # Check if len(v) is equal to map.dim
    if not (len(v) == map.dim):
        print('ERROR(rand): the dimensions of the given list and the map does not match.')
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
        print('ERROR(rand): matrix dimension should be less than or equal to 4.')
        exit()
        
    dtype = None
    # print('Called rand(v,map) where v is a np.ndarray (vector)')
    return grid_rand(m,n,q,r,map)

@dispatch(int,int,GridMap)
def rand(m,n,map):
    """grid_rand() wrapper method.
    """
    q=None
    r=None
    dtype = None
    # print('Called rand(m,n,map)')
    return grid_rand(m,n,q,r,map)

@dispatch(int,int,int,type(GridMap()))
def rand(m,n,q,map):
    """grid_rand() wrapper method.
    """
    r=None
    dtype = None
    # print('Called rand(m,n,q,map)')
    return grid_rand(m,n,q,r,map)

@dispatch(int,int,int,int,type(GridMap()))
def rand(m,n,q,r,map):
    """grid_rand() wrapper method.
    """
    dtype = None
    # print('Called rand(m,n,q,rmap)')
    return grid_rand(m,n,q,r,map)

