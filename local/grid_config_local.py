import os
import platform

import checkOS as OS

def grid_config_local(grid_config):
    """Update local grid_config parameters. 

    Usage:
    ------

    grid_config = grid_config_local(grid_config)

    Update the following information.

    grid_config['remote_host']: the fully qualified hostname to access the scheduler
    grid_config['remote_user']: username on the grid
    grid_config['remote_launch']: command used to access the remote host
    grid_config['remote_flags']: flags used by the remote launch command

    grid_config['q_name']: the queue (partition) name where the job is submitted to
    grid_config['cpu_type']: the CPU type for the nodes in the queue (deprecated in the future compute nodes
                             bacause each queue will have only one CPU-type node)
    grid_config['default_q_name']: default queue (partition) name
    grid_config['default_cpu_type']: default CPU type name 

    grid_config['LL_FILE_SERVER'] = file server name to mount grid home directory locally

    grid_config['GRID_HOME_PATH']: home directory path on the grid for the remote user
    grid_config['HOME_PATH']: locally mounted path for GRID_HOME_PATH
    grid_config['PPYTHON_PATH']: gridPython source installation path
    grid_config['PYTHONMPI_PATH']: PythonMPI source installation path
    grid_config['DMAP_PATH']: distributed map source installation path
    grid_config['DMAT_PATH']: distributed array source installation path
    grid_config['USER_PYTHONMPI_PATH']: path for remote user configuration customization files
    grid_config['CWD_PATH']: current working directory path where you submit a job (automatically detected)

    """

    # Define grid configuration parameters
    #

    DEBUG = 0
    if DEBUG:
        print('--> Entering grid_config_local')

    # Grid user
    USER = os.getenv('USER')

    # Remote access
    grid_config['remote_host'] = 'txg-login.llgrid.ll.mit.edu'
    grid_config['remote_user'] = USER
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
    grid_config['GRID_HOME_PATH'] = '/home/gridsan/'+grid_config['remote_user']
    
    # LLGrid Filesystem
    grid_config['LL_FILE_SERVER'] = 'txg-gridfs.llgrid.ll.mit.edu'
    
    # locally mounted GRID_HOME_PATH
    if os.path.exists('/etc/llgrid.id'):
        # path on the grid
        HOME_PATH = grid_config['GRID_HOME_PATH']
    else:
        # path on the local machines
        if OS.ispc:
            HOME_PATH = 'Z:'
        elif OS.islinux:
            HOME_PATH = '/export/home/'+USER
        elif OS.ismac:
            HOME_PATH = '/Volumes/'+USER
        else:
            print('HOME_PATH is not set. Check OS type.')
            exit()

    # gridPython installation path
    PPYTHON_HOME = os.getenv('PPYTHON_HOME')
    PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
    # PythonMPI installation path
    PYTHONMPI_PATH = PPYTHON_HOME+os.sep+"PythonMPI"+os.sep+"src"
    # PythonMPI customization path for an individual user
    USER_PYTHONMPI_PATH = HOME_PATH+os.sep+"pythonmpi"
    # gridPython path (codes for scheduler integration)
    GRIDPYTHON_PATH = PPYTHON_HOME+os.sep+"grid"
    # Current working directory path
    CWD_PATH = os.getcwd()

    # Additional paths for PGAS using the distributed map and array construction
    DMAP_PATH = PPYTHON_HOME+os.sep+"dmap"+os.sep+"src"
    DMAT_PATH = PPYTHON_HOME+os.sep+"dmat"+os.sep+"src" 

    # Save in the grid_config variable
    grid_config['HOME_PATH'] =  HOME_PATH
    grid_config['PPYTHON_PATH'] = PPYTHON_PATH
    grid_config['PYTHONMPI_PATH'] = PYTHONMPI_PATH
    grid_config['USER_PYTHONMPI_PATH'] = USER_PYTHONMPI_PATH
    grid_config['GRIDPYTHON_PATH'] = GRIDPYTHON_PATH
    grid_config['CWD_PATH'] = CWD_PATH

    # Additional paths for PGAS using the distributed map and array construction
    grid_config['DMAP_PATH'] = DMAP_PATH
    grid_config['DMAT_PATH'] = DMAT_PATH

    # Triples modes releated
    grid_config['n_nodes'] = 0

    # Scheduler information
    grid_config['scheduler'] = 'slurm'
    grid_config['ntasks'] = 1

    if DEBUG:
        print(grid_config)
        print('--> Exiting grid_config_local')

    return grid_config

