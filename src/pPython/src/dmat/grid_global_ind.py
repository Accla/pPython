from get_local_falls import *
from get_global_ind import *

def grid_global_ind(d):
    """Returns global index array for the processor grid.

    Refactored the first part in global_block_ranges() for the Dmat class
    Returns global_ind

    Author: Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    # dimension of the distributed object
    dim = len(d.pitfalls)

    # processor grid on which the object is distributed
    grid = d.map['grid']

    grid_dims = list(grid.shape)
    # Fill up if missing dimension
    if len(grid_dims)<dim:
        for i in range((len(grid_dims)+1),dim+1):
            grid_dims.append(1)

    if dim==2:
        # get local indices for each processor in the grid
        global_ind = dict()
        for i in range(grid_dims[0]):
            global_ind[i] = dict()
            for j in range(grid_dims[1]):
                local_falls = get_local_falls(d.pitfalls, grid, grid[i,j])
                global_ind[i][j] = get_global_ind(local_falls, grid_dims)
    elif dim==3:
        # get local indices for each processor in the grid
        for i in range(grid_dims[0]):
            for j in range(grid_dims[1]):
                for k in range(grid_dims[2]):
                    local_falls = get_local_falls(d.pitfalls, grid, grid[i,j,k])
                    global_ind[i][j][k] = get_global_ind(local_falls, grid_dims)
    elif dim==4:
        # get local indices for each processor in the grid
        for i in range(grid_dims[0]):
            for j in range(grid_dims[1]):
                for k in range(grid_dims[2]):
                    for m in range(grid_dims[3]):
                        local_falls = get_local_falls(d.pitfalls, grid, grid[i,j,k,m])
                        global_ind[i][j][k][m] = get_global_ind(local_falls, grid_dims)
    else:
        raise Exception('GLOBAL_BLOCK_RANGES: Only objects up to 4-D are supported')
        
    return global_ind

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
