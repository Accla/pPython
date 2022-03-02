import numpy as np

def partition_1d(n,m):
    """Calculate data distribution in 1 dimensional space with MPI processes.
    It distributes n elements over m processes uniformly if n is divisible by m.
    If not, the remainder is distributed one element per each MPI process, starting
    the lowest process, MPI rank 0.
    
    Usage: 
    ------
    
    d_index,d_sizes = partition_1d(n,m)
    
    n: number of elements to be distributed
    m: number of MPI processes
    
    d_index: the beginning and ending indices of a partition assigned to each
             MPI processes
    d_sizes: the number of elements assigned to each MPI process
    
    """
    
    # Arrays to handle non-uniform data distribution
    d_sizes = np.zeros(m)
    
    # A dictionary to store the beginning and ending indices of each chunk
    # d_index['Pid']['beg'] and d_index['Pid']['end']
    d_index = dict()

    d_size = int(n/m)
    remainder = n%m

    # Calculate the number of elements per each MPI process
    if remainder:
        # if the size is NOT divisible by m
        icnt = 0
        for iam in range(m):
            d_index[str(iam)] = dict()
            if icnt < remainder:
                d_index[str(iam)]['beg'] = (d_size)*iam + icnt
                d_index[str(iam)]['end'] = d_index[str(iam)]['beg'] + d_size
                icnt = icnt + 1
            else:
                d_index[str(iam)]['beg'] = (d_size)*iam + icnt
                d_index[str(iam)]['end'] = d_index[str(iam)]['beg'] + d_size - 1
    else:
        # if the size is divisible by m
        for iam in range(m):
            d_index[str(iam)] = dict()
            d_index[str(iam)]['beg'] = (d_size)*iam
            d_index[str(iam)]['end'] = d_index[str(iam)]['beg'] + d_size - 1
        
    # Store the chunk size for each MPI process    
    for iam in range(m):
        # Calculate the chunk size of each MPI process
        d_sizes[iam] = d_index[str(iam)]['end'] - d_index[str(iam)]['beg'] + 1

    return d_index,d_sizes

