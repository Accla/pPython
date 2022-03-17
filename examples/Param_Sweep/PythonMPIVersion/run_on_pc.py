"""RUN.py

Example to run a PythonMPI code, param_sweep_parallel.py, with gridPython
To run, execute the following command.

    python RUN.py
"""

import os
import sys

# Export the path to find gridPython & PythonMPI source code:
# GRIDPYTHON_HOME = "/home/gridsan/CH21778/LLGrid/Releases/2022-04/gridPython-v0.1"
GRIDPYTHON_HOME = "Z:\\devtools\\git\\gridPython"
# PYTHONMPI_PATH = GRIDPYTHON_HOME+os.sep+"PythonMPI"+os.sep+"src"
# sys.path.append(PYTHONMPI_PATH)
GRIDPYTHON_PATH = GRIDPYTHON_HOME+os.sep+"src"
os.environ["GRIDPYTHON_HOME"] = GRIDPYTHON_HOME
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

