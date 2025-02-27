"""xbasic.py
    Basic Python MPI script that
    prints out a rank.

    To run, start Matlab and type:

        MPI_Run('xbasic',2,{})

    Or, to run a different machine type:

        MPI_Run('xbasic',2,{'machine1' 'machine2'})

    Output will be piped into two files:

        PythonMPI/xbasic.0.out
        PythonMPI/xbasic.1.out


    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratory
    {cbyun,kepner}@ll.mit.edu
"""

import numpy as np
from scipy.fft import fft

from pyMPI_Comm_dir import *
from pyMPI_Sleep import *
from MPI_Init import *
from MPI_Comm_size import *
from MPI_Comm_rank import *
from MPI_Finalize import *

# Initialize MPI
MPI_Init()

# import MPI_COMM_WORLD (defined in PythonMPI.py)
MPI_COMM_WORLD = pyMCW.MPI_COMM_WORLD

#  Create communicator.
comm = MPI_COMM_WORLD

# Get size and rank.
comm_size = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Modify common directory from default for better performance.
comm = pyMPI_Comm_dir(comm,'/tmp');

# Print rank.
print('my_rank: %d'%(my_rank))

# Wait momentarily.
pyMPI_Sleep(2.0)

# Finalize Matlab MPI.
print('SUCCESS');
MPI_Finalize()

"""
 Copyright 2002 Massachusetts Institute of Technology
 
 Permission is herby granted, without payment, to copy, modify, display
 and distribute this software and its documentation, if any, for any
 purpose, provided that the above copyright notices and the following
 three paragraphs appear in all copies of this software.  Use of this
 software constitutes acceptance of these terms and conditions.

 IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
 SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
 THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
 
 MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
 BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

 THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
 MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.
"""

