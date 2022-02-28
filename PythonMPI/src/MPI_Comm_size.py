def MPI_Comm_size(comm):
    """MPI_Comm_size  -  returns the number of processors in the communicator.

    Usage:
    ------
    size = MPI_Comm_rank(comm)
    
    comm:   MPI communicator  (dtype: dictionary)
    size:   number of MPI processes (dtype: int)
    
    """

    return comm['size']

