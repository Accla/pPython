def MPI_Comm_rank(comm):
    """MPI_Comm_rank  -  returns the rank of the current processor.

    Usage:
    ------
    rank = MPI_Comm_rank(comm)
    
    comm:   MPI communicator  (dtype: dictionary)
    rank:   MPI rank (dtype: int)
    
    """
    return comm['rank']
