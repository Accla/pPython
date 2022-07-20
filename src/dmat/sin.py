import numpy as np
from unfun import *

def sin(x):
    """SIN(X) is the sine of the elements of the distributed array X.
 
    Python version: Dr. Chansup Byun
    Author:  Nadya Travinin
    """

    x = unfun(np.sin, x)

    return x

    """
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    
    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

