def pyMPI_Host_name(comm):
    """pyMPI_Host_name  -  returns the machine name of the host processor (if present).
    
    Usage:
    ------
    hostname = pyMPI_Host_name(comm)
    
    comm:   an MPI Communicator (dtype: dictionary)
    hostname:   a machine name(dtype: string)

    """

    return comm['host_name']

