from multipledispatch import dispatch
import numpy as np

from GridMap import *
from grid_ones import *

@dispatch(int,int)
def ones(m,n):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    q=None
    r=None
    map = None
    dtype = None
    # print('Called ones(m,n)')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(int,int,int,object)
def ones(m,n,q,r):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    if isinstance(r,GridMap):
        map == r 
        r = None
    elif isinstance(r,int) or r == None:
        map = None
    else:
        print('ERROR(ones):  the 4th argunment data type is not supported')
        exit()
    dtype = None
    # print('Called ones(m,n)')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(object,GridMap)
def ones(v,map):
    """grid_ones() wrapper method.
    """
    
    if isinstance(v,(np.ndarray,list)):
        # Check if len(v) is equal to map.dim
        if not (len(v) == map.dim):
            print('ERROR(ones): the dimensions of the given list and the map does not match.')
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
            print('ERROR(ones): matrix dimension should be less than or equal to 4.')
            exit()
    elif isinstance(v,(int,np.int64)):
        m=v
        n=None
        q=None
        r=None
    else:
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()
    dtype = None
    # print('Called ones(m,map) where m is a np.ndarray (vector)')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(object,object,GridMap)
def ones(m,n,map):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    q=None
    r=None
    dtype = None
    # print('Called ones(m,n,map)')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(object,object,object)
def ones(m,n,map):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    if not isinstance(map,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for map.'%(type(map)))
        exit()
    q=None
    r=None
    dtype = None
    # print('Called ones(m,n,map)')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(object,object,object,GridMap)
def ones(m,n,q,map):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    if not isinstance(q,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(q)))
        exit()
    r=None
    dtype = None
    # print('Called ones(m,n,q,map)')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(object,object,object,object,GridMap)
def ones(m,n,q,r,map):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    if not isinstance(q,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(q)))
        exit()
    if not isinstance(r,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(r)))
        exit()
    dtype = None
    # print('Called ones(m,n,q,rmap)')
    return grid_ones(m,n,q,r,map,dtype)
#
# Use of dtype definition
#
@dispatch(object,GridMap,str)
def ones(v,map,dtype):
    """grid_ones() wrapper method.
    """
    
    if isinstance(v,(np.ndarray,list)):
        # Check if len(v) is equal to map.dim
        if not (len(v) == map.dim):
            print('ERROR(ones): the dimensions of the given list and the map does not match.')
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
            print('ERROR(ones): matrix dimension should be less than or equal to 4.')
            exit()
    elif isinstance(v,(int,np.int64)):
        m=v
        n=None
        q=None
        r=None
    else:
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(v)))
        exit()

    # print('Called ones(m,map) where m is a np.ndarray (vector)')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(object,object,GridMap,str)
def ones(m,n,map,dtype):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    q=None
    r=None
    # print('Called ones(m,n,map) with dtype')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(object,object,object,GridMap,str)
def ones(m,n,q,map,dtype):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    if not isinstance(q,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(q)))
        exit()
    r=None
    # print('Called ones(m,n,q,map) with dtype')
    return grid_ones(m,n,q,r,map,dtype)

@dispatch(object,object,object,object,GridMap,str)
def ones(m,n,q,r,map,dtype):
    """grid_ones() wrapper method.
    """
    if not isinstance(m,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(m)))
        exit()
    if not isinstance(n,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(n)))
        exit()
    if not isinstance(q,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(q)))
        exit()
    if not isinstance(r,(int,np.int64)):
        print('ERROR(ones): data type, %s, is not supported for matrix size.'%(type(r)))
        exit()
    # print('Called ones(m,n,q,r,map) with dtype')
    return grid_ones(m,n,q,r,map,dtype)

