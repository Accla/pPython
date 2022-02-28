def pyMPI_Comm_dir(old_comm,dir):
    """MatMPI_Comm_dir  -  function for changing communication directory.

    Usage:
    ------
    new_comm = MatMPI_Comm_dir(old_comm,dir)

    old_comm:   an MPI Communicator (dtype: dictionary)
    new_comm:   an MPI Communicator (dtype: dictionary)

    """

    new_comm = old_comm;
    n = new_comm['machine_db']['n_machine']

    for ii in range(n):
        iistr = str(ii)
        new_comm['machine_db']['dir'][iistr] = dir

    return new_comm
