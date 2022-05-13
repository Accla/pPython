import numpy as np

def put_local(x, x_local):
    """Assigns new data to the local part of the distributed array.
    
    Usage:
    ------
    X = PUT_LOCAL(X, X_LOCAL) 
        X: distributed array
        X_LOCAL: local part of the distributed array, X
        
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering put_local')

    if hasattr(x,'local'):
        if (np.iscomplex(x_local)).any():
            y = np.real(x_local)
            z = np.imag(x_local)
            x.local = np.vectorize(complex)(y,z)
        else:
            x.local[:] = x_local
    else:
        if (np.iscomplex(x_local)).any():
            y = np.real(x_local)
            z = np.imag(x_local)
            x = np.vectorize(complex)(y,z)
        else:
            x = np.zeros(x.shape,x.dtype)
            x[:] = x_local

    if DEBUG:
        print('<-- Exiting put_local')
    return x

