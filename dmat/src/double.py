import numpy as np

def double(d):
    """
    DOUBLE Convert each local part of the DMAT to double precision.
    DOUBLE(D) returns the double precision value for the local part of D in
    a DMAT with the same mapping and dimensions as D.
    If the local part of D is already a double precision array, DOUBLE 
    has no effect.
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    """
    if isinstance(d, Dmat):
        d.local = np.float64(d.local)
    else:
        print('dmat/double: upsupported data type')
        exit()

    return d

