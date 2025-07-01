from multipledispatch import dispatch
import os
import getpass
from glob import glob

import checkOS as OS
from MPI_Abort import *

from exec_shell_cmd import *
from set_remote_cc import *

# Note: refactored MPI_Abort in gridMatlab
#
# Author: Dr. Chansup Byun

@dispatch()
def grid_abort():
    """
    Wrapper for MPI_Abort  -  Aborts any currently running PythonMPI sessions.
    """
    MPI_Abort()

@dispatch(dict)
def grid_abort(grid_config):
    """MPI_Abort  -  Aborts any currently running PythonMPI sessions.

    Usage:
    ------
    MPI_Abort()

    Will abort any currently running PythonMPI sessions
    by looking for leftover PythonMPI jobs and killing them.
    Cannot be used after pyMPI_Delete_all. 
    
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering grid_abort(grid_config): MPI_Abort for grid job')
    # Check if PythonMPI exist and return if it does not
    if not os.path.exists('PythonMPI'):
        return

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
    try:
        username = os.getlogin()
    except OSError as e:
        # Fallback to getpass.getuser() for a more robust solution
        username = getpass.getuser()

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
                raise Exception('MPI_Abort (grid version) does not support the scheduler %s'%(grid_config['scheduler']))
                
            # Print the command and execute it
            print('... '+unix_command)
            ecmd = ExecShellCmd(set_remote_cc())
            ecmd.run(unix_command)

    if DEBUG:
        print('<-- Exiting grid_abort(grid_config)')

########################################################
# gridMatlab
# Dr. Albert Reuther
# reuther@ll.mit.edu
# MIT Lincoln Laboratory
########################################################
# Copyright 2003-9 Massachusetts Institute of Technology
#
# Permission is herby granted, without payment, to copy, modify, display
# and distribute this software and its documentation, if any, for any
# purpose, provided that the above copyright notices and the following
# three paragraphs appear in all copies of this software.  Use of this
# software constitutes acceptance of these terms and conditions.
#
# IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
# THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
#
# THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.
