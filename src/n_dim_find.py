import numpy as np

def n_dim_find(grid,rank):
    """Find the index posision of the process grid array for the given rank.
    
    Usage: 
    ------
    
    ind = n_dim_find(grid,rank)
    
    grid: process grid (its values are process ranks)
    rank: process rank
    
    python version: Dr. Chansup Byun
    """
    
    dim = len(grid.shape)
    ind = np.zeros(dim,dtype=int)
    
    result = np.where(grid == rank)
    # result is a tuple with indices of grid where rank is located
    ifound = any(map(lambda x: any(x>=0), result))
    if ifound:
        # Convert np array into a list for easy of use
        for i in range(len(result)):
            ind[i] = result[i][0]
    else:
        print('ERROR(n_dim_find): Rank, %d, not found in process grid.'%(rank))
            
    # fill up in case ind dimension does not match with dim
    if ifound and (len(ind)<dim):
        for d in range((len(ind)+1),dim+1):
            ind[d] = 0
            
    return ind    

