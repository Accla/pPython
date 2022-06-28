import numpy as np

from MPI_Bcast import *

# pPython class
import pPython as GPC

def BcastMsg(source, tag, *argv):
    """Broadcast message from current process to all other processes.
    """

    DEBUG = 1
    if DEBUG:
        print('--> Entering BcastMsg')

    comm = GPC.comm
    Pid = GPC.my_rank
    
    # preserve the number of message counts
    str_argv = ''
    for ii in range(len(argv)):
        str_argv += 'argv['+str(ii)+'],'
    # remove the last comma
    str_argv = str_argv[0:-1]
        
    cmd = 'MPI_Bcast(source,tag,comm,'+str_argv+')'

    if DEBUG:
        print('source: %d, tag: %d'%(source,tag))
        print('Broadcasting command: %s'%(cmd))
        print('<-- Exiting BcastMsg')
        
    return eval(cmd)

