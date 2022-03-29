import re
import os
import sys

# Set gridPython & PythonMPI search path and import it
GRIDPYTHON_HOME = os.getenv('GRIDPYTHON_HOME')
if not GRIDPYTHON_HOME:
    print('ERROR(pRUN): GRIDPYTHON_HOME is not set.')
    exit()
if not os.path.exists(GRIDPYTHON_HOME):
    print('ERROR(pRUN): GRIDPYTHON_HOME path, %s, does not exist.'%(GRIDPYTHON_HOME))
    exit()

# Assuming PythonMPI is distributed with gridPython as shown below
# PythonMPI path must be added first
PYTHONMPI_PATH = GRIDPYTHON_HOME+os.sep+'PythonMPI'+os.sep+'src'
sys.path.append(PYTHONMPI_PATH)

# Additional path for distributed map and array support
GMAP_PATH = GRIDPYTHON_HOME+os.sep+'gmap'+os.sep+'src'
sys.path.append(GMAP_PATH)
DMAT_PATH = GRIDPYTHON_HOME+os.sep+'dmat'+os.sep+'src'
sys.path.append(DMAT_PATH)

# Assuming local configuration is available from $HOME/pythonmpi directory.
# where $HOME is local path matching with GRID_HOME_PATH
HOME_PATH = os.getenv('HOME_PATH')
if not HOME_PATH:
    print('ERROR(pRUN): HOME_PATH is not set.')
    exit()

USER_PYTHONMPI_PATH = HOME_PATH+os.sep+'pythonmpi'
if not os.path.exists(USER_PYTHONMPI_PATH):
    print('ERROR(pRUN): USER_PYTHONMPI_PATH path, %s, does not exist.'%(USER_PYTHONMPI_PATH))
    exit()
sys.path.append(USER_PYTHONMPI_PATH)

GRIDPYTHON_PATH = GRIDPYTHON_HOME+os.sep+'src'
sys.path.append(GRIDPYTHON_PATH)

# for p in sys.path:
#     print(p)

if os.path.exists(PYTHONMPI_PATH):
    import checkOS as OS
    # from PythonMPI import *
    from pyMPI_Delete_all import *
    from pyMPI_Sleep import *
else:
    print('ERROR(pRUN): PythonMPI package path, %s, does not exist.'%(PYTHONMPI_PATH))
    exit()
    
if os.path.exists(GRIDPYTHON_PATH):
    import grid_config as grid
    # from gridPython import *
    from check_allowance import *
    from grid_abort import *
    from grid_config_init import *
    from grid_run import *
    print('gridPython functions are loaded......')
else:
    print('ERROR(pRUN): gridPython package path, %s, does not exist.'%(GRIDPYTHON_PATH))
    exit()

def pRUN(py_file,n_proc,machines,sched_options=None):
    """Launch a PythonMPI script on a grid environment with a scheduler.
    
    Usage:
    ------
    pRUN('py_code.py', n_proc, 'grid', 'scheduler options')
        Launch interactively on a suppored cluster system with the scheduler integration.
    
    pRUN('py_code.py', n_proc, 'grid&')
        Launch as a backgrounded job on a grid environment.
        
    py_file: a PythonMPI code name
    n_proc: number of PythonMPI processes to spawn
    machines: either a string or a list of machines
        'grid': dispatch the job to the default queue (interactive jobs)
        'grid&': backgrounded job to the default queue (entire job is running on the grid)
        []: running on the local machine
        ['machine_a','machine_b',...]: a list of machines to dispatch the job
    sched_options: additional scheduler options when using the scheduler [ToDo]
    
    """
    
    # At this point, grid_config should be set.
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering pRUN')
        for p in sys.path:
            print(p)
        
    # Initialize the grid_config parameters
    grid.grid_config = grid_config_init()

    if DEBUG:
        print(grid.grid_config)

    # Check allowance 
    cpu_type = grid.grid_config['default_cpu_type'] 
    status = check_allowance(n_proc,cpu_type)
    if DEBUG:
        print('pRUN: n_proc,cpu_type = %d, %s'%(n_proc,cpu_type))
        print('check_allowance status: %d'%(status))
    
    # For PC, use ;, For Mac & Linux, use :
    if OS.ispc:
        sep_path = ";"
    else:
        sep_path = ':'
        
    # Construct the PythonMPI search paths
    # For PC, use ;, For Mac & Linux, use :
    if OS.ispc:
        sep_path = ";"
    else:
        sep_path = ':'
        
    GRID_PATH = grid.grid_config['GRIDPYTHON_PATH']+sep_path \
        +grid.grid_config['PYTHONMPI_PATH']+sep_path \
        +grid.grid_config['USER_PYTHONMPI_PATH']+sep_path \
        +grid.grid_config['GMAP_PATH']+sep_path \
        +grid.grid_config['DMAT_PATH']+sep_path \
        +grid.grid_config['CWD_PATH']
    os.environ["PYTHONMPI_PATH"] = GRID_PATH

    # Disable HDF5 file locking
    os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

    # Launch the script.
    print('Running: %s'%(py_file))

    # Clearn up an old PythonMPI run
    if isinstance(machines, str):
        grid_abort(grid.grid_config)
    else:
        grid_abort()
    # wait for the filesystem update
    pyMPI_Sleep(1.0)
    pyMPI_Delete_all()
    # wait for the filesystem update
    pyMPI_Sleep(1.0)

    # Launch PythonMPI
    if DEBUG:
        print('grid_run called . . .')
    cmd = grid_run(py_file, n_proc, machines)

    if DEBUG:
        print('<-- Exiting pRUN')
