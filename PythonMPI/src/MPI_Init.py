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
    
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering MPI_Init.')
        print(pyMCW.MPI_COMM_WORLD)

    # Convert pc and unix directories.
    for ii in range(pyMCW.MPI_COMM_WORLD['machine_db']['n_machine']):
        iistr = str(ii)
        dir = pyMCW.MPI_COMM_WORLD['machine_db']['dir'][iistr]
        dir_pc, dir_linux, dir_mac, dir_grid = pyMPI_Dir_map(pyMCW.MPI_COMM_WORLD['machine_db'],dir)

        if os.path.exists('/etc/llgrid.id'):
            pyMCW.MPI_COMM_WORLD['machine_db']['dir'][iistr] = dir_grid
        else:
            if (OS.ispc):
                pyMCW.MPI_COMM_WORLD['machine_db']['dir'][iistr] = dir_pc
            elif (OS.islinux):
                pyMCW.MPI_COMM_WORLD['machine_db']['dir'][iistr] = dir_linux
            elif (OS.ismac):
                pyMCW.MPI_COMM_WORLD['machine_db']['dir'][iistr] = dir_mac
    if DEBUG:
        print('<-- Exiting MPI_Init.')

