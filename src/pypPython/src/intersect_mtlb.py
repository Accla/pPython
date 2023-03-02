import numpy as np

def intersect_mtlb(a, b):
    """
    Python equivalentt Matlab intersect for C,IA,IB = intersect(A,B)
    https://stackoverflow.com/questions/45637778/how-to-find-intersect-indexes-and-values-in-python
    
    """
    a1, ia = np.unique(a, return_index=True)
    b1, ib = np.unique(b, return_index=True)
    aux = np.concatenate((a1, b1))
    aux.sort()
    c = aux[:-1][aux[1:] == aux[:-1]]
    return c, ia[np.isin(a1, c)], ib[np.isin(b1, c)]

