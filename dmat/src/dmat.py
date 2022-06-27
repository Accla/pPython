from multipledispatch import dispatch
import numpy as np

from Dmap import *
from grid_dmat import *

def dmat(v,p):
    """grid_dmat() wrapper method.
    
    p: map

    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering dmat')
        print('len(v): %d, p.dim=%d'%(len(v),p.dim))
        print(v)

    # Check if len(v) is equal to p.dim
    if isinstance(p,Dmap) and not (len(v) == p.dim):
        print('ERROR(dmat): the dimensions of the given list and the map, p, does not match.')
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
        print('ERROR(dmat): matrix dimension should be less than or equal to 4.')
        exit()
        
    # print('Called dmat(m,p) where m is a vector (list)')
    if DEBUG:
        print('--> Exiting dmat with calling grid_dmat(m,n,q,r,p)')
    
    return grid_dmat(m,n,q,r,p)

