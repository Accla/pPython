import numpy as np
import sys

# pPython class
import pPython as GPC
from Dmat import *
from Dmap import *
from agg import *

def display(m):
    """
    DISPLAY(M) is called for the Map object or the distributed matrix object, M
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering display')
    
    if isinstance(m,Dmap):
        print('  Map object')
        print('      Dimension:  %d'%(m.dim))
        print('      Grid specification: ')
        print(m.grid_spec)
        print('      Grid: ')
        print(m.grid)
        print('      Overlap: ')
        print(m.overlap)
        print('      Distribution: ')
        for i in range(m.dim):
            print('      Dim %d: %s'%(i,m.dist_spec[i]['dist']))

    elif isinstance(m,Dmat):
        # ToDo: is there any better way to find the input variable name in Python?
        # Find all keys with same value
        keys = [k for k,v in sys._getframe(1).f_locals.items() if v == m]

        if DEBUG:
            print(keys)
        print('%s = '%(keys[0]))
        print('  Distributed matrix object')
        print(agg(m))

    if DEBUG:
        print('<-- Exiting display')

