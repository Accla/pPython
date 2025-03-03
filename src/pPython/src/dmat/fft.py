import numpy as np
import scipy.fftpack 

from Dmap import *
#2022-12-08: changed to fix a TypeError: 'module' object is not callable
from ll_dmat import grid as proc_grid
from size import *
from remap import *

def fft(x, *argv):
    """
    FFT Discrete Fourier transform on a distributed matrix.
    
    FFT(X) is the discrete Fourier transform (DFT) of matrix X. The FFT
    operation is applied to each column. If the matrix X is row
    distributed, throws a warning and remaps the distributed array. Calls
    the Python fft on the local part.
    
    FFT(X,[],DIM) or FFT(X,N,DIM) applies the FFT operation across the
    dimension DIM. If the matrix is distributed along different dimension
    than DIM, throws a warning and remaps the array along appropriate
    dimension. Calls the MATLAB fft on the local part.
    
    NOTE: If the fft remaps X, returned X has a new map (different from the
    orginal map passed in).
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    
    Updates to @dmat/fft
    Changes:
    (1) Supports the fft operation on 3-D numerical arrays
    (2) If the numerical array passed into the fft is not distributed
    accordingly, remaps the array warning the user that remapping is taking
    place
    Issue to consider: Should the array be mapped to the original
    mapping after the fft is performed?
    Plus: The output is mapped the same as the input
    Minus: Significant overhead due to communication required during
    remapping
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering fft')
    
    nargin = len(argv)+1
    
    if isinstance(x,np.ndarray):
        if nargin==1:  #FFT(X)
            scipy.fftpack.fft(x)
        else:
            if isinstance(argv[0],list):
                N = x.shape[0]
            else:
                N = argv[0]
            scipy.fftpack.fft(x,N,argv[1])
    else:
        if x.dim == 2:  # distributed array is a matrix
            g = proc_grid(x)
            grid_dims = size(g)
            if nargin==1:  #FFT(X): default calling convention - fft along the columns
                N = x.local.shape[0]
                if grid_dims[0] == 1: # the matrix is broken up along the columns
                    # Only 1 processor is allocated for the entire column, use a regular fft along the column
                    x.local = scipy.fftpack.fft(x.local, N, 0)
                else: # the matrix is broken up along the rows, redistribute
                    print('WARNING: @dmat/fft: The matrix is not mapped along the appropriate dimension, remapping along columns.')
                    #>>REMAPPING CODE
                    grid_spec = [1, grid_dims[0]*grid_dims[1]]
                    old_map = x.map
                    dist_spec = old_map['dist_spec']
                    proc_list = list(g.flatten('F'))
                    #CB: now work in map equality check,  proc_list = g.flatten('F')
                    new_map = Dmap(grid_spec, dist_spec, proc_list)
                    x = remap(x,new_map)
                    #>>REMAPPING CODE
                    x.local = scipy.fftpack.fft(x.local, N, 0)

            elif nargin == 3: # FFT(X,[],DIM) or FFT(X,N,DIM) 
                if isinstance(argv[0],list):
                    N = x.local.shape[argv[1]]
                else:
                    N = argv[0]
                if argv[1]==1: #fft along the rows
                    if grid_dims[1]==1:  # Only 1 processor is allocated the entire row, use a regular fft
                        x.local = scipy.fftpack.fft(x.local, N, 1)
                    else:
                        print('@dmat/fft: The matrix is not mapped along the appropriate dimension, remapping along rows.')
                        #>>REMAPPING CODE
                        grid_spec = [grid_dims[0]*grid_dims[1], 1]
                        old_map = x.map
                        dist_spec = old_map['dist_spec']
                        proc_list = list(g.flatten('F'))
                        # Not work: proc_list = g.flatten('F')
                        new_map = Dmap(grid_spec, dist_spec, proc_list)
                        x = remap(x,new_map)
                        #>>REMAPPING CODE
                        x.local = scipy.fftpack.fft(x.local, N, 1)

                elif argv[1]==0: #fft applied to each column
                    if grid_dims[0] == 1:
                        x.local = scipy.fftpack.fft(x.local, N, 0)
                    else:
                        print('Warning: @dmat/fft: The matrix is not mapped along the appropriate dimension, remapping along columns.')
                        #>>REMAPPING CODE
                        grid_spec = [1, grid_dims[0]*grid_dims[1]]
                        old_map = x.map
                        dist_spec = old_map['dist_spec']
                        proc_list = list(g.flatten('F'))
                        # Not work: proc_list = g.flatten('F')
                        new_map = Dmap(grid_spec, dist_spec, proc_list)
                        x = remap(x,new_map)
                        #>>REMAPPING CODE
                        x.local = scipy.fftpack.fft(x.local, N, 0)
            else:
                raise Exception('@dmat/fft: Distributed fft must be called with either 1 or 3 arguments.')
    
        elif x.dim == 3: # distributed array is 3-D
            g = proc_grid(x)
            grid_dims = size(g)    
            if nargin==1: # FFT(X): default calling convention - fft along the columns
                print('3D FFT: fft(x)')
                N = x.local.shape[0]
                if grid_dims[0] == 1: # the matrix is broken up along the columns & the third dimension, but not rows
                    x.local = scipy.fftpack.fft(x.local, N, 0)
                else: # the matrix is broken up along the rows, redistribute
                    print('Warning: @dmat/fft: The matrix is not mapped along the appropriate dimension, remapping along 3-rd dimension.')
                    # >>REMAPPING CODE
                    if len(grid_dims)<3: # fill in singleton dimensions
                        grid_dims.append(1)
                    grid_spec = [1,1,grid_dims[0]*grid_dims[2]*grid_dims[3]] # map along the third dimension
                    # !!!NEED TO CHECK THAT THIS IS IN FACT THE
                    # MOST EFFICIENT MAPPING
                    old_map = x.map
                    dist_spec = old_map['dist_spec']
                    proc_list = list(g.flatten('F'))
                    # Not work: proc_list = g.flatten('F')
                    new_map = Dmap(grid_spec, dist_spec, proc_list)
                    x = remap(x,new_map)
                    # >>REMAPPING CODE
                    x.local = scipy.fftpack.fft(x.local, N, 0)
                end
            elif nargin == 3: # FFT(X,[],DIM)
                if isinstance(argv[0],list):
                    N = x.local.shape[argv[1]]
                else:
                    N = argv[0]
                if argv[1]==1: #fft along the rows
                    print('3D FFT: fft(x, [], 1)')
                    if grid_dims[2] == 1: # the matrix is broken up along the rows & the third dimension, but not columns
                        x.local = scipy.fftpack.fft(x.local, N, 1)
                    else: # the matrix is broken up along the columns, redistribute
                        print('Warning: @dmat/fft: The matrix is not mapped along the appropriate dimension, remapping along 3-rd dimension.')
                        # >>REMAPPING CODE
                        if len(grid_dims)<3: # fill in singleton dimensions
                            grid_dims.append(1)
                        grid_spec = [1, 1, grid_dims[0]*grid_dims[2]*grid_dims[3]] # map along the third dimension
                        # !!!NEED TO CHECK THAT THIS IS IN FACT THE
                        # MOST EFFICIENT MAPPING
                        old_map = x.map
                        dist_spec = old_map['dist_spec']
                        proc_list = list(g.flatten('F'))
                        # Not work: proc_list = g.flatten('F')
                        new_map = Dmap(grid_spec, dist_spec, proc_list)
                        x = remap(x,new_map)
                        # >>REMAPPING CODE
                        x.local = scipy.fftpack.fft(x.local, N, 1)
                elif argv[1]==0: # fft applied to each column
                    print('3D FFT: fft(x, [], 0)')
                    if grid_dims[0] == 1: # the matrix is broken up along the columns & the third dimension, but not rows
                        x.local = scipy.fftpack.fft(x.local, N, 0)
                    else: # the matrix is broken up along the rows, redistribute
                        print('Warning: @dmat/fft: The matrix is not mapped along the appropriate dimension, remapping along 3-rd dimension.')
                        # >>REMAPPING CODE
                        if len(grid_dims)<3: # fill in singleton dimensions
                            grid_dims.append(1)
                        grid_spec = [1,1,grid_dims[0]*grid_dims[2]*grid_dims[3]] # map along the third dimension
                        # !!!NEED TO CHECK THAT THIS IS IN FACT THE
                        # MOST EFFICIENT MAPPING
                        old_map = x.map
                        dist_spec = old_map['dist_spec']
                        proc_list = list(g.flatten('F'))
                        # Not work: proc_list = g.flatten('F')
                        new_map = Dmap(grid_spec, dist_spec, proc_list)
                        x = remap(x,new_map)
                        # >>REMAPPING CODE
                        x.local = scipy.fftpack.fft(x.local, N, 0)
        else:
            raise Exception('dmat/src/fft: FFT can only be applied to matrices or 3-D arrays.')
    
    if DEBUG:
        print('<-- Exiting fft')
    return x

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

