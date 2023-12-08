from Dmat import *
from size import *

def global_ind(d, dim=None):
    """Returns the global indices of the distributed array D local to 
    the current processor in the specified dimension, DIM.
    
    Usage:
    ------
    local_ind = global_ind(d,dim=None)
    
    D: distributed array
    dim: dimension of the distributed array D. 
        A scalar or list containing the desired dimension axis.
    local_ind: a list (in order to support a string ':' element 
        representting the full indices of the given dimension)
 
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering global_ind')
        
    if dim == None:
        # no dim provided. returns for all dimension
        if DEBUG:
            print('no dim')
        dims = list(range(len(d.shape)))
    else:
        if DEBUG:
            print('provided dim')
        if isinstance(dim,int):
            dims = []
            dims.append(dim)
        else:
            dims = dim

    if isinstance(d,Dmat): 
        #
        # distributed array
        #
        my_inds = d.global_ind
        s = d.shape
        if DEBUG:
            print('my_inds:')
            print(my_inds)
            print('d.shape:')
            print(s)
    
        if len(dims)==1:
            # Change due to switching from list to tuple of ranges
            # Select the 1st range element in the tuple
            local_ind = list(my_inds[dims[0]][0])
        else:
            local_ind = []
            for i in range(len(dims)):
                # Change due to switching from list to tuple of ranges
                # Select the 1st range element in the tuple
                local_ind.append(list(my_inds[dims[i]][0]))
    else:
        #
        # non-distributed array
        # 
        my_inds = size(d)
        if len(my_inds) == 1:
            # 1-D array (even if array construct was 2-D)
            local_ind = list(range(my_inds[0]))
        else:
            if len(dims)==1:
                local_ind = list(range(my_inds[dims[0]]))
            else:
                local_ind = []
                for i in range(len(dims)):
                    local_ind.append(list(range(my_inds[dims[i]])))

    if DEBUG:
        print('<-- Exiting global_ind')
    return local_ind

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
