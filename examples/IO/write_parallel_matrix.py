import numpy as np

from local import *

def write_parallel_matrix(X,FILE):
    """Save a distributed matrix (2D) into a file
    """
    Xloc = local(X)        # Get local matrix.
    np.savez(FILE, Xloc=Xloc)

