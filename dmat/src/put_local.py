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

    if isinstance(x_local, np.ndarray):
        x.local = x_local
    else:
        x.local[:] = x_local

    return x

