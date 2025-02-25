"""
An exampl script to run a PythonMPI/pPython code
"""

import re
import os
import sys

# import pPython and pRUN.
import pPython
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

