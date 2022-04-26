import numpy as np

from unfun import *

def uint8(d):
    """UINT8 Convert each local part of the DMAT to unsigned 8-bit integers.
    UINT8(D) Returns unsigned 8-bit integer value for the local part of D
    in a DMAT with the same mapping and dimensions as D.
    If the local part of D is already unsigned 8-bit integer array, UINT8 
    has no effect.
 
    Python version: Dr. Chansup Byun
    Author:  Nadya Travinin
    """

    d = unfun(np.uint8, d)
 
    return d

    """
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    
    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

