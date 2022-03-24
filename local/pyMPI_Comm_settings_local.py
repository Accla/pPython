import checkOS as OS

def pyMPI_Comm_settings_local(machine_db_settings):
    """pyMPI_Comm_settings_local  -  Update values in the MPI Communicator setting for local environment.

    Usage:
    ------
    machine_db_settings = pyMPI_Comm_settings(machine_db_settings)
    
    machine_db_settings:   an internal machine database (dtype: dictionary)

    python_location: python binary to be used on the grid and on local machine
    python_command: python binary with additional option(s) for python
    python_command_llsc: python binary with additional option(s) for python on LLGrid
    python_module_path: module path on LLGrid where anaconda modules are located
    python_module_name: anaconda module name to be used for PythonMPI

    local_dir_map: local paths matching with the LLGrid home directory path
                   for PC, Linux, and Mac OS environment

    """
    # Grid user
    # USER = 'ch21778'
    USER = os.getenv('USER')

    # Set default type of remote machines to 'unix' (for linux and mac OSes) or 'pc'
    machine_db_settings['type'] = 'unix';     # [OK TO CHANGE.]

    # Set location of python on unix systems.
    # Generic location.  
    python_location = ' python ';   # [OK TO CHANGE.]

    # If this is a unix system, we can
    # try and guess a better location of python on remote
    # machines.  If wrong, then this needs to be hard coded (see below).
    if OS.ispc:
        python_location = 'C:\ProgramData\Anaconda3\python.exe'
        machine_db_settings['python_command'] = python_location + ' -u '
    elif OS.islinux:
        python_location = 'python'
        machine_db_settings['python_command'] = python_location + ' -u '
    elif OS.ismac:
        # python_location = '/usr/bin/python'
        # python_location = '/state/partition1/llgrid/pkg/anaconda/anaconda3-2021b/bin/python'
        python_location = '/opt/anaconda3/bin/python'
        machine_db_settings['python_command'] = python_location + ' -u '
    else:
        print('Error (pyMPI_Comm_settings_local): unsupported OS.')
        exit()

    # LLSC python location
    python_location = '/state/partition1/llgrid/pkg/anaconda/anaconda3-2021b/bin/python'
    machine_db_settings['python_command_llsc'] = python_location + ' -u '
    machine_db_settings['python_module_path'] = '/etc/environment-modules/modules'
    machine_db_settings['python_module_name'] = 'anaconda/2021b'

    # local directory mapping. (pc, linux, mac, grid, sgrp_1)
    machine_db_settings['local_dir_map'] = ['Z:', '/export/home/'+USER, '/Volumes/'+USER, '/home/gridsan/'+USER, '/home/gridsan/groups']

    return machine_db_settings

