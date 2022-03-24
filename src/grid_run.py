from multipledispatch import dispatch
import math
import re
import os

import checkOS as OS
import pyMPI_COMM_WORLD as pyMCW
from MPI_Run import *

from convert_to_dict import *
from StopExecution import *
from pyMPI_Comm_init import *
from pyMPI_Commands import *
from pyMPI_Dir_map import *
from pyMPI_Sleep import *

from exec_shell_cmd import *
from grid_resource_policy  import *
from slurm_write_job_script import *
from slurm_submit_job import *
import grid_config as grid

@dispatch(str,int,list)
def grid_run( py_file, n_proc, machines ):
    """Wrapper for MPI_Run()."""
    return MPI_Run(py_file, n_proc, machines)

@dispatch(str,int,str)
def grid_run( py_file, n_proc, machines ):
    """MPI_Run  -  Run py_file on multiple processors on LLGrid.

    Usage:
    ------
    defscommands = MPI_Run( py_file, n_proc, machines )

    Runs n_proc copies of py_file on machines, where

    machines = 'grid'   (dtype: string)
        Run on a LLGrid system interactively.

    machines = 'grid&'   (dtype: string)
        Run on a LLGrid system in a backgrounded mode.

    py_file:  the python script name (dtype: string)
    n_proc:   total number of MPI processes (dtype: int)
    machines: 'grid' or 'grid&'
              extended to 'grid-cpu_type' or 'grid-cpu_type&'
    
    defscommands: command to run locally if machine is a local machine

    """

    DEBUG = 0

    if DEBUG:
        print('--> Entering MPI_Run (gridPython version).')
        print('MPI_Run: isunix, ismac, islinux, ispc = %d,%d,%d,%d'%(OS.isunix, OS.ismac, OS.islinux, OS.ispc))
    
    # Set some strings for special characters.
    qq = '"'
    sp = ' '
    nl = '\n'
    # Get single quote character. 
    q = '\''
    
    # Unix vs. Windows file seperator.
    dir_sep = os.sep

    # Unix vs. Windows host name.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')

    # Determine whether it is an interactive or backgrounded job
    # print('machines: %s'%(machines))
    if machines.find('&')>0:
        # Backgrounded job
        endStr = '&'
        interactive = 0
    else:
        # Interacttive job
        endStr = ''
        interactive = 1
    
    # Determine if a specific CPU type is requested
    cpu_type = ''
    if len(machines) > 5:
        # 'grid-xeon-e5[&]'
        if endStr == '&':
            cpu_type = machines[5:-1]
        else:
            cpu_type = machines[5:]
            
    # Modify the default value if cpu_type is specified
    if len(cpu_type):
        grid.grid_config['cpu_type'] = cpu_type
        # Update the queue name (partition name) accordingly
        if (cpu_type == 'xeon64c'):
            grid.grid_config['q_name'] = 'manycore'
        elif (cpu_type == 'xeon-g6'):
            grid.grid_config['q_name'] = 'gaia'

    # number of cores to be allocated from the grid
    requested,unclaimed_procs,unclaimed_nodes = grid_resource_policy(grid.grid_config, n_proc, interactive)
    n_proc = requested + interactive

    # Create a fictious machine list when 'grid[&]' is used
    machines = []
    if grid.grid_config['n_nodes'] > 0: 
        # Triples modes, local MPI processes aggregated into a single scheduler task
        grid.grid_config['ntasks'] = grid.grid_config['n_nodes']
        n_digits = int(math.log10(grid.grid_config['n_nodes'])+1)
        for i in range(grid.grid_config['n_nodes']):
            node_strid = str(i+1).zfill(n_digits)
            machines.append('grid_slurm_'+node_strid)
    else:
        # Non-triple modes
        grid.grid_config['ntasks'] = n_proc
        n_digits = int(math.log10(n_proc)+1)
        for i in range(n_proc):
            node_strid = str(i+1).zfill(n_digits)
            machines.append('grid_slurm_'+node_strid)
    
    # Overwrite the Pid=0 machine for an interactive job
    if interactive:
        machines[0] = host
        
    # Convert machines into a dictionary variable if needed
    machines = convert_to_dict(machines,host)

    # Check if the directory 'PythonMPI' exists
    checkPath = '.'+os.sep+'PythonMPI'
    if os.path.isdir(checkPath):
        print('Error: PythonMPI directory already exists: rename or remove with pyMPI_Delete_all')
        raise StopExecution
    else:
        os.makedirs(checkPath)

    # Get number of machines to launch on.
    n_machines = len(machines)

    # Create generic comm. (Initialize global pyMCW.MPI_COMM_WORLD)
    pyMCW.MPI_COMM_WORLD = pyMPI_Comm_init(n_proc,machines);

    # Set paths.
    if DEBUG:
        # print(pyMCW.MPI_COMM_WORLD['machine_db'])
        print(os.getcwd())
    pwd_pc,pwd_linux,pwd_mac,pwd_grid = pyMPI_Dir_map(pyMCW.MPI_COMM_WORLD['machine_db'],os.getcwd())

    tmp = py_file.split('.')
    py_file_basename = tmp[0] # Remove .py
    
    # Initialize command launch on all the different machines.
    unix_launch = ''

    # Get number of machines.
    n_m = pyMCW.MPI_COMM_WORLD['machine_db']['n_machine']

    # Loop backwards over each machine target machine
    # so that we hit the host machine last (if it is a target).
    for i_m in range(n_m,0,-1):
        # convert into string
        imstr = str(i_m)
        imstrm1 = str(i_m-1)
        
        # Get number of processes to launch on this target machine.
        # Note: python indexing starts from zero, 0, to n_m-1
        n_proc_i_m = pyMCW.MPI_COMM_WORLD['machine_db']['n_proc'][i_m-1]
            
        if DEBUG:
            print('MPI_Run: i_m=%d, n_proc_i_m=%d'%(i_m,n_proc_i_m))

        if (n_proc_i_m >= 1):
            # Get machine name, remote lauch command & flags, and type.
            machine = pyMCW.MPI_COMM_WORLD['machine_db']['machine'][imstrm1]
            remote_launch = pyMCW.MPI_COMM_WORLD['machine_db']['remote_launch'][imstrm1]
            remote_flags = pyMCW.MPI_COMM_WORLD['machine_db']['remote_flags'][imstrm1]
            type = pyMCW.MPI_COMM_WORLD['machine_db']['type'][imstrm1]

            # Set file extension of launch script to be run on
            # this target.
            if type == 'pc':
                file_ext = '.bat'
            else:
                file_ext = '.sh';

            # Get starting and stopping rank for this machine. [To be check if minus 1 is needed?]
            i_rank_start = pyMCW.MPI_COMM_WORLD['machine_db']['id_start'][i_m-1]
            i_rank_stop = pyMCW.MPI_COMM_WORLD['machine_db']['id_stop'][i_m-1]
            # print('MPI_Run: i_rank_start=%d, i_rank_stop=%d'%(i_rank_start,i_rank_stop))

            # Initialize command that will be run on each target node.
            python_module_path = pyMCW.MPI_COMM_WORLD['machine_db']['python_module_path']
            python_module_name = pyMCW.MPI_COMM_WORLD['machine_db']['python_module_name']
            unix_commands = ''
            unix_commands_prefix = '#!/bin/bash'+nl+'source /etc/profile'+nl
            #
            # Add a check if this is on a LLSC system
            unix_commands_prefix = unix_commands_prefix+'if [ -e /etc/llgrid.id ]; then'+nl
            unix_commands_prefix = unix_commands_prefix+'    export MODULEPATH=${MODULEPATH}:'+python_module_path+nl
            unix_commands_prefix = unix_commands_prefix+'    module load '+python_module_name+nl
            unix_commands_prefix = unix_commands_prefix+'fi'+nl

            # Loop backwards over number of processes.
            for i_rank in range(i_rank_stop,i_rank_start-1,-1):
                if DEBUG:
                    print('--> MPI_Run: i_rank = %d'%(i_rank))
                # Note: python index start zero to N-1.
                # Check if i_rank value needs to be adjusted

                # Build commands that lauch multiple matlab on target nodes.
                defscommands, unix_cmd_i_rank = pyMPI_Commands(py_file_basename,i_rank,pyMCW.MPI_COMM_WORLD)
                unix_commands = unix_commands+unix_cmd_i_rank

            # Create a file name to hold script that will be run on target.
            # Make sure to use the correct directory separator for Unix and DOS
            # unix_cmd_file used when host machine is running Unix
            # dos_cmd_file used when host machine is running Windows/DOS
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
            local_path = pwd_pc
        else:
            if OS.ispc:
                local_path = pwd_pc
            elif OS.islinux:
                local_path = pwd_linux
            elif OS.ismac:
                local_path = pwd_mac
        pyMCW.MPI_COMM_WORLD['machine_db']['dir']['0'] = local_path
        
    # Display launch command.
    # print(unix_launch)
  
    # Write the scheduler job script file
    # This is done to fix Matlab's problem with very long commands sent to unix().
    # It may not present with python, though
    sched_job_file = 'PythonMPI/Unix_Commands.sh'
    if grid.grid_config['scheduler'] == 'slurm':
        slurm_write_job_script(sched_job_file,py_file,pwd_grid)
    else:
        print('Error: unsupported scheduler, %s'%(grid.grid_config['scheduler']))
        exit()
        
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
    if grid.grid_config['scheduler'] == 'slurm':
            slurm_submit_job(grid.grid_config,sched_job_file,py_file,pwd_grid)
    else:
        print('Error: unsupported scheduler, %s'%(grid.grid_config['scheduler']))
        exit()

    # For somehow find out if this is an interactive job. then, execute the local processing:
    if interactive:
        print(defscommands)
        print('grid_run: executing %s in the current python process.'%(py_file))
        exec(defscommands)

    if DEBUG:
        print('. . .')
        print('<-- Exiting MPI_Run.')
        
    return defscommands

