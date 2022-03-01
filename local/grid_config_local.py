import os
import platform

import checkOS as OS

def grid_config_local(grid_config):
    """Update local grid_config parameters. """

    # Define grid configuration parameters
    #

    DEBUG = 0
    if DEBUG:
        print('--> Entering grid_config_local')

    # Remote access
    grid_config['remote_host'] = 'txg-login.llgrid.ll.mit.edu'
    grid_config['remote_user'] = 'ch21778'
    grid_config['remote_launch'] = 'ssh'
    grid_config['remote_flags'] = '-q -x'
    #
    # Cluster system
    grid_config['default_q_name'] = 'normal'
    grid_config['default_cpu_type'] = 'xeon-e5'
    grid_config['q_name'] = grid_config['default_q_name']
    grid_config['cpu_type'] = grid_config['default_cpu_type']
    #
    # Paths for PythonMPI installation location and customization
    grid_config['GRID_HOME_PATH'] = '/home/gridsan/ch21778'
    
    # LLGrid Filesystem
    grid_config['LL_FILE_SERVER'] = 'txg-gridfs.llgrid.ll.mit.edu'
    
    # Locally valid paths
    # locally mounted GRID_HOME_PATH
    if os.path.exists('/etc/llgrid.id'):
        HOME_PATH = '/home/gridsan/ch21778'
    else:
        if OS.ispc:
            HOME_PATH = 'Z:'
        elif OS.islinux:
            HOME_PATH = '/home/gridsan/ch21778'
        elif OS.ismac:
            HOME_PATH = '/Volumes/ch21778'
        else:
            print('HOME_PATH is not set. Check OS type.')
            exit()

    # gridPython installation path
    GRIDPYTHON_HOME = os.getenv('GRIDPYTHON_HOME')
    GRIDPYTHON_PATH = GRIDPYTHON_HOME+os.sep+"src"
    # PythonMPI installation path
    PYTHONMPI_PATH = GRIDPYTHON_HOME+os.sep+"PythonMPI"+os.sep+"src"
    # PythonMPI customization path for an individual user
    USER_PYTHONMPI_PATH = HOME_PATH+os.sep+"pythonmpi"
    # Current working directory path
    CWD_PATH = os.getcwd()

    # Save in the grid_config variable
    grid_config['HOME_PATH'] =  HOME_PATH
    grid_config['GRIDPYTHON_PATH'] = GRIDPYTHON_PATH
    grid_config['PYTHONMPI_PATH'] = PYTHONMPI_PATH
    grid_config['USER_PYTHONMPI_PATH'] = USER_PYTHONMPI_PATH
    grid_config['CWD_PATH'] = CWD_PATH

    # Triples modes releated
    grid_config['n_nodes'] = 0

    # Scheduler information
    grid_config['scheduler'] = 'slurm'
    grid_config['ntasks'] = 1

    if DEBUG:
        print(grid_config)
        print('--> Exiting grid_config_local')

    return grid_config

