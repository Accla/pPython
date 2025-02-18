import numpy as np

def sample_function(i_global, my_rank, my_other_arg):
    """Sample function to return three variables."""
    out = np.zeros((1,3),dtype=float)

    out[:,0] = i_global
    out[:,1] = my_rank
    out[:,2] = my_other_arg

    return out
