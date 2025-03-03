import re
import os

import checkOS as OS
from pyMPI_Commands import *
from pyMPI_Sleep import *

from exec_shell_cmd import *
from slurm_submit_job import *
from slurm_write_job_script import *

def launch_non_triples(py_file, comm, grid_config):
    """
    Launch pPython job on the grid without using the triples mode optimiztion.
    Each individual pPython parallel process becomes an individual array task with the scheduler.

    This is good for small scale job
    
    comm:  MPI communicator which provides information for creating all the required script for job submisison

    Note: refactored from MPI_RunG() of gridMatlab

    Author: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering launch_non_triples')

    tmp = py_file.split('.')
    py_file_basename = tmp[0] # Remove .py

    # Set some strings for special characters.
    nl = '\n'
    qq = '"'

    interactive = grid_config['interactive']
    
    pwd_pc,pwd_linux,pwd_mac,pwd_grid = pyMPI_Dir_map(pyMCW.MPI_COMM_WORLD['machine_db'],os.getcwd())

    
    # Initialize command launch on all the different machines.
    unix_launch = ''

    # Get number of machines.
    n_m = comm['machine_db']['n_machine']

    # Loop backwards over each machine target machine
    # so that we hit the host machine last (if it is a target).
    for i_m in range(n_m,0,-1):
        # convert into string
        imstr = str(i_m)
        imstrm1 = str(i_m-1)
        
        # Get number of processes to launch on this target machine.
        # Note: python indexing starts from zero, 0, to n_m-1
        n_proc_i_m = comm['machine_db']['n_proc'][i_m-1]
            
        if DEBUG:
            print('grid_run: i_m=%d, n_proc_i_m=%d'%(i_m,n_proc_i_m))

        if (n_proc_i_m >= 1):
            # Get machine name, remote lauch command & flags, and type.
            machine = comm['machine_db']['machine'][i_m-1]
            remote_launch = comm['machine_db']['remote_launch'][i_m-1]
            remote_flags = comm['machine_db']['remote_flags'][i_m-1]
            type = comm['machine_db']['type'][i_m-1]

            # Set file extension of launch script to be run on
            # this target.
            if type == 'pc':
                file_ext = '.bat'
            else:
                file_ext = '.sh';

            # Get starting and stopping rank for this machine. [To be check if minus 1 is needed?]
            i_rank_start = comm['machine_db']['id_start'][i_m-1]
            i_rank_stop = comm['machine_db']['id_stop'][i_m-1]
            # print('grid_run: i_rank_start=%d, i_rank_stop=%d'%(i_rank_start,i_rank_stop))

            # Initialize command that will be run on each target node.
            python_module_path = comm['machine_db']['python_module_path']
            python_module_name = comm['machine_db']['python_module_name']
            unix_commands = ''
            unix_commands_prefix = '#!/bin/bash'+nl+'source /etc/profile'+nl
            #
            # Add a check if this is on a LLSC system
            unix_commands_prefix = unix_commands_prefix+'if [ -e /etc/llgrid.id ]; then'+nl
            unix_commands_prefix = unix_commands_prefix+'    export MODULEPATH=${MODULEPATH}:'+python_module_path+nl
            unix_commands_prefix = unix_commands_prefix+'    module load '+python_module_name+nl
            unix_commands_prefix = unix_commands_prefix+'fi'+nl
            PYTHONPATH= os.getenv('PYTHONPATH',default='')
            if len(PYTHONPATH):
                unix_commands_prefix = unix_commands_prefix+'export PYTHONPATH='+PYTHONPATH+nl
                unix_commands_prefix = unix_commands_prefix+'echo "`hostname`: PYTHONPATH=$PYTHONPATH"'+nl+nl

            # Loop backwards over number of processes.
            for i_rank in range(i_rank_stop,i_rank_start-1,-1):
                if DEBUG:
                    print('--> launch_non_triples: i_rank = %d'%(i_rank))
                # Note: python index start zero to N-1.
                # Check if i_rank value needs to be adjusted

                # Build commands that lauch multiple matlab on target nodes.
                defscommands, unix_cmd_i_rank = pyMPI_Commands(py_file_basename,i_rank,comm,grid_config=grid_config)
                unix_commands = unix_commands+unix_cmd_i_rank

            # Create a file name to hold script that will be run on target.
            # Make sure to use the correct directory separator for Unix and DOS
            # unix_cmd_file used when host machine is running Unix
            # dos_cmd_file used when host machine is running Windows/DOS

            if interactive:
                # For ineractive, one less scripts are generaed
                imstr = imstrm1
                if i_m == 1:
                    # skip the last one
                    continue

            if type == 'pc':
                unix_cmd_file = 'PythonMPI/Dos_Commands.'+imstr+file_ext
                dos_cmd_file = 'PythonMPI\\Dos_Commands.'+imstr+file_ext
            else:
                # Add prefix for Unix systems
                unix_commands = unix_commands_prefix+unix_commands
                unix_cmd_file = 'PythonMPI/Unix_Commands.'+imstr+file_ext
                dos_cmd_file = 'PythonMPI/Unix_Commands.'+imstr+file_ext

            # Put commands in a file.
            fid = open(unix_cmd_file,'w')
            
            # Fix unix_commands for LLGrid run
            # Remove & at the end of each line
            # unix_commands = re.sub("out &","out", unix_commands)
            # Comment out the touch command
            unix_commands = re.sub("touch","# touch", unix_commands)
            # Add the "wait" at the end so that all the processes are done 
            # before exiting Slurm task
            unix_commands += '\nwait\n'
            fid.write(unix_commands)
            fid.close()

    # If it's an interactive job, translate the current working directory as local path for Pid=0
    if interactive:
        if os.path.exists('/etc/llgrid.id'):
            local_path = pwd_grid
        else:
            if OS.ispc:
                local_path = pwd_pc
            elif OS.islinux:
                local_path = pwd_linux
            elif OS.ismac:
                local_path = pwd_mac
        comm['machine_db']['dir']['0'] = local_path
        
    # Display launch command.
    # print(unix_launch)
  
    # Write the scheduler job script file
    # This is done to fix Matlab's problem with very long commands sent to unix().
    # It may not present with python, though
    sched_job_file = 'PythonMPI/Unix_Commands.sh'
    if grid_config['scheduler'] == 'slurm':
        slurm_write_job_script(grid_config,sched_job_file,py_file,pwd_grid)
    else:
        raise Exception('Error: unsupported scheduler, %s'%(grid_config['scheduler']))
        
    # Execute launch script.
    # dos2unix convert command
    if OS.ispc:
        # Convert Windows EOL characters to Unix EOL characters
        # print('Execute dos2unix to convert EOL characters')
        convert_command = 'dos2unix PythonMPI/*py PythonMPI/*sh'    
        ecmd = ExecShellCmd(set_remote_cc())
        cmdstr = qq+'cd '+pwd_grid+'; '+convert_command+qq
        ecmd.run(cmdstr)
        #
        # Need a delay to make this conversion become effective on the grid environment
        pyMPI_Sleep(1.0)
        
        if DEBUG:
            output = ecmd.get_output().strip()
            print('\n'+output+'\n')
            errout = ecmd.get_stderr()
            print(errout)


    # Submit the job
    if grid_config['scheduler'] == 'slurm':
            slurm_submit_job(grid_config,sched_job_file,py_file,pwd_grid)
    else:
        raise Exception('Error: unsupported scheduler, %s'%(grid_config['scheduler']))

    # For somehow find out if this is an interactive job. then, execute the local processing:
    if interactive:
        # print(defscommands)
        print('grid_run: executing %s in the current python process.'%(py_file))
        print(' ')
        exec(defscommands)

    if DEBUG:
        print(defscommands)
        print('. . .')
        print('<-- Exiting launch_non_triples')
        
    return defscommands

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
