from multipledispatch import dispatch
import os
from glob import glob

import checkOS as OS
from MPI_Abort import *

from exec_shell_cmd import *
from set_remote_cc import *

@dispatch()
def grid_Abort():
    """Wrapper for MPI_Abort  -  Aborts any currently running MatlabMPI sessions."""
    MPI_Abort()

@dispatch(dict)
def grid_Abort(grid_config):
    """MPI_Abort  -  Aborts any currently running MatlabMPI sessions.

    Usage:
    ------
    MPI_Abort()

    Will abort any currently running PythonMPI sessions
    by looking for leftover PythonMPI jobs and killing them.
    Cannot be used after pyMPI_Delete_all. 
    
    """

    # Set some strings for special characters.
    # Get single quote character. 
    q = '\''
    qq = '"'
    
    # Get host name.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')

    # Get list of pid files.
    pid_files = glob('PythonMPI/pid.*.*')
    n_files = len(pid_files)

    # Get username (assuming local and remote username are the same)
    username = os.getlogin()
        
    # Check if there are any files
    if (n_files < 1):
        print('No pid files found')
    else:
        # Loop over each file.
        for i_file in range(n_files):
            # Python index starts from 0
            # Get file name.
            file_name = pid_files[i_file]
            # Check if there is a pid appended.
            tstr = file_name.split('.')
            if len(tstr) >=3:
                # Parse file name.
                machine = '.'.join(tstr[1:-1])
                pid = tstr[-1]

            #Check if the target machine is the host
            if grid_config['scheduler'] == 'slurm':
                unix_command = 'scancel '+pid
            else:
                print('MPI_Abort (grid version) does not support the scheduler %s'%(grid_config['scheduler']))
                exit()
                
            # Print the command and execute it
            print('... '+unix_command)
            ecmd = ExecShellCmd(set_remote_cc())
            ecmd.run(unix_command)


