import numpy as np

def size(d, dims=None):
    """Size of the distributed array.
    SIZE(D) returns the length of each dimension in distributed
    matrix D or an array
 
    SIZE(D, DIMS) returns the length of those dimensions specified
    in DIMS.
 
    Python version: Dr. Chansup Byun
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    """

    # if no dimensions are specified, all are used
    if dims == None:
        # take care of non Dmat array
        if isinstance(d,np.ndarray):
            return list(d.shape)
        dims = list(range(d.dim))
    elif isinstance(dims,(int)):
        dims = [dims]
    
    # If there are no output arguments or 1 output argument,
    # return the size as an array
    s = []
    for i in dims:
        # take care of non Dmat array
        if isinstance(d,np.ndarray):
            s.append(d.shape[i])
        else:
            s.append(d.size[i])
    
    return s

    """
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    
    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

