import numpy as np

from size import *
from get_local_falls import *
from get_global_ind import *
from find import *


def get_local_proc(pitfalls, grid, ind):
    """
    GET_LOCAL_PROC Returns the rank of the processor that contains index IND.
    
    GET_LOCAL_IND(PITFALLS, GRID, IND) Given the pitfalls structure, the
    grid and index pair, computes the rank of the processor where the index
    pair is local. IND is an array of two elements, GRID is the processor grid.
    
    Author: Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    DEBUG = 1
    if DEBUG:
        print('--> Entering get_local_proc')
        
    # get dimensions of the grid
    g_dims = size(grid)
    
    # global_ind as a dictionary variable
    global_ind = dict()
    
    #  2D processor grid
    if (len(g_dims) == 2):
        # get global indices for each processor in the grid
        for i in range(g_dims[0]):
            if i not in global_ind:
                global_ind[i] = dict()
            for j in range(g_dims[1]):
                local_falls = get_local_falls(pitfalls, grid, grid[i,j])
                # get_global_ind() returns a dictionary with numerical string keys
                global_ind[i][j] = get_global_ind(local_falls)
    
        # search each processor's global indices for the requested indices
        for i in range(g_dims[0]):
            for j in range(g_dims[1]):
                if (  not np.array(find(global_ind[i][j][0]==ind[0])).size==0 \
                      and not np.array(find(global_ind[i][j][1]==ind[2])).size==0):
                    r = grid[i,j]

        #  3D processor grid
    elif (len(g_dims) == 3):
        # get global indices for each processor in the grid
        for i in range(g_dims[0]):
            for j in range(g_dims[1]):
                for k in range(g_dims[2]):
                    local_falls = get_local_falls(pitfalls, grid, grid[i,j,k])
                    global_ind[i,j,k] = get_global_ind(local_falls)

        # search each processor's global indices for the requested indices
        for i in range(g_dims[0]):
            for j in range(g_dims[1]):
                for k in range(g_dims[2]):
                    if (  not np.array(find(global_ind[i,j,k][0]==ind[0])).size==0 \
                          and not np.array(find(global_ind[i,j,k][1]==ind[2])).size==0 \
                          and not np.array(find(global_ind[i,j,k][2]==ind[2])).size==0):
                        r = grid[i,j,k]
 
        #  4D processor grid
    elif (len(g_dims) == 4):
        # get global indices for each processor in the grid
        for i in range(g_dims[0]):
            for j in range(g_dims[1]):
                for k in range(g_dims[2]):
                    for l in range(g_dims[3]):
                        local_falls = get_local_falls(pitfalls, grid, grid[i,j,k,l])
                        global_ind[i,j,k,l] = get_global_ind(local_falls)

        # search each processor's global indices for the requested indices
        for i in range(g_dims[0]):
            for j in range(g_dims[1]):
                for k in range(g_dims[2]):
                    for l in range(g_dims[3]):
                        if (  not np.array(find(global_ind[i,j,k,l][0]==ind[0])).size==0 \
                              and not np.array(find(global_ind[i,j,k,l][1]==ind[2])).size==0 \
                              and not np.array(find(global_ind[i,j,k,l][2]==ind[2])).size==0 \
                              and not np.array(find(global_ind[i,j,k,l][3]==ind[3])).size==0):
                            r = grid[i,j,k,l]
    else:
        print('GET_LOCAL_PROC: does not support %d dimensions.'%(len(g_dims)))
        exit()

    if DEBUG:
        print('<-- Exiting get_local_proc')

    return r

