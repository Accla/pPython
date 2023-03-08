import os

import pyMPI_COMM_WORLD as pyMCW
import checkOS as OS

from pyMPI_Dir_map import *

def MPI_Init():
    """MPI_Init  -  Called at the start of an MPI program.

    Usage:
    ------
    MPI_Init()
    
    Called at the beginning of an MPI program.
    
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering MPI_Init.')
        print(pyMCW.MPI_COMM_WORLD)

    # Convert pc and unix directories.
    # OS.islocal = pyMCW.MPI_COMM_WORLD['islocal']
    OS.islocal = pyMCW.MPI_COMM_WORLD['grid_config']['islocal']
    for ii in range(pyMCW.MPI_COMM_WORLD['machine_db']['n_machine']):
        dir = pyMCW.MPI_COMM_WORLD['machine_db']['dir'][ii]
        dir_pc, dir_linux, dir_mac, dir_grid = pyMPI_Dir_map(pyMCW.MPI_COMM_WORLD['machine_db'],dir)

        if os.path.exists('/etc/llgrid.id'):
            pyMCW.MPI_COMM_WORLD['machine_db']['dir'][ii] = dir_grid
        else:
            if (OS.ispc):
                pyMCW.MPI_COMM_WORLD['machine_db']['dir'][ii] = dir_pc
            elif (OS.islinux):
                pyMCW.MPI_COMM_WORLD['machine_db']['dir'][ii] = dir_linux
            elif (OS.ismac):
                pyMCW.MPI_COMM_WORLD['machine_db']['dir'][ii] = dir_mac
    if DEBUG:
        print('<-- Exiting MPI_Init.')
    return

########################################################
# MatlabMPI
# Dr. Jeremy Kepner
# MIT Lincoln Laboratory
# kepner@ll.mit.edu
########################################################
# Copyright 2002 Massachusetts Institute of Technology
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
