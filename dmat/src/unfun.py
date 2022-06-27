import numpy

from Dmat import *

def unfun(fhandle,x):
    """Unary operation on a distirbuted array Y.
    X = fhandle(Y). Performs the unary operation specified by the
    function handle, fhanlde. The operation is entirely local, therefore
    the fhandle operation is simply performed on the local part of the
    distirbuted array Y.
 
    Python version: Dr. Chansup Byun
    Author:  Nadya Travinin
    """
    
    if isinstance(x,Dmat):
        x.local = fhandle(x.local)
    else:
        x = fhandle(x)

    return x

    """
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    
    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

