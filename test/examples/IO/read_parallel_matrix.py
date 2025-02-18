import numpy as np

from local import *
from put_local import *

def read_parallel_matrix(X,file):
    """Read a distributed array (Matrix in 2-D)
    """
    Xloc = local(X)             # Create a local matrix.

    npzfile = np.load(file)
    Xloc[:] = npzfile['Xloc']
    X = put_local(X,Xloc)       # Copy back to distributed matrix.

    return X

