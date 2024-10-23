import numpy as np

def get_local_ind(global_ind, ind):
    """
    get_local_ind returns a dictionary array of local indices given an array of
    global indices on the current processor and an array of global indices
    that are being referenced.
    
    GET_LOCAL_IND(GLOBAL_IND, IND)
    GLOBAL_IND - a dictionary with numeric key of length equal to the number of dimensions.
    Each entry in the array specifies the global indices in the i-th
    dimension stored on the current processor.
    
    IND - a dictionary of length equal to the number of dimensions, where each
    entry specifies the global indices being referenced in that
    dimension.
    
    Returns LOCAL_IND:
    len(LOCAL_IND) is equal to the number of dimensions of the distributed object. 
    LOCAL_IND[i] is of the form [ind1 ind2 ind3 ...] where ind_i is a
    local index of the data stored locally.
    
    LOCAL_IND is a Python dictionary with the numeric key for each dimension
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Enterintering get_local_ind')
        print('global_ind & ind')
        print(global_ind)
        print(ind)

    local_ind = dict()
    dim = len(ind)
    if dim <= 4: # number of dimensions of the distributed object is 4 or less
        for i in range(dim):
            local_ind[i] = []
            if global_ind[i] == ':': 
                # dimension i is not distributed
                loc_inds = ind[i]
            else:  
                # dimension i is distributed
                if ind[i] == ':':
                    loc_inds = ':'
                else:
                    if isinstance(ind[i],slice):
                        # Convert to a list of index from a slice object
                        ind_list = list(range(ind[i].stop)[ind[i]])
                    else:
                        # assuming it is a list already
                        ind_list = ind[i]
                    # PRESERVES THE ORDERING OF INDICES
                    loc_inds = []
                    #  vvvvv new code vvvvv
                    [vals, i_global, i_ind] = np.intersect1d(global_ind[i], ind_list, return_indices=True)
                    i_ind_sorted = np.argsort(i_ind)
                    ind_sorted = i_ind[i_ind_sorted]
                    loc_inds = i_global[i_ind_sorted]
                    if (len(loc_inds) == 0):
                        loc_inds = []
                    #  ^^^^^ new code ^^^^^
                # dimension i is distributed
            local_ind[i] = loc_inds
    else:  # number of dimensions is greater than 4
        raise Exception('localdims: Only objects up to 4-D are supported')
        # number of dimensions is greater than 4    

    if DEBUG:
        print('local_ind')
        print(local_ind)
        print('<-- Exiting get_local_ind')
    
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
