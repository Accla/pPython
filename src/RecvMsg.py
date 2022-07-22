from MPI_Recv import *

# pPython class
import pPython as GPC

def RecvMsg(source, tag):
    """Receive message from source onto current Matlab instance.
    """

    comm = GPC.comm
    
    # SendMsg add an additional dictionary layer
    # So unpack it before returning the message.
    [buf] =  MPI_Recv(source, tag, comm)

    return list(buf.values())

