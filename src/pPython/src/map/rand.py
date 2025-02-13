import numpy as np

import pPython as GPC
from Dmap import *
from Dmat import *

def rand(*array_sizes, **keywords):
    """
    Rand distributed array.

    Input:
        array_sizes: array sizes 
        keywords: 
            'dmap': 1 or distributed map, Dmap object
            'dtype': data type of array element

    Distributed array of random numbers between 0 and 1 distributed uniformly.
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
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering rand')
    
    # form dims vector
    if isinstance(array_sizes[0],list):
        ndim = len(array_sizes[0])
        dims = array_sizes[0]
    else:
        ndim = len(array_sizes)
        dims = []
        for i in range(ndim):
            dims.append(array_sizes[i])
    if DEBUG:
        print('Dimension of distributed zeros: %d'%(len(dims)))
        print(array_sizes)
        print(dims)

    if ndim>4:
        raise Exception('ERROR(zeros): array dimension larger than 4-D is not supported')

    dmap = None
    if 'map' in keywords:
        if isinstance(keywords['map'], Dmap):
            dmap = keywords['map']
        elif isinstance(keywords['map'], int):
            dmap = 1

    dtype = np.float64
    if 'dtype' in keywords:
        dtype = keywords['dtype']

    if not isinstance(dmap,Dmap):
        if DEBUG:
            print('<-- Exiting rand with non-Dmat array')
        d = np.random.random(dims)
        return d
    
    d = Dmat(None, dtype, dims, map=dmap)
    local_size = d.local_dim

    if DEBUG:
        print('local_size:')
        print(local_size)

    # Allocating memory for the distributed matrix is no longer done
    # by @dmat/dmat.  Therefore, we can no longer use the following
    # line to get the dimensions of the local portion of the Dmat
    # local_size = size(local(d));

    #   Figure out local dimensions of Dmat
    #   NOTE: This is recomputing information already computed within
    #   @dmat/dmat. Is there a cleaner way of getting this information?
    #CB falls = get_local_falls(dpitfalls(d), p.grid, pMATLAB.my_rank);
    #CB local_size = localdims(falls, p.dim);
    
    dim = dmap['dim']
    g = (dmap['grid']).shape
    if dim==2:
        for j in range(g[1]):     # i 1
            for i in range(g[0]): # j 2
                if DEBUG:
                    print('my rank: %d, Process grid rank: %d'%(GPC.Pid,dmap['grid'][i][j]))
                if (GPC.Pid==dmap['grid'][i][j]):
                    d.local = np.random.random(local_size)
                else:
                    np.random.random(local_size)
    elif dim==3:
        for k in range(g[2]):
            for j in range(g[1]):
                for i in range(g[0]):
                    if (GPC.Pid==dmap['grid'][i][j][k]):
                        d.local = np.random.random(local_size)
                    else:
                        np.random.random(local_size)
    elif dim==4:
        for l in range(g[3]):
            for k in range(g[2]):
                for j in range(g[1]):
                    for i in range(g[0]):
                        if (GPC.Pid==dmap['grid'][i][j][k][l]):
                            d.local = np.random.random(local_size)
                        else:
                            np.random.random(local_size)
    else:
        raise Exception('@MAP/RAND: Only objects up to 4 dimensions are supported.')

    if DEBUG:
        print('type(d): %s'%(type(d)))
        print('<-- Exiting rand')
    return d

########################################################
# pMatlab: Parallel Matlab Toolbox
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2005, Massachusetts Institute of Technology All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#      * Neither the name of the Massachusetts Institute of Technology nor
#        the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written
#        permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
