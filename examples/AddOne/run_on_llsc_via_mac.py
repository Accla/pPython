"""run_on_llsc_via_mac.py

Example to run a PythonMPI code, param_sweep_parallel.py, with gridPython
To run, execute the following command.

    python run_on_llsc_via_mac.py
"""

import os
import sys

USER = os.getenv('USER')
HOME_PATH = "/Volumes/"+USER
os.environ["HOME_PATH"] = HOME_PATH

GRIDPYTHON_HOME = HOME_PATH+"/llgrid_beta/gridPython/Ver-0.5.0"
GRIDPYTHON_PATH = GRIDPYTHON_HOME+os.sep+"src"
os.environ["GRIDPYTHON_HOME"] = GRIDPYTHON_HOME
sys.path.append(GRIDPYTHON_PATH)

from pRUN import *

os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

py_file = 'pAddOne.py'
n_proc = 3

# Backgrounded job
# pRUN( py_file, n_proc, 'grid&' )
# Interactive job
pRUN( py_file, n_proc, 'grid' )

