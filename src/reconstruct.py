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
        # Get the datatype of temp_mat
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
            my_global_ind[str(i)] = dict()
            for j in range(grid_dims[1]):
                local_falls = get_local_falls(pitfalls, grid, grid[i][j])
                my_global_ind[str(i)][str(j)] = get_global_ind(local_falls, grid_dims)

        # !!!FOR NOW - assume MAT is of type DOUBLE
        # for i in range(grid_dims[0]):
        #     for j in range(grid_dims[1]):
        i = 0
        for ikey in ikeys:
            j = 0
            for jkey in jkeys:
                if temp_mat[ikey][jkey].any() != 0.0:
                    ii = my_global_ind[str(i)][str(j)][str(0)]
                    jj = my_global_ind[str(i)][str(j)][str(1)]
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
        # Get the datatype of temp_mat
        for ikey in temp_mat.keys():
            ival = temp_mat[ikey]
            ikeys = temp_mat.keys()
            for jkey in ival.keys():
                jval = ival[jkey]
                jkeys = ival.keys()
                for kkey in jval.keys():
                    kval = jval[kkey]
                    kkeys = jval.keys()
                    dtype = type(kval[0,0])
                    if DEBUG:
                        print('dtype, %s, at ikey,jkey,kkey = %s,%s'%(dtype,ikey,jkey,kkey))
                        print('kval:')
                        print(kval)
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
            my_global_ind[str(i)] = dict()
            for j in range(grid_dims[1]):
                my_global_ind[str(i)][str(j)] = dict()
                for k in range(grid_dims[2]):
                    local_falls = get_local_falls(pitfalls, grid, grid[i][j][k])
                    my_global_ind[str(i)][str(j)][str(k)] = get_global_ind(local_falls, grid_dims)

        # !!!FOR NOW - assume MAT is of type DOUBLE
        # for i in range(grid_dims[0]):
        #     for j in range(grid_dims[1]):
        i = 0
        for ikey in ikeys:
            j = 0
            for jkey in jkeys:
                j = 0
                for kkey in kkeys:
                    k = 0
                    if temp_mat[ikey][jkey][kkey].any() != 0.0:
                        ii = my_global_ind[str(i)][str(j)][str(k)][str(0)]
                        jj = my_global_ind[str(i)][str(j)][str(k)][str(1)]
                        kk = my_global_ind[str(i)][str(j)][str(k)][str(2)]
                        if DEBUG:
                            print('mat index: ii,jj,kk = %d,%d,%d'%(len(ii),len(jj).len(kk)))
                            print('temp_mat keys: ikey,jkeykkey = %s,%s'%(ikey,jkey,kkey))
                            print(ii)
                            print(jj)
                            print(kk)
                            print(temp_mat[ikey][jkey][kkey])
                        # Add new axis for broadcasting
                        new_mat = temp_mat[ikey][jkey][kkey]
                        if len(ii)==1:
                            new_mat = new_mat[np.newaxis,:,:]
                        elif len(jj)==1:
                            new_mat = new_mat[:,np.newaxis,:]
                        elif len(kk)==1:
                            new_mat = new_mat[:,:,np.newaxis]

                        mat[ii[0]:ii[-1]+1,jj[0]:jj[-1]+1,kk[0]:kk[-1]+1] = new_mat
                    k +=1
                j +=1
            i +=1

    elif dim==4:
        print('RECONSTRUCT: Not implemented for 4-D supported');
    else:
        print('RECONSTRUCT: Only objects up to 4-D are supported');

    if DEBUG:
        print('--> Exiting reconstruct')
    return mat

