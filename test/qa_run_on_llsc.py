"""
An exampl script to run a PythonMPI/pPython code
"""

import re
import os
import sys

RUN_ON_SOURCE=os.getenv('PPYTHON_RUN_ON_SOURCE',default='')
if len(RUN_ON_SOURCE):
    # Set to run pPython code from a source installation directory
    """
    Customization for the user runtime environment
    """
    HOME_PATH = os.getenv('HOME')
    PPYTHON_HOME = HOME_PATH + "/devtools/git/pPython/src/pPython"
    os.environ["PPYTHON_HOME"] = PPYTHON_HOME

    # Add Python search path for pPython main function
    PPYTHON_PATH = PPYTHON_HOME+os.sep+"src"
    sys.path.append(PPYTHON_PATH)

    #Update PYTHONPATH to direct to the pPython modules from the source location
    PYTHONPATH=PPYTHON_HOME+os.sep+'PythonMPI'+os.sep+'src'
    PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME+os.sep+'grid'
    PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME+os.sep+'src'
    PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME+os.sep+'src'+os.sep+'map'
    PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME+os.sep+'src'+os.sep+'dmat'
    PYTHONPATH=PYTHONPATH+':'+PPYTHON_HOME
    os.environ["PYTHONMPI"]=PYTHONPATH
    # print('PYTHONMPI=%s'%(PYTHONPATH))

    # Disable HDF5 file locking (Lustre parallel filesystem on LLSC)
    os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"

# import pPython and pRUN.
# import pPython
from pRUN import pRUN

# Python environment variable to define a pPython script filename and runtime environment
PPYTHON_CLASSIC = os.getenv('PPYTHON_CLASSIC')
QA_PYFILE = os.getenv('QA_PYFILE')
QA_NPROCS = int(os.getenv('QA_NPROCS'))
QA_NPPN = int(os.getenv('QA_NPPN',1))
QA_MACHINES = os.getenv('QA_MACHINES','grid&')
QA_EXTRA = os.getenv('QA_EXTRA')
py_file = QA_PYFILE

# Define number of MPI processes
# Define machines
if re.search('grid',QA_MACHINES):
    if PPYTHON_CLASSIC:
        # classic mode
        n_proc = QA_NPROCS
    else:
        # triples mode
        nppn = QA_NPPN
        n_proc = [QA_NPROCS,nppn,3]
    machines = QA_MACHINES
else:
    # running locally
    n_proc = QA_NPROCS
    machines = {}

# Launch 
# pRUN(py_file, n_proc, machines, '--reservation=anaconda')
if QA_EXTRA:
    pRUN(py_file, n_proc, machines, QA_EXTRA)
else:
    pRUN(py_file, n_proc, machines)

