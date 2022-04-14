import numpy as np

def local(d):
    """Returns the local part of the distributed array.
    if it is not a distributed array, it returns itself (no op).

    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering local')

    if hasattr(d,'local'):
        # create an array same as d.local
        x = np.zeros(d.local.shape)
        x[:] = d.local
    else:
        # create an array same as d
        x = np.zeros(d.shape)
        x[:] = d

    if DEBUG:
        print('<-- Exiting local')

    return x

