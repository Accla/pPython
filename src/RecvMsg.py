from MPI_Recv import *

# GridPython class
import GridPython as GPC

def RecvMsg(source, tag):
    """Receive message from source onto current Matlab instance.
    """

    comm = GPC.comm
    
    return MPI_Recv(source, tag, comm)

