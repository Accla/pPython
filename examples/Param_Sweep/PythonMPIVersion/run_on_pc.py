"""RUN.py

Example to run a PythonMPI code, param_sweep_parallel.py, with pPython
To run, execute the following command.

    python RUN.py
"""

import os
import sys

# Export the path to find pPython & PythonMPI source code:
PPYTHON_HOME = "Z:\\llgrid_beta\\pPython\\latest"
# PYTHONMPI_PATH = PPYTHON_HOME+os.sep+"PythonMPI"+os.sep+"src"
# sys.path.append(PYTHONMPI_PATH)
PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
os.environ["PPYTHON_HOME"] = PPYTHON_HOME
sys.path.append(PPYTHON_PATH)

GRIDPYTHON_PATH = PPYTHON_HOME+os.sep+"grid"
sys.path.append(GRIDPYTHON_PATH)

# To locate local configuration files
HOME_PATH = "Z:"
os.environ["HOME_PATH"] = HOME_PATH

# Import PythonMPI launch funciton
from pRUN import *

# Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# PythonMPI script filename
py_file = 'param_sweep_parallel.py'
# Define number of MPI processes
n_proc = 4

# Launch PythonMPI
# print('Running: %s via pRUN().'%(py_file))
# pRUN( py_file, n_proc, 'grid&' )
pRUN( py_file, n_proc, 'grid-xeon-p8&')
#pRUN( py_file, n_proc, 'grid-xeon-p8')

