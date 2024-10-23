import numpy as np

from Dmap import *
from Dmat import *

def ones(*array_sizes, **keywords):
    """
    Zeros distributed array.

    Input:
        array_sizes: array sizes 
        keywords: 
            'dmap': 1 or distributed map, Dmap object
            'dtype': data type of array element
    
    NOTE: DIMENSION OF THE DISTRIBUTED ARRAY MUST BE CONSISTENT WITH THE
        DIMENSION OF THE MAP.
        
    ZEROS(N, P) If N is scalar, an N by N distributed matrix of
        ones mapped according to the map specified by P; if N is a vector
        (numpy array), a distributed matrix with dimensions specified by N
        mapped according to P.
    ZEROS(M, N, P) M by N distributed matrix of ones mapped according to the
        map specified by P.
    ZEROS(M, N, Q, P) MxNxQ distributed array of ones mapped according to
        the map specified by P.
    ZEROS(M, N, Q, R, P) MxNxQxR distributed array of ones mapped according to
        the map specified by P.
    ZEROS(M, N, ..., P, TYPE) MxNx... distributed array of ones of datatype
        TYPE mapped according to the map specified by P.
 
    Example:
           Create a 100x10 Dmat of 8-bit signed integers
           p = Dmap([1,Ncpus], {}, range(Ncpus))
           x = ones(100, 10, map=p, dtype=int8)
 
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    Python version: Dr. Chansup Byun (cbyun@ll.mit.edu)
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering ones')

    #
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
        print('Dimension of distributed ones: %d'%(len(dims)))
        print(array_sizes)
        print(dims)

    if ndim>4:
        raise Exception('ERROR(ones): array dimension larger than 4-D is not supported')

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
        d = np.ones(dims, dtype)
        return d
    
    if len(dims) < 5:
        d = Dmat(None, dtype, dims, map=dmap)
    else:
        print('ERROR(map/ones): Incorrect number of inputs')

    # Figure out local dimensions of Dmat
    # NOTE: This is recomputing information already computed within
    # @dmat/dmat. Is there a cleaner way of getting this information?
    # comm = my_MCW.MPI_COMM_WORLD
    # my_rank = MPI_Comm_rank(comm)
    
    if DEBUG:
        # print('ones: my_rank = %d'%(my_rank))
        print(d.pitfalls)
        print(dpitfalls(d))
    
    # falls = get_local_falls(dpitfalls(d), p.grid, my_rank)
    # local_dims = localdims(falls, p.dim);

    # Allocating memory for the distributed matrix is no longer done
    # by @dmat/dmat.

    # Allocate a ones matrix for the local portion of the Dmat
    # Determine Matlab version

    d.local = np.ones(d.local_dim, dtype)

    if DEBUG:
        print('<-- Exiting ones')
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
