import os

from MPI_Comm_size import *

import pyMPI_COMM_WORLD as pyMCW
import checkOS as OS
from pyMPI_Host_rank import *
from pyMPI_Dir_map import *

def pyMPI_Commands(py_file,rank,MPI_COMM_WORLD):
    """pyMPI_Commands  -  Commands to launch a python script remotely.

    Usage:
    ------
    defscommands, unix_command = pyMPI_Commands(py_file,rank,pyMCW.MPI_COMM_WORLD)
    
    py_file: a python script name (dtype: string)
    rank: a MPI process rank (dtype: int)
    pyMCW.MPI_COMM_WORLD: MPI communicator (dtype: dictionary)
    defscommands: Python commands to be executed by remotely launched Python processes
                  to start coressponding Python MPI processes under the hood.
    unix_command: Command to start PythonMPI script.

    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering pyMPI_Commands:')
        print('rank = %d'%(rank))

    Np = MPI_Comm_size(MPI_COMM_WORLD)

    # Unix vs. Windows file seperator.
    dir_sep = os.sep;

    # Get host.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')
        
    # Set some strings for special characters.
    qq = '"'
    sp = ' '
    nl = '\n'
    # Get single quote character. 
    q = '\''

    # Set OMP_NUM_THREADS to control the number of threads.
    # The default is 1.
    OMP_NUM_THREADS = os.environ.get('OMP_NUM_THREADS', '1')

    # Get info on the target machine.
    machine_id = pyMCW.MPI_COMM_WORLD['machine_id'][rank]
    machine = pyMCW.MPI_COMM_WORLD['machine_db']['machine'][machine_id]
    remote_launch = pyMCW.MPI_COMM_WORLD['machine_db']['remote_launch'][machine_id]
    remote_flags = pyMCW.MPI_COMM_WORLD['machine_db']['remote_flags'][machine_id]
    python_base  = pyMCW.MPI_COMM_WORLD['machine_db']['python_command'][machine_id]
    type = pyMCW.MPI_COMM_WORLD['machine_db']['type'][machine_id]

    # Create filename each Python job will run at startup.
    defsbase = 'PythonMPI/PythonMPIdefs' + str(rank)
    defsfile = defsbase + '.py'
    comm_pkl_file = 'PythonMPI/MPI_COMM_WORLD.pkl'

    # Replace my_script_file with py_file basename (withoutt .py)
    outfile = 'PythonMPI/' + py_file + '.' + str(rank) +'.out'

    # Create Python MPI setup commands.
    # Find the location for PythonMPI modules
    python_mpi_path = os.getenv("PYTHONMPI_PATH")
    if not python_mpi_path:
        print('pyMPI_Commands: PYTHONMPI_PATH is not set to find PythonMPI modules')
        raise StopExecution
        
    commands = dict()
    # split python_mpi_path individually
    if OS.ispc:
        sep_str = ';'
    else:
        sep_str = ':'
    tmp = python_mpi_path.split(sep_str)
    if DEBUG:
        print(tmp)
    add_path_str = ''
    for path in tmp:
        # path needs to be translated in to the LLSC path if the machine is not the host
        dir_pc, dir_linux, dir_mac, dir_grid = pyMPI_Dir_map(pyMCW.MPI_COMM_WORLD['machine_db'],path)
        if machine == host:
            if os.path.exists('/etc/llgrid.id'):
                path = dir_grid
            else:
                if OS.ispc:
                    path = dir_pc
                elif OS.ismac:
                    path = dir_mac
                else:
                    path = dir_linux
        else:
            # Use dir_grid (assuming all remote hosts are on the grid)
            path = dir_grid
        if DEBUG:
            print('Translated path: %s'%(path))
        if OS.ispc:
           # Add prefix r to fix the error, unicodeescape codec annnot decode bytes in position 2-3: trauncate \UXXXXX escape
           add_path_str = add_path_str + 'sys.path.append(r'+q+path+q+')'+nl
        else:
           add_path_str = add_path_str + 'sys.path.append('+q+path+q+')'+nl

    commands[0] = 'import os'+nl
    commands[0] = commands[0]+'import sys'+nl+add_path_str
    commands[0] = commands[0]+'os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"' + nl
    commands[0] = commands[0]+'os.environ["OMP_NUM_THREADS"]="' + OMP_NUM_THREADS + '"' + nl
    # commands[0] = commands[0]+'from PythonMPI import *' + nl
    commands[0] = commands[0]+'import pyMPI_COMM_WORLD as pyMCW' + nl
    commands[0] = commands[0]+'from dict_with_pickle import load_dict_from_pickle' + nl
    commands[1] = 'from pPython_init import *' + nl
    commands[2] = 'pyMCW.MPI_COMM_WORLD = load_dict_from_pickle('+q+comm_pkl_file+q+')' + nl
    commands[3] = 'pyMCW.MPI_COMM_WORLD['+q+'rank'+q+'] = ' + str(rank) + nl
    # Additional to define global variables: 
    commands[3] = commands[3]+'pPython_init()' + nl
    # commands[3] = commands[3]+'id=CheckOS()' + nl
    # commands[4] = ['delete(' q defsfile q ');' nl];
    commands[5] = 'exec(open("'+py_file+'.py").read())'+nl

    defscommands = '';

    # Print name of the target machine we are launching on.
    # CB: Reduce the output when Np > 16
    if (Np>=16):
        if (rank > (Np-3)) or (rank < 2):
            print('Launching MPI rank: %d on %s.' %(rank,machine))
        elif (rank==(Np-3)):
            print('Continuing to launch MPI processes ......')
    else:
        print('Launching MPI rank: %d on %s.' %(rank,machine))

    # Create base python command.
    python_command = python_base+' '+defsfile+' &> '+outfile

    # Determine how to run script and where to send output.
    if machine == host: # Target is host.
        # Check if running with host& set.
        if ((rank == 0) and (pyMPI_Host_rank(pyMCW.MPI_COMM_WORLD) == 0)):
            # Run defsfile scipt interactively.
            defscommands = commands[0]+commands[1]+commands[2]+commands[3]+commands[5]
            unix_command = nl;
            defscommands = defscommands
            if DEBUG:
                print('Rank 0: defscommands = %s'%(defscommands))
        else:
            # Write commands to a .py text file.
            fid = open(defsfile,'w')
            n_command = len(commands)
            for k,v in commands.items():
                #print('k,v: %d, %s'%(k,v))
                fid.write(v)
            fid.close()

            # Create command to run defsfile locally and pipe output to another file.
            if type == 'pc':
                # Target is a pc.
                # PC equivalent to touch is 'copy nul filename.txt'
                python_command = python_base+' '+defsfile+' > '+outfile
                unix_command = 'start /b '+python_command+nl+'copy nul PythonMPI\pid.'+machine+'.pc'+nl 
            else:
                unix_command = python_command+' &'+nl+'touch PythonMPI/pid.'+machine+'.$!'+nl
    else:
        # Target is a remote machine.
        # Write commands to a .m text file.
        fid = open(defsfile,'w');
        n_command = len(commands)
        for k,v in commands.items():
            #print('k,v: %d, %s'%(k,v))
            fid.write(v)
        fid.close()

        # Create command to run defsfile locally and pipe output to another file.
        if type == 'pc':
            # Remote machine is a pc.
            # PC equivalent to touch is 'copy nul filename.tx&t'
            python_command = python_base+' '+defsfile+' > '+outfile
            unix_command = 'start /b '+python_command+nl+'copy nul PythonMPI\pid.'+machine+'.pc'+nl 
        else:
            unix_command = python_command+' &'+nl+'touch PythonMPI/pid.'+machine+'.$!'+nl

    if DEBUG:
        print('unix_command: %s'%(unix_command))
        print('<-- Exiting pyMPI_Commands:')
    return defscommands, unix_command

