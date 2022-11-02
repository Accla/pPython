"""RUN.py

Example to run a PythonMPI code with pPython
To run, execute the following command.

    python RUN.py
"""

import os
import sys

# To locate local configuration files
USER = os.getenv('USER')
if os.getenv('HOME_PATH'):
    HOME_PATH = os.environ["HOME_PATH"]
    print('Obtained HOME_PATH from environment setup as %s'%(HOME_PATH))
else:
    # On LLSC environment
    HOME_PATH = os.getenv('HOME')
    os.environ["HOME_PATH"] = HOME_PATH
    print('HOME_PATH is set in the run script as %s'%(HOME_PATH))

# Export the path to find pPython & PythonMPI source code:
if os.getenv('PPYTHON_HOME'):
    PPYTHON_HOME = os.getenv('PPYTHON_HOME')
    print('Obtained PPYTHON_HOME from environment setup')
    print('PPYTHON_HOME is set in the runtime environment as %s'%(PPYTHON_HOME))
else:
    # PPYTHON_HOME = "/home/gridsan/groups/llgrid_beta/pPython/latest"
    # PPYTHON_HOME = HOME_PATH+"/devtools/git/pPython"
    PPYTHON_HOME = HOME_PATH
    print('PPYTHON_HOME is set in the run script as %s'%(PPYTHON_HOME))
    os.environ['PPYTHON_HOME'] = PPYTHON_HOME

# Export the path to find pPython & PythonMPI source code:
# PPYTHON_HOME = "/home/gridsan/groups/llgrid_beta/pPython/latest"
# PPYTHON_HOME = "/home/gridsan/"+USER+"/devtools/git/pPython"
PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
os.environ["PPYTHON_HOME"] = PPYTHON_HOME
sys.path.append(PPYTHON_PATH)

GRIDPYTHON_PATH = PPYTHON_HOME+os.sep+"grid"
sys.path.append(GRIDPYTHON_PATH)

# Local configuration setup
LOCAL_PYTHONMPI_CONFIG_PATH = os.getenv('HOME')+os.sep+"pythonmpi"
sys.path.append(LOCAL_PYTHONMPI_CONFIG_PATH)

# Import PythonMPI launch funciton
from pRUN import *

# Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# PythonMPI script filename
py_file = 'pBlurimage.py'
# Define number of MPI processes
n_proc = 4

# Launch PythonMPI
# print('Running: %s via pRUN().'%(py_file))
# pRUN( py_file, n_proc, 'grid&' )
# pRUN( py_file, n_proc, 'grid-xeon-p8&','--exclusive' )
pRUN( py_file, n_proc, {} )

