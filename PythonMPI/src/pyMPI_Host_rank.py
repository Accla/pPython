def pyMPI_Host_rank(comm):
    """pyMPI_Host_rank  -  returns the rank of the host processor (if present).
    
    Usage:
    ------
    rank = pyMPI_Host_rank(comm)
    
    comm:   an MPI Communicator (dtype: dictionary)
    rank:   an MPI process rank (dtype: dictionary)

    """

    return comm['host_rank']

