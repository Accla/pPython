import os

import checkOS as OS
from pyMPI_Dir_map import *
from pyMPI_Host_name import *

def gen_commands(py_file,python_mpi_path,rank,machine,comm,EPPAC=None):
    """
    Generate Python commands to be executed before calling pPUN_Parallel_wrapper()
    """
    DEBUG = 1
    if DEBUG:
        print('--> Entering gen_commands')
    
    # Set variables for special string.
    nl = '\n'
    # Get single quote character. 
    q = '\''

    # split python_mpi_path individually
    if OS.ispc:
        sep_str = ';'
    else:
        sep_str = ':'
    rank_str = str(rank)

    tmp = python_mpi_path.split(sep_str)
    if DEBUG:
        print(tmp)
    
    # Get host.
    host = pyMPI_Host_name(comm)
    
    # Set OMP_NUM_THREADS to control the number of threads.
    # The default is 1.
    OMP_NUM_THREADS = os.environ.get('OMP_NUM_THREADS', '1')

    comm_pkl_file = 'PythonMPI/MPI_COMM_WORLD.pkl'

    commands = dict()

    add_path_str = ''
    for path in tmp:
        # path needs to be translated in to the LLSC path if the machine is not the host
        dir_pc, dir_linux, dir_mac, dir_grid = pyMPI_Dir_map(comm['machine_db'],path)
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
    commands[1] = 'from pRUN_Parallel_wrapper import *' + nl
    commands[2] = 'pyMCW.MPI_COMM_WORLD = load_dict_from_pickle('+q+comm_pkl_file+q+')' + nl
    commands[3] = 'pyMCW.MPI_COMM_WORLD['+q+'rank'+q+'] = ' + rank_str + nl
    # Additional to define global variables: 
    commands[3] = commands[3]+'pRUN_Parallel_wrapper('+q+py_file+'.py'+q+')' + nl
    # commands[3] = commands[3]+'id=CheckOS()' + nl
    # commands[4] = ['delete(' q defsfile q ');' nl];
    # commands[5] = 'exec(open("'+py_file+'.py").read())'+nl
    commands[5] = ' '

    if DEBUG:
        print('<-- Exiting gen_commands')

    return commands

