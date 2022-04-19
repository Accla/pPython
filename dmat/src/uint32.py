import numpy as np

def uint32(d):
    """UINT32 Convert each local part of the DMAT to unsigned 32-bit integers.
    UINT32(D) Returns unsigned 32-bit integer value for the local part of D
    in a DMAT with the same mapping and dimensions as D.
    If the local part of D is already unsigned 32-bit integer array, UINT32 
    has no effect.
 
    Python version: Dr. Chansup Byun
    Author:  Nadya Travinin
    """

    d = unfun(np.uint32, d)
 
    return d

    """
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    
    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

