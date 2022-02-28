from multipledispatch import dispatch
import os
from glob import glob

from pyMPI_Comm_settings import *
import checkOS as OS

@dispatch()
def MPI_Abort():
    """MPI_Abort  -  Aborts any currently running MatlabMPI sessions.

    Usage:
    ------
    MPI_Abort()

    Will abort any currently running PythonMPI sessions
    by looking for leftover PythonMPI jobs and killing them.
    Cannot be used after pyMPI_Delete_all. 
    
    """

    # global isunix, ismac, islinux, ispc
    
    # Get host name.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')

    # Get possibly user defined settings.
    machine_db_settings = pyMPI_Comm_settings()
    remote_launch = machine_db_settings['remote_launch']
    remote_flags = machine_db_settings['remote_flags']

    # Get list of pid files.
    pid_files = glob('PythonMPI/pid.*.*')
    n_files = len(pid_files)

    # Set some strings for special characters.
    # Get single quote character. 
    q = '\''
    qq = '"'

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

            # Check if the target machine is a PC
            if pid == 'pc':
                # Check if the target machine is the host
                if machine == host:
                    # Don't do anything, otherwise MPI_Abort will kill the instance of Python that launched
                    # the MPI_Abort command
                    unix_command = ''
                else:
                    # The target machine is a remote PC.
                    if OS.isunix:
                        # The host machine is a Unix machine
                        unix_command = remote_launch+machine+remote_flags+' '+q+'taskkill /f /FI "USERNAME eq '+username+'" /im python.exe'+q
                    else:
                        unix_command = remote_launch+machine+remote_flags+' '+qq+'taskkill /f /FI \"USERNAME eq '+username+'\" /im python.exe'+qq

            else:  # pid != 'pc' [target machine is a Unix machines]
                #Check if the target machine is the host
                if machine == host:
                    unix_command = 'kill -9 '+pid
                else:
                    if OS.isunix:
                        # The host machine is a  Unix machine
                        unix_command = remote_launch+machine+remote_flags+' '+q+'kill -9 '+pid+q
                    else:
                        # the host machine is a PC machine
                        unix_command = remote_launch+machine+remote_flags+' '+qq+'kill -9 '+pid+qq
            # Print the command and execute it
            print(unix_command)
            os.system(unix_command)

