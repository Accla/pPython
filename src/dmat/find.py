import numpy as np

from MPI_Send import *
from MPI_Recv import *

import pPython as GPC
from Dmat import *
from inmap import *
from size import *

def find(x):
    """
    FIND Find indices of nonzero elements.
    
    [I,J] = FIND(X) returns the row and column indices of nonzero elements
    of the distributed matrix X.
    NOTE: Currently supports only [i,j] = find(x) calling convention.
    Only works on 2D arrays.
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering find')

    if not isinstance(x,Dmat):
        if DEBUG:
            print('... find for a non-distributed array')
        local_ij = np.argwhere(x)
        # Note: local_ij[:,0] -> local_i, local_ij[:,1] -> local_j
        if len(x.shape) == 1:
            if len(local_ij)>0:
                i = local_ij[:,0]
            else:
                i = []
            if DEBUG:
                print('<-- Exiting find')
            return [i]
        elif len(x.shape) == 2:
            if len(local_ij)>0:
                i = local_ij[:,0]
                j = local_ij[:,1]
            else:
                i = []
                j = []
            if DEBUG:
                print('<-- Exiting find')
            return [i,j]
        else:
            print('Not implemented yet for DIM > 2.')
            exit()
    else:
        if DEBUG:
            print('... find for a distributed array')
        # increment tag
        GPC.tag_num = GPC.tag_num+1
        GPC.tag = 'tag-'+str(GPC.tag_num)
        
        if inmap(x.map, GPC.my_rank):
            local_ij = np.argwhere(x.local)
            # Note: local_ij[:,0] -> local_i, local_ij[:,1] -> local_j
            if isinstance(x.global_ind[0], str):
                if x.global_ind[0] == ':':
                    # Send range() instead of list to save memory
                    x.global_ind[0] = range(x.shape[1]+1)
            if isinstance(x.global_ind[1], str):
                if x.global_ind[1] == ':':
                    x.global_ind[1] = range(x.shape[2]+1)
        
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
        
            grid_size = size(x.map.grid)
            #grid_size(1) - number of grid rows, grid_size(2) - number of grid cols
            #send local finds to everyone
            for d1 in range(grid_size[0]):
                for d2 in range(grid_size[1]):
                    if (GPC.my_rank != x.map.grid[d1,d2]):
                        MPI_Send(x.map.grid[d1,d2], GPC.tag, GPC.comm, data)

            #receive finds from everyone
            for d1 in range(grid_size[0]):
                if d1 not in temp:
                    temp[d1] = dict()
                for d2 in range(grid_size[1]):
                    if DEBUG:
                        print('x.map.grid[d1, d2]')
                        print(x.map.grid[d1,d2])
                    if (GPC.my_rank != x.map.grid[d1,d2]):
                        [temp[d1][d2]] = MPI_Recv(x.map.grid[d1,d2], GPC.tag, GPC.comm)
                    else:
                        temp[d1][d2] = data
            i = []
            j = []
            for d2 in range(grid_size[1]): #grid cols
                for d1 in range(grid_size[0]): #grid rows
                    if (GPC.my_rank != x.map.grid[d1,d2]):
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

