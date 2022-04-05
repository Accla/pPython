import numpy as np

from MPI_Send import *
from MPI_Mcast import *

# GridPython class
import GridPython as GPC

def SendMsg(dest, tag, *argv):
    """Send message from current process to dest.
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering SendMsg')

    comm = GPC.comm
    Pid = GPC.my_rank
    
    # preserve the number of message counts
    str_argv = ''
    for ii in range(len(argv)):
        str_argv += 'argv['+str(ii)+'],'
    # remove the last comma
    str_argv = str_argv[0:-1]
        
    if DEBUG:
        print('Sending message: %s'%(str_argv))

    if isinstance(dest,(int,np.int64)):
        cmd = 'MPI_Send(dest,tag,comm,'+str_argv+')'
        exec(cmd)
    elif (len(dest) > 1):
        cmd = 'MPI_Mcast(Pid,dest,tag,comm,'+str_argv+')'
        exec(cmd)

    if DEBUG:
        print('<-- Exiting SendMsg')
