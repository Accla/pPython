import numpy as np

from Falls import *

def local_dims(falls, dim):
    """Given the local FALLS and object dimension, calculates
    a vector of local dimensions of the distributed object.
    
    Usage:
    ------
    local_size = local_dims(falls, dim)
    
    FALLS: an array of FALLS structures for each dimension of
        the distributed object, i.e. FALLS(i) is a FALLS
        representation of the i-th dimension
    DIM: dimension of the distributed object (2, 3, or 4)
 
    LOCAL_SIZE:
        length(LOCAL_SIZE)is equal to the number of dimensions of the
        distributed object. a NumPy array
 
    Author: Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    if dim <= 4:
        # local_falls = falls;
        # compute local dimensions from the local FALLS
        # !!!NOTE: The following calculation works only if data on processor
        # RANK can be represented by a single FALLS.
        local_size = []
        if isinstance(falls[0], type(Falls())):
            for i in range(dim):
                # local size is just the local_len field of the local falls
                local_size = local_size + [int(falls[i].local_len)]
            local_size = np.array(local_size)
        else: # no local data
            local_size = np.zeros(dim,dtype='int')
    else:
        raise Exception('ERROR(local_dims): Only objects up to 4-D are supported')
    return local_size

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
