# import PythonMPI and pPython
import pyMPI_COMM_WORLD as pyMCW

# from pPython import *
from MPI_Init import *
from MPI_Comm_rank import *
from MPI_Comm_size import *

# pPython class
import pPython as GPC

def pPython_init():
    """Initialize pPython environment.

    Fields of the pPython class:
        comm        - contains the PythonMPI communicator
        Np   - size of communicator, i.e. number of processors
        Pid     - rank of the local processor
        leader      - processor with rank 0
        tag         - message tag
        tag_num     - number of messages sent; synchronized accross all
                      processors in pList
    Fields to be potentially added in the future
        pList       - list of participating processors
        num_tasks   - number of tasks (scopes) created from the beginning of the program
        curr_task   - current task (scope)
        scopes      - contains a cell array of communication scopes; each entry in
        the array is a struct with the current fields of the pMATLAB
        structure plus the task_num field

    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """

    # PythonMPI initialization

    # Initialize PYthonMPI
    MPI_Init()

    # Create communicator. 
    # pyMCW is imported in PythonMPI.py
    # GPC is imported in pPython.py
    GPC.comm = pyMCW.MPI_COMM_WORLD

    # Get size and rank.
    GPC.Np = MPI_Comm_size(GPC.comm)
    GPC.Pid = MPI_Comm_rank(GPC.comm)

    # Set the default leader
    GPC.leader = 0

    # Set the message number and tag
    GPC.tag_num = 0;
    # message tag - MUST be unique for each message
    GPC.tag = 'tag-'+str(GPC.tag_num)

    return

########################################################
# pMatlab: Parallel Matlab Toolbox
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2005, Massachusetts Institute of Technology All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#      * Neither the name of the Massachusetts Institute of Technology nor
#        the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written
#        permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
