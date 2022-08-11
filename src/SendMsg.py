import numpy as np

from MPI_Send import *
from MPI_Mcast import *

# pPython class
import pPython as GPC

def SendMsg(dest, tag, *argv):
    """Send message from current process to dest.
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering SendMsg')

    comm = GPC.comm
    Pid = GPC.Pid
    
    # Send after packing the message into a dictionary
    msg = dict()
    ii = 0
    if DEBUG:
        print('Length of argv: %d'%(len(argv)))
    for arg in argv:
        if DEBUG:
            print(arg)
        msg[ii] = arg
        ii = ii + 1

    if isinstance(dest,(int,np.int64)):
        MPI_Send(dest,tag,comm,msg)
    elif (len(dest) > 1):
        MPI_Mcast(Pid,dest,tag,comm,msg)

    if DEBUG:
        print('<-- Exiting SendMsg')
