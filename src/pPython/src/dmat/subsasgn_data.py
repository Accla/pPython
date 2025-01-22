from get_global_ind import *
from get_local_ind import *

def subsasgn_data(a, b, falls_index, fi):
    """
    SUBSASGN_DATA Helper function for distributed array subsasgn.
    
    SUBSASGN_DATA(A, B, FALLS_INDEX, FI) Computes which data to send from
    distributed array B to distributed array A based on falls intersection FI.
    
    a,b: distributed arrays
    fi: a dictionary based on the dimension
    
    data, a_local_ind: dictionary variables with numeric key
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering subsasgn_data')
    
    # dimension of the distributed object
    dim = len(fi)
    
    data = dict()
    a_local_ind = dict()
    
    if dim==2:
        num_data=0
        for f1 in range(len(fi[0][falls_index])):
            for f2 in range(len(fi[1][falls_index])):
                fi_temp = []
                fi_temp.append(fi[0][falls_index][f1])
                fi_temp.append(fi[1][falls_index][f2])
                g_ind = get_global_ind(fi_temp)
                b_local_ind = get_local_ind(b.global_ind, g_ind)
                if DEBUG:
                    print('b.local')
                    print(b.local)
                    print('b_local_ind')
                    print(b_local_ind)
                if len(b_local_ind[0])>0 and len(b_local_ind[1])>0:
                    # Different behavior as compared to Matlab: data[num_data] = b.local[b_local_ind[0], b_local_ind[1]]
                    data[num_data] = b.local[slice(b_local_ind[0][0],b_local_ind[0][-1]+1),slice(b_local_ind[1][0],b_local_ind[1][-1]+1)]
                else:
                    # Workaround for Matlab, which still works with empty index
                    data[num_data] = None
                a_local_ind[num_data] = get_local_ind(a.global_ind, g_ind)
                num_data=num_data+1

    elif dim==3:
        num_data=0
        for f1 in range(len(fi[0][falls_index])):
            for f2 in range(len(fi[1][falls_index])):
                for f3 in range(len(fi[2][falls_index])):
                    fi_temp = []
                    fi_temp.append(fi[0][falls_index][f1])
                    fi_temp.append(fi[1][falls_index][f2])
                    fi_temp.append(fi[2][falls_index][f3])
                    g_ind = get_global_ind(fi_temp)
                    b_local_ind = get_local_ind(b.global_ind, g_ind)
                    if len(b_local_ind[0])>0 and len(b_local_ind[1])>0 and len(b_local_ind[2])>0:
                        # Workaround for Matlab, which still works with empty index
                        data[num_data] = b.local[slice(b_local_ind[0][0],b_local_ind[0][-1]+1), slice(b_local_ind[1][0],b_local_ind[1][-1]+1), slice(b_local_ind[2][0],b_local_ind[2][-1]+1)]
                    else:
                        # Workaround for Matlab, which still works with empty index
                        data[num_data] = None
                    a_local_ind[num_data] = get_local_ind(a.global_ind, g_ind)
                    num_data=num_data+1

    elif dim==4:
        num_data=0
        for f1 in range(len(fi[0][falls_index])):
            for f2 in range(len(fi[1][falls_index])):
                for f3 in range(len(fi[2][falls_index])):
                    for f4 in range(len(fi[3][falls_index])):
                        fi_temp = []
                        fi_temp.append(fi[0][falls_index][f1])
                        fi_temp.append(fi[1][falls_index][f2])
                        fi_temp.append(fi[2][falls_index][f3])
                        fi_temp.append(fi[3][falls_index][f4])
                        g_ind = get_global_ind(fi_temp)
                        b_local_ind = get_local_ind(b.global_ind, g_ind)
                        if len(b_local_ind[0])>0 and len(b_local_ind[1])>0 and len(b_local_ind[2])>0 and len(b_local_ind[3])>0:
                            # Workaround for Matlab, which still works with empty index
                            data[num_data] = b.local[slice(b_local_ind[0][0],b_local_ind[0][-1]+1), slice(b_local_ind[1][0],b_local_ind[1][-1]+1), slice(b_local_ind[2][0],b_local_ind[2][-1]+1), slice(b_local_ind[3][0],b_local_ind[3][-1]+1)]
                        else:
                            # Workaround for Matlab, which still works with empty index
                            data[num_data] = None
                        a_local_ind[num_data] = get_local_ind(a.global_ind, g_ind)
                        num_data=num_data+1
    else:
        raise Exception('DMAT/SUBSASGN_DATA: Only objects up to four (4) dimensions are supported.')

    if DEBUG:
        print('<-- Exiting subsasgn_data')
    return  [data, a_local_ind]
 
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

