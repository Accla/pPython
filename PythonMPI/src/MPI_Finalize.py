import pyMPI_COMM_WORLD as pyMCW

from MPI_Comm_rank import *
from pyMPI_Host_rank import *

def MPI_Finalize():
    """MPI_Finalize - Called at the end of a MatlabMPI program.

    Usage:
    ------
    MPI_Finalize()
    
    Called at the end of an MPI program (currently empty).
    
    """
    my_rank = MPI_Comm_rank(pyMCW.MPI_COMM_WORLD)
    host = pyMPI_Host_rank(pyMCW.MPI_COMM_WORLD)
    leader = 0

    # exit python process if this is not the host
    if my_rank != host:
        exit()

