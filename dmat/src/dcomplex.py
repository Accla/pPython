import numpy as np

from size import *
from zeros import *

def dcomplex(x,y):
    """Convert each local part of the DMATs, X & y to a new local portion of DMAT with a complex number, x.local + (y.local)j.
    If x & y are not a DMAT, it returns complex(x,y)
 
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering dcomplex')

    if hasattr(x,'local') and hasattr(y,'local'):
        # DMAT objects
        if DEBUG:
            print('DMAT object')
        # if only works if x and y are equally sized and distributed DMAT
        if x.map == y.map:
            d = zeros(size(x),map=x.map,dtype=complex)
            d.local = np.vectorize(complex)(x.local,y.local)
        else:
            print('ERROR: Both DMAT objects have to be the same kind.')
            exit()
        if DEBUG:
            print('dmat/dcomplex: return distributed array with its local array shape of %s'%(str(d.local.shape)))
    else:
        d = np.vectorize(complex)(x,y)
        if DEBUG:
            print('dmat/dcomplex: return non-distributed array shape of %s'%(str(d.shape)))
 
    if DEBUG:
        print('<-- Exiting dcomplex')
    return d

    """
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    
    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

