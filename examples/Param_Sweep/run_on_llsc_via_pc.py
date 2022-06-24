"""run_on_llsc_via_linux.py

Example to run a PythonMPI code, param_sweep_parallel.py, with gridPython
To run, execute the following command.

    python run_on_llsc_via_mac.py
"""

import os
import sys

HOME_PATH = 'Z:'
os.environ["HOME_PATH"] = HOME_PATH

PPYTHON_HOME = HOME_PATH+"/llgrid_beta/gridPython/latest"
PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
os.environ["PPYTHON_HOME"] = PPYTHON_HOME
sys.path.append(PPYTHON_PATH)

from pRUN import *

os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

py_file = 'param_sweep_parallel.py'
n_proc = 5

# Backgrounded job
# pRUN( py_file, n_proc, 'grid&' )
# Interactive job
pRUN( py_file, n_proc, 'grid' )

