from MPI_Recv import *

# pPython class
import pPython as GPC

def RecvMsg(source, tag):
    """Receive message from source onto current Matlab instance.
    """

    comm = GPC.comm
    
    return MPI_Recv(source, tag, comm)

