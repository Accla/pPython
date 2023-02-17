import numpy as np

from get_local_falls import *
from get_global_ind import *

def reconstruct(pitfalls, grid, temp_mat, mat_size):
    """Given collected distributed data in grid layout, reconstructs the original  
    object according to data distribution. If the original distribution was BLOCK, 
    the grid layout is the original layout.
 
    Also returns reconstructed matrix in the same format as the distributed
    matrix, i.e. full distributed matrices are returned as full matrices
    and sparse distributed matrices are returned as sparse matrices.
 
    MAT_SIZE: the array describing the dimensions of the distributed
        object.
 
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering reconstruct')

    # dimension of the distributed object
    dim = len(pitfalls)
    # convert tuple to list in case expanding dimension
    grid_dims = list(grid.shape)
    if len(grid_dims)<dim:
        for i in range((len(grid_dims)+1),dim):
            grid_dims.append(0)
    
    # Determine if the matrix to be reconstructed is a sparse or dense matrix
    """

    if (issparse(temp_mat{1,1}))
        # At this point we do not know how many non-zero values the overall
        # sparse distributed matrix contains, so we set it to 0 and let
        # Matlab take care of allocating memory  
        mat = spalloc(mat_size(1), mat_size(2), 0);
    else
     
    """

    if dim==2:
        # Get the datatype of temp_mat (additional in pPython)
        for ikey in temp_mat.keys():
            ival = temp_mat[ikey]
            ikeys = temp_mat.keys()
            for jkey in ival.keys():
                jval = ival[jkey]
                jkeys = ival.keys()
                dtype = type(jval[0,0])
                if DEBUG:
                    print('dtype, %s, at ikey,jkey = %s,%s'%(dtype,ikey,jkey))
                    print('jval:')
                    print(jval)
                break
            break
        # Create a zeros array of the same type as temp_mat
        mat = np.zeros(mat_size,dtype)
        if DEBUG:
            print('mat size: %s'%(str(mat_size)))
            print('type(mat): %s'%(type(mat)))
            print('type(mat[0,0]): %s'%(type(mat[0,0])))

        # get local indices for each processor in the grid
        my_global_ind = dict()
        for i in range(grid_dims[0]):
            my_global_ind[i] = dict()
            for j in range(grid_dims[1]):
                local_falls = get_local_falls(pitfalls, grid, grid[i][j])
                my_global_ind[i][j] = get_global_ind(local_falls, grid_dims)

        # !!!FOR NOW - assume MAT is of type DOUBLE
        i = 0
        for ikey in ikeys:
            j = 0
            for jkey in jkeys:
                if temp_mat[ikey][jkey].any() != 0.0:
                    # Change due to switch from list to tuple of ranges
                    # Select the 1st range element in the tuple
                    ii = my_global_ind[i][j][0][0]
                    jj = my_global_ind[i][j][1][0]
                    if DEBUG:
                        print('mat index: ii,jj = %d,%d'%(len(ii),len(jj)))
                        print('temp_mat keys: ikey,jkey = %s,%s'%(ikey,jkey))
                        print(ii)
                        print(jj)
                        print(temp_mat[ikey][jkey])
                    mat[ii[0]:ii[-1]+1,jj[0]:jj[-1]+1] = temp_mat[ikey][jkey]
                j +=1
            i +=1
    elif dim==3:
        # Get the datatype of temp_mat (additional in pPython)
        for ikey in temp_mat.keys():
            ival = temp_mat[ikey]
            ikeys = temp_mat.keys()
            for jkey in ival.keys():
                jval = ival[jkey]
                jkeys = ival.keys()
                for kkey in jval.keys():
                    kval = jval[kkey]
                    kkeys = jval.keys()
                    dtype = type(kval[0,0,0])
                    if DEBUG:
                        print('dtype, %s, at ikey,jkey,kkey = %s,%s,%s'%(dtype,ikey,jkey,kkey))
                        print('kval:')
                        # print(kval)
                    break
                break
            break
        # Create a zeros array of the same type as temp_mat
        mat = np.zeros(mat_size,dtype)
        if DEBUG:
            print('mat size: %s'%(str(mat_size)))
            print('type(mat): %s'%(type(mat)))
            print('type(mat[0,0,0]): %s'%(type(mat[0,0,0])))

        # get local indices for each processor in the grid
        my_global_ind = dict()
        for i in range(grid_dims[0]):
            my_global_ind[i] = dict()
            for j in range(grid_dims[1]):
                my_global_ind[i][j] = dict()
                for k in range(grid_dims[2]):
                    local_falls = get_local_falls(pitfalls, grid, grid[i][j][k])
                    my_global_ind[i][j][k] = get_global_ind(local_falls, grid_dims)

        # !!!FOR NOW - assume MAT is of type DOUBLE
        i = 0
        for ikey in ikeys:
            j = 0
            for jkey in jkeys:
                k = 0
                for kkey in kkeys:
                    if temp_mat[ikey][jkey][kkey].any() != 0.0:
                        # Change due to switch from list to tuple of ranges
                        # Select the 1st range element in the tuple
                        ii = my_global_ind[i][j][k][0][0]
                        jj = my_global_ind[i][j][k][1][0]
                        kk = my_global_ind[i][j][k][2][0]
                        if DEBUG:
                            print('mat index: ii,jj,kk = %d,%d,%d'%(len(ii),len(jj),len(kk)))
                            print('temp_mat keys: ikey,jkeykkey = %s,%s,%s'%(ikey,jkey,kkey))
                            print(ii)
                            print(jj)
                            print(kk)
                            # print(temp_mat[ikey][jkey][kkey])
                        mat[ii[0]:ii[-1]+1,jj[0]:jj[-1]+1,kk[0]:kk[-1]+1] = temp_mat[ikey][jkey][kkey]
                    k +=1
                j +=1
            i +=1

    elif dim==4:
        print('RECONSTRUCT: Implemented for 4-D support but not tested yet.');
        # Get the datatype of temp_mat (additional in pPython)
        for ikey in temp_mat.keys():
            ival = temp_mat[ikey]
            ikeys = temp_mat.keys()
            for jkey in ival.keys():
                jval = ival[jkey]
                jkeys = ival.keys()
                for kkey in jval.keys():
                    kval = jval[kkey]
                    kkeys = jval.keys()
                    for mkey in kval.keys():
                        mval = kval[mkey]
                        mkeys = kval.keys()
                        dtype = type(mval[0,0,0,0])
                        if DEBUG:
                            print('dtype, %s, at ikey,jkey,kkey = %s,%s,%s,%s'%(dtype,ikey,jkey,kkey,mkey))
                            print('mval:')
                            # print(mval)
                        break
                    break
                break
            break
        # Create a zeros array of the same type as temp_mat
        mat = np.zeros(mat_size,dtype)
        if DEBUG:
            print('mat size: %s'%(str(mat_size)))
            print('type(mat): %s'%(type(mat)))
            print('type(mat[0,0,0,0]): %s'%(type(mat[0,0,0,0])))

        # get local indices for each processor in the grid
        my_global_ind = dict()
        for i in range(grid_dims[0]):
            my_global_ind[i] = dict()
            for j in range(grid_dims[1]):
                my_global_ind[i][j] = dict()
                for k in range(grid_dims[2]):
                    my_global_ind[i][j][k] = dict()
                    for m in range(grid_dims[3]):
                        local_falls = get_local_falls(pitfalls, grid, grid[i][j][k][m])
                        my_global_ind[i][j][k][m] = get_global_ind(local_falls, grid_dims)

        # !!!FOR NOW - assume MAT is of type DOUBLE
        i = 0
        for ikey in ikeys:
            j = 0
            for jkey in jkeys:
                k = 0
                for kkey in kkeys:
                    m = 0
                    for mkey in mkeys:
                        if temp_mat[ikey][jkey][kkey][mkey].any() != 0.0:
                            # Change due to switch from list to tuple of ranges
                            # Select the 1st range element in the tuple
                            ii = my_global_ind[i][j][k][m][0][0]
                            jj = my_global_ind[i][j][k][m][1][0]
                            kk = my_global_ind[i][j][k][m][2][0]
                            ll = my_global_ind[i][j][k][m][3][0]
                            if DEBUG:
                                print('mat index: ii,jj,kk,mm = %d,%d,%d,%d'%(len(ii),len(jj),len(kk),len(mm)))
                                print('temp_mat keys: ikey,jkeykkey,mkey = %s,%s,%s,%s'%(ikey,jkey,kkey,mkey))
                                print(ii)
                                print(jj)
                                print(kk)
                                print(mm)
                                # print(temp_mat[ikey][jkey][kkey][mkey])
                            mat[ii[0]:ii[-1]+1,jj[0]:jj[-1]+1,kk[0]:kk[-1]+1,mm[0]:mm[-1]+1] = temp_mat[ikey][jkey][kkey][mkey]
                        m +=1
                    k +=1
                j +=1
            i +=1
    else:
        print('RECONSTRUCT: Only objects up to 4-D are supported');

    if DEBUG:
        print('<-- Exiting reconstruct')
    return mat

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
