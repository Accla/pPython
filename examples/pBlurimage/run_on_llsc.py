"""RUN.py

Example to run a PythonMPI code with pPython
To run, execute the following command.

    python RUN.py
"""

import os
import sys

# To locate local configuration files
USER = os.getenv('USER')
HOME_PATH = "/home/gridsan/"+USER
os.environ["HOME_PATH"] = HOME_PATH

# Export the path to find gridPython & PythonMPI source code:
# PPYTHON_HOME = "/home/gridsan/groups/llgrid_beta/gridPython/latest"
PPYTHON_HOME = "/home/gridsan/"+USER+"/devtools/git/gridPython"
PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
os.environ["PPYTHON_HOME"] = PPYTHON_HOME
sys.path.append(PPYTHON_PATH)

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
pRUN( py_file, n_proc, 'grid-xeon-e5')
# pRUN( py_file, n_proc, {} )

