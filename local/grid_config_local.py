import os
import re
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
    grid_config['GRID_MOUNT_PATH']: locally mounted path for GRID_HOME_PATH
    grid_config['PPYTHON_PATH']: pPython source installation path
    grid_config['PYTHONMPI_PATH']: PythonMPI source installation path
    grid_config['DMAP_PATH']: distributed map source installation path
    grid_config['DMAT_PATH']: distributed array source installation path
    grid_config['LOCAL_PYTHONMPI_CONFIG_PATH']: path for remote user configuration customization files
    grid_config['CWD_PATH']: current working directory path where you submit a job (automatically detected)

    """

    # Define grid configuration parameters
    #

    DEBUG = 0
    if DEBUG:
        print('--> Entering grid_config_local')

    # Am I on a LLGrid system?
    # Set the cluster name to work with
    cluster_name = 'noname'
    if os.path.exists('/etc/llgrid.id'):
        with open('/etc/llgrid.id') as f:
            lines = f.readlines()
        for line in lines:
            # print(line)
            if re.search('txgreen',line,re.IGNORECASE):
                cluster_name = 'txgreen'
            elif re.search('txe1',line,re.IGNORECASE):
                cluster_name = 'txe1'
            elif re.search('txc',line,re.IGNORECASE):
                cluster_name = 'txc'
    else:
        # Manually define
        cluster_name = 'txgreen'
    grid_config['cluster_name'] = cluster_name

    # Grid user (ToDo: need a better way to set the grid username)
    # pick up the local username
    if OS.ispc:
        USER = os.getenv('USERNAME')
    else:
        USER = os.getenv('USER')
    
    if isinstance(USER,type(None)):
        if cluster_name == 'txgreen':
            grid_config['remote_user'] = 'ch21778'
        elif cluster_name == 'txe1':
            grid_config['remote_user'] = 'cbyun'
        else:
            print('grid_config_local: Unsupported system. Exited.')
            exit()
    else:
        # The following line will not work if local username is differen from the grid username
        grid_config['remote_user'] = USER

    # Remote access
    if cluster_name == 'txgreen':
        grid_config['remote_host'] = 'txg-login.llgrid.ll.mit.edu'
    elif cluster_name == 'txe1':
        grid_config['remote_host'] = 'txe1-login.mit.edu'
    else:
        # print('grid_config_local: Unsupported system. Exited.')
        # exit()
        print('grid_config_local: This is not a LLSC system. ')

    grid_config['remote_launch'] = 'ssh'
    grid_config['remote_flags'] = '-q -x'
    #
    # Cluster system
    grid_config['default_q_name'] = 'xeon-p8'
    grid_config['default_cpu_type'] = 'xeon-p8'
    grid_config['q_name'] = grid_config['default_q_name']
    grid_config['cpu_type'] = grid_config['default_cpu_type']
    #
    # Paths for PythonMPI installation location and customization
    grid_config['GRID_HOME_PATH'] = '/home/gridsan/'+grid_config['remote_user']
    
    # LLGrid Filesystem
    grid_config['LL_FILE_SERVER'] = 'txe1-login.mit.edu'
    
    # HOME directory path
    HOME= os.getenv('HOME')

    # locally mounted GRID_HOME_PATH
    if os.path.exists('/etc/llgrid.id'):
        # path on the grid
        GRID_MOUNT_PATH = grid_config['GRID_HOME_PATH']
    else:
        # path on the local machines (required to run jobs on the grid)
        if OS.ispc:
            GRID_MOUNT_PATH = 'Z:'
        elif OS.islinux:
            GRID_MOUNT_PATH = '/home/gridsan/'+USER
        elif OS.ismac:
            GRID_MOUNT_PATH = '/Volumes/'+USER

    # pPython installation path
    try:
        PPYTHON_HOME = os.getenv('PPYTHON_HOME')
        print('grid_config_local: PPYTHON_HOME = %s'%(PPYTHON_HOME))
        PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
        # PythonMPI installation path
        PYTHONMPI_PATH = PPYTHON_HOME+os.sep+"PythonMPI"+os.sep+"src"
        # PythonMPI customization path for an individual user
        if os.path.exists(GRID_MOUNT_PATH):
            LOCAL_PYTHONMPI_CONFIG_PATH = GRID_MOUNT_PATH+os.sep+"pythonmpi"
        else:
            LOCAL_PYTHONMPI_CONFIG_PATH = HOME+os.sep+"pythonmpi"
        # pPython path (codes for scheduler integration)
        GRIDPYTHON_PATH = PPYTHON_HOME+os.sep+"grid"
        # Current working directory path
        CWD_PATH = os.getcwd()
    except Exception:
        print('grid_config_local: Failed to setup environment variables')
        exit()


    # Additional paths for PGAS using the distributed map and array construction
    DMAP_PATH = PPYTHON_PATH+os.sep+"map"
    DMAT_PATH = PPYTHON_PATH+os.sep+"dmat"

    # Save in the grid_config variable
    grid_config['GRID_MOUNT_PATH'] =  GRID_MOUNT_PATH
    grid_config['PPYTHON_PATH'] = PPYTHON_PATH
    grid_config['PYTHONMPI_PATH'] = PYTHONMPI_PATH
    grid_config['LOCAL_PYTHONMPI_CONFIG_PATH'] = LOCAL_PYTHONMPI_CONFIG_PATH
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

