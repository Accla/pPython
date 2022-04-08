import numpy as np

import GridPython as GPC
from dmat import *

def grid_rand(m,n,q,r,p):
    """Distributed array of random numbers between 0 and 1 distributed uniformly.
    NOTE: DIMENSION OF THE DISTRIBUTED ARRAY MUST BE CONSISTENT WITH THE
        DIMENSION OF THE MAP.
    Calls the MATLAB RAND function to create each local part of the
        distributed array. The resulting array will not be the same as a DOUBLE
        rand array of the same dimensions.
    RAND(N, P) If N is scalar, an N by N distributed matrix of
        random numbers mapped according to the map specified by P;
        if N is a vector, a distributed matrix with dimensions
        specified by N mapped according to P.
    RAND(N, P) N by N distributed matrix of random numbers mapped according to the map
        specified by P.
    RAND(M, N, P) M by N distributed matrix of random numbers mapped according to the
        map specified by P.
    RAND(M, N, Q, P) MxNxQ distributed array of random numbers mapped according to
        the map specified by P.
    RAND(M, N, Q, R, P) MxNxQxR distributed array of random numbers mapped according to
        the map specified by P.
 
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    """
    
    DEBUG = 1
    if DEBUG:
        print('--> Entering grid_rand')
    
    # form dims vector
    dims = []
    dims.append(m)
    if n:
        dims.append(int(n))
    if q:
        dims.append(int(q))
    if r:
        dims.append(int(r))
    
    if DEBUG:
        print('Dimension of distributed zeros: %d'%(len(dims)))
        print(dims)
    
    d = dmat(dims, p)
    local_size = d.local_dim

    if DEBUG:
        print('local_size:')
        print(local_size)

    # Allocating memory for the distributed matrix is no longer done
    # by @dmat/dmat.  Therefore, we can no longer use the following
    # line to get the dimensions of the local portion of the dmat
    # local_size = size(local(d));

    #   Figure out local dimensions of dmat
    #   NOTE: This is recomputing information already computed within
    #   @dmat/dmat. Is there a cleaner way of getting this information?
    #CB falls = get_local_falls(pitfalls(d), p.grid, pMATLAB.my_rank);
    #CB local_size = localdims(falls, p.dim);
    
    dim = p.dim
    g = (p.grid).shape
    if dim==2:
        for j in range(g[1]):     # i 1
            for i in range(g[0]): # j )2
                if DEBUG:
                    print('my rank: %d, Process grid rank: %d'%(GPC.my_rank,p.grid[i][j]))
                if (GPC.my_rank==p.grid[i][j]):
                    d.local = np.random.random(local_size)
                else:
                    np.random.random(local_size)
    elif dim==3:
        for k in range(g[2]):
            for j in range(g[1]):
                for i in range(g[0]):
                    if (GPC.my_rank==p.grid[i][j][k]):
                        d.local = np.random.random(local_size)
                    else:
                        np.random.random(local_size)
    elif dim==4:
        for l in range(g[3]):
            for k in range(g[2]):
                for j in range(g[1]):
                    for i in range(g[0]):
                        if (GPC.my_rank==p.grid[i][j][k][l]):
                            d.local = np.random.random(local_size)
                        else:
                            np.random.random(local_size)
    else:
        print('@MAP/RAND: Only objects up to 4 dimensions are supported.')
        exit()

    if DEBUG:
        print('type(d): %s'%(type(d)))
        print('<-- Exiting grid_rand')
    return d

    """
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    
    pMatlab: Parallel Matlab Toolbox
    Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
    Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
    MIT Lincoln Laboratory
    """

