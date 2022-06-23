"""run_on_llsc.py.py

Example to run a parallel python code, pHPL.py, with gridPython
To run, execute the following command.

    python run_on_llsc.py
"""

import os
import sys

# To locate local configuration files
USER = os.getenv('USER')
HOME_PATH = "/home/gridsan/"+USER
os.environ["HOME_PATH"] = HOME_PATH

# Export the path to find gridPython & PythonMPI source code:
GRIDPYTHON_HOME = "/home/gridsan/groups/llgrid_beta/gridPython/latest"
GRIDPYTHON_PATH = GRIDPYTHON_HOME+os.sep+"src"
os.environ["GRIDPYTHON_HOME"] = GRIDPYTHON_HOME
sys.path.append(GRIDPYTHON_PATH)

# Import PythonMPI launch funciton
from pRUN import *

# Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# PythonMPI script filename
# py_file = 'test_HPL_01.py'
# py_file = 'test_HPL_02.py'
py_file = 'pSpeedtest.py' 
# Define number of MPI processes
n_proc = 4

# Launch PythonMPI
# print('Running: %s via pRUN().'%(py_file))
# pRUN( py_file, n_proc, 'grid&' )
pRUN( py_file, n_proc, 'grid-xeon-e5' )
# pRUN( py_file, n_proc, {} )

