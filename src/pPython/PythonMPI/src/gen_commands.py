import os

import checkOS as OS
from pyMPI_Dir_map import *
from pyMPI_Host_name import *

def gen_commands(py_file,python_mpi_path,rank,machine,comm,EPPAC=False):
    """
    Generate Python commands to be executed before calling pPUN_Parallel_wrapper()

    Author: Dr. Chansup Byun
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering gen_commands')
        # print('EPPAC = ',end=" ")
        # print(EPPAC)
        # print(" ")
    
    # Set variables for special string.
    nl = '\n'
    # Get single quote character. 
    q = '\''

    # split python_mpi_path individually
    if OS.ispc:
        sep_str = ';'
    else:
        sep_str = ':'
    rank_str = str(rank)

    tmp = python_mpi_path.split(sep_str)
    if DEBUG:
        print(tmp)
    
    # Get host.
    host = pyMPI_Host_name(comm)
    
    # Set OMP_NUM_THREADS to control the number of threads.
    # The default is 1.
    OMP_NUM_THREADS = os.environ.get('OMP_NUM_THREADS', '1')

    comm_pkl_file = 'PythonMPI/MPI_COMM_WORLD.pkl'

    commands = dict()
    commands[0] = 'import os'+nl+'import sys'+nl+'sys.path.append(".")'+nl
    PYTHONMPI = os.getenv('PYTHONMPI',default='')
    if len(PYTHONMPI):
        PPYTHON_HOME=os.getenv("PPYTHON_HOME")
        commands[0] = commands[0]+'sys.path.append("'+PPYTHON_HOME+'")'+nl
        commands[0] = commands[0]+'sys.path.append("'+PPYTHON_HOME+'/PythonMPI/src")'+nl
        commands[0] = commands[0]+'sys.path.append("'+PPYTHON_HOME+'/src")'+nl
        commands[0] = commands[0]+'os.environ["PYTHONMPI"]="'+PYTHONMPI+'"'+nl
    commands[0] = commands[0]+'os.environ["HDF5_USE_FILE_LOCKING"]="FALSE"' + nl
    if EPPAC:
        # For the triples mode, a single script launches many pPython MPI processes.
        # Each process will inherit OMP_NUM_THREADS environment variable exported by the script
        # So no need to set.
        commands[0] = commands[0] + nl
    else:
        commands[0] = commands[0]+'os.environ["OMP_NUM_THREADS"]="' + OMP_NUM_THREADS + '"' + nl
    # commands[0] = commands[0]+'from PythonMPI import *' + nl
    commands[0] = commands[0]+'# import pPython' + nl
    commands[0] = commands[0]+'import pyMPI_COMM_WORLD as pyMCW' + nl
    commands[0] = commands[0]+'from dict_with_pickle import load_dict_from_pickle' + nl
    commands[1] = 'from pRUN_Parallel_wrapper import *' + nl
    commands[2] = 'pyMCW.MPI_COMM_WORLD = load_dict_from_pickle('+q+comm_pkl_file+q+')' + nl
    if EPPAC:
        # For the triples mode, a single script launches many pPython MPI processes.
        # Each process will get its rank from MPI_COMM_WORLD_RANK environment variable exported by the script
        commands[3] = 'pyMCW.MPI_COMM_WORLD['+q+'rank'+q+'] = ' + 'int(os.getenv('+q+'MPI_COMM_WORLD_RANK'+q+'))' + nl
    else:
        commands[3] = 'pyMCW.MPI_COMM_WORLD['+q+'rank'+q+'] = ' + rank_str + nl
    # Additional to define global variables: 
    commands[3] = commands[3]+'pRUN_Parallel_wrapper('+q+py_file+'.py'+q+')' + nl
    # commands[3] = commands[3]+'id=CheckOS()' + nl
    # commands[4] = ['delete(' q defsfile q ');' nl];
    # commands[5] = 'exec(open("'+py_file+'.py").read())'+nl
    commands[5] = ' '

    if DEBUG:
        print('<-- Exiting gen_commands')

    return commands

########################################################
# PythonMPI
# Dr. Jeremy Kepner & Dr. Chansup Byun
# MIT Lincoln Laboratory
# kepner@ll.mit.edu & cbyun@ll.mit.edu
########################################################
# Copyright 2023 Massachusetts Institute of Technology
#
# Permission is herby granted, without payment, to copy, modify, display
# and distribute this software and its documentation, if any, for any
# purpose, provided that the above copyright notices and the following
# three paragraphs appear in all copies of this software.  Use of this
# software constitutes acceptance of these terms and conditions.
#
# IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
# THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
#
# THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.
