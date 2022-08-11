from MPI_Probe import *

# pPython class
import pPython as GPC

def ProbeMsg(source, tag):
    """
    ProbeMsg abstracts away further details with MPI_Probe
    Returns message_rank, numeric_tag, string_tag
    """
    
    comm = GPC.comm
    nargout = 3
    return MPI_Probe(source, tag, comm, nargout)

