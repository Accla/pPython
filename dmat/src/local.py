from GridDmat import *

def local(d):
    """Returns the local part of the distributed array.
    if it is not a distributed array, it returns itself (no op).

    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    if isinstance(d,type(GridDmat())):
        return d.local
    else:
        return d

