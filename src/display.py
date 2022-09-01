import numpy as np

# pPython class
import pPython as GPC
from Dmat import *
from Dmap import *

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
        print('%s = '%(input_name))
        print('  Distributed matrix object')
        print(agg(m))

    if DEBUG:
        print('<-- Exiting display')

