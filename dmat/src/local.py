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
        if (np.iscomplex(d.local)).any():
            y = np.real(d.local)
            z = np.imag(d.local)
            x = np.vectorize(complex)(y,z)
            if DEBUG:
                print('Return a complex local array from a DMAT')
        else:
            x = np.zeros(d.local.shape)
            x[:] = d.local
            if DEBUG:
                print('Return a real local array from a DMAT')
    else:
        # create an array same as d
        if (np.iscomplex(d)).any():
            y = np.real(d)
            z = np.imag(d)
            x = np.vectorize(complex)(y,z)
        else:
            x = np.zeros(d.shape,d.dtype)
            x[:] = d

    if DEBUG:
        print('<-- Exiting local')

    return x

