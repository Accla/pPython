from multipledispatch import dispatch
import numpy as np

from Dmat import *

#
# For np.ndarray type variables
#

@dispatch(np.ndarray)
def global_block_range(d):
    """Returns the range of indices in the specified dimension.
    
    Usage:
    ------
    ind = GLOBAL_BLOCK_RANGE(D) 
    
    d: a DOUBLE.
    ind: an array containing index range boundary for all dimensions
    
    One of the functions that mimics the parallel library behavior on
    non-distributed arrays.
 
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun

    """
    
    dims = []
    for i in range(len(d.shape)):
        dims.append(i)

    return global_block_range(d, dims)


@dispatch(np.ndarray,int)
def global_block_range(d, dim):
    """Returns the range of indices in the specified dimension.
    
    Usage:
    ------
    ind = GLOBAL_BLOCK_RANGE(D, dim) 
    
    d: a DOUBLE.
    dim: an integer from range(max. dimension)
    ind: an array containing index range boundary for given dimension
    
    One of the functions that mimics the parallel library behavior on
    non-distributed arrays.
 
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun

    """
    
    dims = []
    dims.append(dim)
        
    return global_block_range(d, dims)


@dispatch(np.ndarray,list)
def global_block_range(d, dims):
    """Returns the range of indices in the specified dimension.
    
    Usage:
    ------
    ind = GLOBAL_BLOCK_RANGE(D, dims=None) 
    
    d: a DOUBLE.
    dims: a list of dimension or dimensions
    ind: an array containing index range boundary for given list
    
    One of the functions that mimics the parallel library behavior on
    non-distributed arrays.
 
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun

    """
    
    ind = np.zeros((len(dims),2),int)
    my_inds = list(d.shape)
    # print(my_inds)
    
    for i in range(len(dims)):
        # For python, index ranges from 0 to N-1
        # print(dims[i])
        ind[i,1] = my_inds[dims[i]]-1
        
    return ind

#
# For distributed array type (Dmat) variables
#

@dispatch(type(Dmat(None,np.float64)))
def global_block_range(d):
    """Returns the ranges of global indices local to the current processor.
    
    Usage:
    ------
    ind = GLOBAL_BLOCK_RANGE(D) 
    
    GLOBAL_BLOCK_RANGE(D) Returns the global index range of the 
        distributed array D local to the current processor in all 
        dimensions.
        
    d: a distributed array.
    ind: an array containing index range boundary for given dimension
    
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun
    
    """

    dims = []
    for i in range(len(d.shape)):
        dims.append(i)

    return global_block_range(d, dims)


@dispatch(type(Dmat(None,np.float64)),int)
def global_block_range(d, dim):
    """Returns the ranges of global indices local to the current processor.
    
    Usage:
    ------
    ind = GLOBAL_BLOCK_RANGE(D, dim) 
    
    GLOBAL_BLOCK_RANGE(D, DIM) Returns the global index range of the 
        distributed array D local to the current processor in the 
        specified dimension, DIM.
        
    d: a DOUBLE.
    dim: an integer for a specfic dimension
    ind: an array containing index range boundary for given dimension
    
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun
    
    """

    dims = []
    dims.append(dim)
        
    return global_block_range(d, dims)


@dispatch(type(Dmat(None,np.float64)),list)
def global_block_range(d, dims):
    """Returns the ranges of global indices local to the current processor.
    
    Usage:
    ------
    ind = GLOBAL_BLOCK_RANGE(D, dim) 
    
    GLOBAL_BLOCK_RANGE(D, DIM) Returns the global index range of the 
        distributed array D local to the current processor in the 
        specified dimension, DIM.
        
    d: a DOUBLE.
    dims: a list for a specfic dimension or all dimensions
    ind: an array containing index range boundary for given dimension[s]
    
    Author:   Nadya Travinin
    Pytthon version: Dr. Chansup Byun
    
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering global_block_range')

    my_inds = d.global_ind
    """
    global_ind is a dictionary such as {0: [0, 1, 2, 3], 1: [0, 1, 2]}
    """
    myLocalLenghs = [d.falls[i].local_len  for i in range(len(d.falls))  ]

    """
    d.falls: a list of len(dims)
    """
    s = d.shape
    
    ind = np.zeros((len(dims),2),int)

    if (all(myLocalLenghs) == 0):
        ind = None
    else:
        for i in range(len(dims)):
            # For python, index ranges from 0 to N-1
            # print(dims[i])
            if DEBUG:
                print(my_inds[dims[i]])
            # Change due to switch from list to tupler of ranges
            # pick up the first and the last indices from the 1st range element in the tuple
            ind[i,0] = my_inds[dims[i]][0][0]
            ind[i,1] = my_inds[dims[i]][0][-1]

    if DEBUG:
        print('<-- Exiting global_block_range')

    return ind

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
