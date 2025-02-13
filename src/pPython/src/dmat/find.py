from multipledispatch import dispatch
import numpy as np

from MPI_Send import *
from MPI_Recv import *

import pPython as GPC
from inmap import *
from size import *

DEBUG = 0

def find(x):
    """
    FIND Find indices of nonzero elements of a Dmat object.
         Replaced by np.where for regular np.array
    
    [I,J] = FIND(X) returns the row and column indices of nonzero elements
    of the distributed matrix X.
    NOTE: Currently supports only [i,j] = find(x) calling convention.
    Only works on 2D arrays.
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    
    """
    if DEBUG:
        print('--> Entering find for a Dmat object')
        print('... find for a distributed array')
    # increment tag
    GPC.tag_num = GPC.tag_num+1
    GPC.tag = 'tag-'+str(GPC.tag_num)
    
    if inmap(x.map, GPC.Pid):
        local_ij = np.argwhere(x.local)
        # Note: local_ij[:,0] -> local_i, local_ij[:,1] -> local_j
        if isinstance(x.global_ind[0], str):
            if x.global_ind[0] == ':':
                # Send range() instead of list to save memory
                x.global_ind[0] = range(x.shape[0]+1)
        if isinstance(x.global_ind[1], str):
            if x.global_ind[1] == ':':
                x.global_ind[1] = range(x.shape[1]+1)
        
        # When a processor is allocated a single row (column), x.global_ind[0]
        # (x.global_ind[1]) contain a 1x1 matrix.  Since local_i and local_j
        # are
        # column vectors, global_i (global_j) will contain a column vector.
        # Transpose local_i and local_j so that global_i and global_j are row
        # vectors.
        local_i = np.array(local_ij[:,0])
        local_j = np.array(local_ij[:,1])
        if DEBUG:
            print('local_i')
            print(local_i)
            print('x.global_ind[0]')
            print(x.global_ind[0])
        # Change due to switch from list to tuple of range
        # Select the first element of range lists in the tuple, x.global_ind[0][0], for the 1st dimension
        global_i = np.array(list(x.global_ind[0][0]))[local_i]
        global_j = np.array(list(x.global_ind[1][0]))[local_j]
        
        data = []
        data.append(global_i)
        data.append(global_j)
        temp = dict()
    
        grid_size = size(x.map['grid'])
        #grid_size(1) - number of grid rows, grid_size(2) - number of grid cols
        #send local finds to everyone
        for d1 in range(grid_size[0]):
            for d2 in range(grid_size[1]):
                if (GPC.Pid != x.map['grid'][d1,d2]):
                    MPI_Send(x.map['grid'][d1,d2], GPC.tag, GPC.comm, data)

        #receive finds from everyone
        for d1 in range(grid_size[0]):
            if d1 not in temp:
                temp[d1] = dict()
            for d2 in range(grid_size[1]):
                if DEBUG:
                    print("x.map['grid'][d1, d2]")
                    print(x.map['grid'][d1,d2])
                if (GPC.Pid != x.map['grid'][d1,d2]):
                    [temp[d1][d2]] = MPI_Recv(x.map['grid'][d1,d2], GPC.tag, GPC.comm)
                else:
                    temp[d1][d2] = data
        i = []
        j = []
        for d2 in range(grid_size[1]): #grid cols
            for d1 in range(grid_size[0]): #grid rows
                if (GPC.Pid != x.map['grid'][d1,d2]):
                    if len(temp[d1][d2][0])>0:
                        i = i+list(temp[d1][d2][0])
                        j = j+list(temp[d1][d2][1])
                else:
                    if len(data[0])>0:
                        i = i+list(data[0])
                        j = j+list(data[1])
        #transpose outputs since MATLAB find returns column vectors
        # No need to transpose: i = i'
        # No need to transpose: j = j'
    else:
        i = []
        j = []
    if DEBUG:
        print('<-- Exiting find')
    return [i,j]

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

