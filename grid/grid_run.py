import math
import re
import os

import checkOS as OS
import pyMPI_COMM_WORLD as pyMCW
from MPI_Run import *

from pyMPI_Comm_init import *
from pyMPI_Commands import *
from pyMPI_Dir_map import *
from pyMPI_Sleep import *

import grid_config as grid
from exec_shell_cmd import *
from grid_resource_policy  import *
from slurm_write_job_script import *
from slurm_submit_job import *
from launch_non_triples import *
from launch_with_triples import *

def grid_run( py_file, n_proc, machines ):
    """
    grid_run  -  Run py_file on multiple processors on LLGrid.
                 Refactored for modified MPI_Run from pPython

    Usage:
    ------
    defscommands = grid_run( py_file, n_proc, machines )

    Runs n_proc copies of py_file on machines, where

    machines = 'grid'   (dtype: string)
        Run on a LLGrid system interactively.

    machines = 'grid&'   (dtype: string)
        Run on a LLGrid system in a backgrounded mode.

    py_file:  the python script name (dtype: string)
    n_proc:   total number of MPI processes (dtype: int)
    machines: a dictionary variable
              preprocessed in check_runtime()
    
    defscommands: command to run locally if machine is a local machine

    Author: Dr. Chansup Byun
    """

    DEBUG = 0

    if DEBUG:
        print('--> Entering grid_run (pPython version of MPI_Run).')
        print('grid_run(MPI_Run): isunix, ismac, islinux, ispc = %d,%d,%d,%d'%(OS.isunix, OS.ismac, OS.islinux, OS.ispc))
    
    # Set some strings for special characters.
    qq = '"'
    sp = ' '
    nl = '\n'
    # Get single quote character. 
    q = '\''
    
    # Unix vs. Windows file seperator.
    dir_sep = os.sep

    # Unix vs. Windows host name.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')

    # Determine whether it is an interactive or backgrounded job
    if DEBUG:
        print('machines: %s'%(machines))

    # Recover variables processed in check_runtime()
    islocal = grid.grid_config['islocal']
    cpu_type = grid.grid_config['cpu_type']
    grid_job = grid.grid_config['grid_job']
    interactive = grid.grid_config['interactive']

    OS.islocal = islocal
    if DEBUG:
        print('OS.islocal = %d'%(OS.islocal))

    # Check if the directory 'PythonMPI' exists
    checkPath = '.'+os.sep+'PythonMPI'
    if os.path.isdir(checkPath):
        raise Exception('Error: PythonMPI directory already exists: rename or remove with pyMPI_Delete_all')
    else:
        os.makedirs(checkPath, exist_ok=True)

    # Create generic comm. (Initialize global pyMCW.MPI_COMM_WORLD)
    #
    # The grid.grid_config should be passed to pyMPI_Comm_init()
    # because pyMPI_Comm_init() saves MPI_COMM_WORLD.
    # When each pPython process starts, it read MPI_COMM_WORLD.
    #
    pyMCW.MPI_COMM_WORLD = pyMPI_Comm_init(n_proc,machines,grid_config=grid.grid_config);

    if not grid_job:
        #
        # Call PythonMPI MPI_Run
        defscommands = MPI_Run(py_file, n_proc, machines, python_mpi_keep=True)
        if DEBUG:
            print(defscommands)
            print('. . .')
            print('<-- Exiting grid_run (MPI_Run).')
        return defscommands

    # For grid jobs
    # Set paths.
    if DEBUG:
        # print(pyMCW.MPI_COMM_WORLD['machine_db'])
        print(pyMCW.MPI_COMM_WORLD['grid_config'])
        print(os.getcwd())

    
    
    ## Work in Progress
    
    
    
    if (grid.grid_config['EPPAC'] == True):
        #
        # Triples mode job
        #
        if DEBUG:
            print('grid_run: call launch_with_triples')
        # defscommands = MPI_RunG_MC()
        defscommands = launch_with_triples(py_file,pyMCW.MPI_COMM_WORLD,grid.grid_config)
        
    else:
        #
        # Non-triples mode job
        #
        if DEBUG:
            print('grid_run: call launch_non_triples')
        # defscommands = MPI_RunG()
        defscommands = launch_non_triples(py_file,pyMCW.MPI_COMM_WORLD,grid.grid_config)
    
    return defscommands

########################################################
# gridMatlab
# Dr. Albert Reuther
# reuther@ll.mit.edu
# MIT Lincoln Laboratory
########################################################
# Copyright 2003-9 Massachusetts Institute of Technology
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
