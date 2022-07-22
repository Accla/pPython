from get_local_falls import *
from get_global_ind import *

def grid_global_ind(d):
    """Returns global index array for the processor grid.
    """
    
    # dimension of the distributed object
    dim = len(d.pitfalls)

    # processor grid on which the object is distributed
    grid = d.map.grid

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
        print('GLOBAL_BLOCK_RANGES: Only objects up to 4-D are supported')
        exit()
        
    return global_ind

