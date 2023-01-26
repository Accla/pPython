from Dmat import *

def grid(d):
    """
    GRID Returns the processor grid onto which the distributed array is mapped.
    
    Python version: Dr. Chansup Byun
    Author: Nadya Travinin
    """
    if not isinstance(d,Dmat):
        raise Exception('ERROR(grid): it is not a DMAT object.')

    print('Function grid(): called')
    return d.map.grid
