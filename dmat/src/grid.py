from Dmat import *

def grid(d):
    """
    GRID Returns the processor grid onto which the distributed array is mapped.
    
    Python version: Dr. Chansup Byun
    Author: Nadya Travinin
    """
    if not isinstance(d,Dmat):
        print('ERROR(grid): it is not a DMAT object.')
        exit()

    return d.map.grid
