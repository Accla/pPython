from multipledispatch import dispatch
import os

import pyMPI_COMM_WORLD as pyMCW
import checkOS as OS

from convert_to_dict import *
from StopExecution import *
from pyMPI_Comm_init import *
from pyMPI_Commands import *
from pyMPI_Dir_map import *

@dispatch(str,int,list)
def MPI_Run( py_file, n_proc, machines ):
    """MPI_Run  -  Run py_file on multiple processors.

    Usage:
    ------
    defscommands = MPI_Run( py_file, n_proc, machines )

    Runs n_proc copies of py_file on machines, where

    machines = []   (dtype: dictionary, empty)
        Run on a local machine.

    machines = [ 'machine1', 'machine2'] (dtype: list)
        Run on multi nodes
        
    machines = ['machine1:dir1' 'machine2:dir2'] (dtype: list)
        Run on multi nodes and communicate using via dir1 and dir2,
        which must be visible to both machines. 

    machines = ['machine1:type:dir1' 'machine2:type:dir2'] (dtype: list)
        Run on a multi processors of different type ('unix' or 'pc').
        Default is 'unix' (can be overiden in pyMPI_Comm_settings.py)

    Full syntax is: machine['&'][':unix'|':pc'][:dir]
        & => all jobs launched on host should be run in background.

    If machine1 is the local cpu, then defscommands will contain
    the commands that need to be run locally, via exec(open("defscommands").read()).

    py_file:  the python script name (dtype: string)
    n_proc:   total number of MPI processes (dtype: int)
    machines: a list of machines (dtype: dictionary)
              if given as a lit, convert it as a dictionary.
    defscommands: command to run locally if machine is a local machine

    """

    DEBUG = 0

    if DEBUG:
        print('--> Entering MPI_Run.')
        print('MPI_Run: isunix, ismac, islinux, ispc = %d,%d,%d,%d'%(OS.isunix, OS.ismac, OS.islinux, OS.ispc))
    
    # Unix vs. Windows file seperator.
    dir_sep = os.sep

    # Unix vs. Windows host name.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')

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
    pwd_pc,pwd_linux,pwd_mac = pyMPI_Dir_map(pyMCW.MPI_COMM_WORLD['machine_db'],os.getcwd())

    # Set some strings for special characters.
    qq = '"'
    sp = ' '
    nl = '\n'
    # Get single quote character. 
    q = '\''
    ssh_response=checkPath+dir_sep+'remote.out'
    
    # Extract the actual pPython script name (do we need this?)
    script_file_head = '.pRUN_Parallel_Stub_';
    script_file_tail = '_temp';
    # The following assumes that only one such a file exists.
    # It will fail if more than one files exists.
    # Find the script file name
    for file in os.listdir("."):
        if file.startswith(script_file_head):
            last5chars = file[len(file)-5:]
            if script_file_tail == last5chars:
                my_script_file = file[len(script_file_head):(len(file)-5)]
                # print('Script name: %s'%(script_name))
                
    tmp = py_file.split('.')
    py_file_basename = tmp[0] # Remove .py
    
    # Initialize command launch on all the different machines.
    unix_launch = ''

    # Get number of machines.
    n_m = pyMCW.MPI_COMM_WORLD['machine_db']['n_machine']

    # dos2unix convert command
    if OS.ispc:
        convert_command = 'dos2unix PythonMPI/*py PythonMPI/*sh'
        convert_file = 'PythonMPI\dos2unix_conversion.bat'
    
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
                unix_cmd_file = 'PythonMPI/Dos_Commands.' +machine+'.'+str(i_rank_start)+file_ext
                dos_cmd_file = 'PythonMPI\\Dos_Commands.'+machine+'.'+str(i_rank_start)+file_ext
            else:
                # Add prefix for Unix systems
                unix_commands = unix_commands_prefix+unix_commands
                unix_cmd_file = 'PythonMPI/Unix_Commands.'+machine+'.'+str(i_rank_start)+file_ext
                dos_cmd_file = 'PythonMPI/Unix_Commands.'+machine+'.'+str(i_rank_start)+file_ext

            # Put commands in a file.
            fid = open(unix_cmd_file,'w')
            fid.write(unix_commands)
            fid.close()

            # Create host commands to launch this file.
            if machine == host:     # Target (machine) is host.
                if type == 'pc':    # Host is a pc.
                    unix_launch_i_m = 'start /b '+dos_cmd_file+nl
                else:
                    unix_launch_i_m = '/bin/bash ./'+unix_cmd_file+' &'+nl

            else:    # Target is a remote machine.
                if (OS.ispc):    # Host is a pc.
                    if type == 'pc':    # Target is a pc.
                        if DEBUG:
                            print('C1 - Remote target: host IS a pc and remote target is a pc')
                        unix_launch_i_m = 'sttart /b '+remote_launch+machine+remote_flags+qq+'cd /d '+pwd_pc+' & '+dos_cmd_file+qq+nl
                    else:
                        if DEBUG:
                            print('C2 - Remote target: host IS a pc but remote target is NOT a pc')
                        unix_launch_i_m = 'start /b '+remote_launch+machine+remote_flags+qq+'cd '+pwd_linux+'; /bin/bash ./'+unix_cmd_file+' &'+qq+nl
                        remote_machine = machine
                else:    # Host is NOT a pc.
                    if DEBUG:
                        print('Remote target: host is NOT a pc')
                    if type == 'pc':    # Target is a pc.
                        if DEBUG:
                            print('C3 - Remote target: host is NOT a pc but remote target IS a pc')
                        unix_launch_i_m = remote_launch+machine+remote_flags+qq+'cd /d '+pwd_pc+' & '+dos_cmd_file+qq+nl
                    else: 
                        if DEBUG:
                            print('C4 - Remote target: host is NOT a pc but remote target IS NOT a pc')
                        unix_launch_i_m = remote_launch+machine+remote_flags+q+'cd '+pwd_linux+'; /bin/bash ./'+unix_cmd_file+q+' > '+ssh_response+' >&2 & '+nl

            # Append to variable that will be written to a file.
            unix_launch = unix_launch+unix_launch_i_m

    # Display launch command.
    print(unix_launch)
  
    # Write launch commands to .sh or .bat text file
    # This is done to fix Matlab's problem with very long commands sent to unix().
    # It may not present with python, though
    if (OS.ispc):
        launch_file = 'PythonMPI\Dos_Commands.bat'
    else:
        launch_file = 'PythonMPI/Unix_Commands.sh'
            
    fid = open(launch_file,'w')
    fid.write(unix_launch)
    fid.close()

    # Execute launch script.
    if (OS.ispc):
        # Convert Windows EOL characters to Unix EOL characters
        fid = open(convert_file,'w')
        cmd = 'start /b '+remote_launch+remote_machine+remote_flags+qq+'cd '+pwd_linux+'; '+convert_command
        fid.write(cmd)
        fid.close()
        os.startfile(convert_file)
        os.startfile(launch_file)
    else:
        os.system('/bin/bash '+launch_file)

    # For somehow find out if this is an interactive job. then, execute the local processing:
    if DEBUG:
        print(defscommands)
        print('MPI_Run: executing %s in the current python process.'%(py_file))
    exec(defscommands)

    if DEBUG:
        print('. . .')
        print('<-- Exiting MPI_Run.')
        
    return defscommands

