import numpy as np

from MPI_Bcast import *

# pPython class
import pPython as GPC

def BcastMsg(source, tag, *argv):
    """Broadcast message from current process to all other processes.
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering BcastMsg')

    comm = GPC.comm
    Pid = GPC.my_rank

    # BcastMsg add an additional dictionary layer
    # So unpack it before returning the message.

    msg = dict()
    if Pid == source:
        # Send after packing the message into a dictionary
        ii = 0
        if DEBUG:
            print('Length of argv: %d'%(len(argv)))
        for arg in argv:
            if DEBUG:
                print(arg)
            msg[ii] = arg
            ii = ii + 1
   
    [out] = MPI_Bcast(source,tag,comm,msg)

    if DEBUG:
        print('source: %d, tag: %d'%(source,tag))
        print('<-- Exiting BcastMsg')
        
    return list(out.values())

