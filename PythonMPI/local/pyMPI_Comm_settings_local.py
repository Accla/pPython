import checkOS as OS

def pyMPI_Comm_settings_local(machine_db_settings):
    """pyMPI_Comm_settings_local  -  Update values in the MPI Communicator setting for local environment.

    Usage:
    ------
    machine_db_settings = pyMPI_Comm_settings(machine_db_settings)
    
    machine_db_settings:   an internal machine database (dtype: dictionary)

    """

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
        python_location = '/usr/bin/python'
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

    # local directory mapping. (pc, linux, mac)
    machine_db_settings['local_dir_map'] = ['Z:', '/home/gridsan/ch21778', '/Volumes/ch21778']

    return machine_db_settings

