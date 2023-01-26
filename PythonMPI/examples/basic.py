"""basic.py
    Basic Pyhton MPI script that
    sends a matrix to another processor.

    To run, start Pyhton and type:

        MPI_Run('basic',2,{})

    Or, to run a different machine type:

        MPI_Run('basic',2,{'machine1' 'machine2'})

    Output will be piped into two files:

        PythonMPI/basic.0.out
        PythonMPI/basic.1.out

    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratory
    {cbyun,kepner}@ll.mit.edu
"""

import numpy as np
from scipy.fft import fft

from PythonMPI import *

# Initialize MPI
MPI_Init()

# Create communicator. (pyMCW is imported in PythonMPI.py)
comm = pyMCW.MPI_COMM_WORLD;

# Modify common directory from default for better performance.
# (Use only when all MPI processes are on the same node)
# comm = pyMPI_Comm_dir(comm,'/tmp');

# Uncomment if you want to save the messages that were sent.
comm = pyMPI_Save_messages(comm,1);

# Get size and rank.
comm_size = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Print rank.
print('my_rank: %d'%(my_rank))

# Set who is source and who is destination.
source = comm_size-1
dest = 0

# Create a unique tag id for this message (very important in Matlab MPI!).
tag = 1

# data type
DTYPE = int
DTYPE = np.float64

# Source.
if (my_rank == source):
    # Create data.
    data = np.arange(10,dtype=DTYPE)
    print(data)
    # Send it.
    MPI_Send( dest, tag, comm, data, data )

# Destination.
if (my_rank == dest):
    #Receive data.
    [data,data1] = MPI_Recv( source, tag, comm )
    print(data)
    # Check data.
    if np.count_nonzero(data - np.arange(10,dtype=DTYPE)):
        raise Exception('ERROR: incorrect data sent.')

# Wait in order to check weather MPI message file is saved if uncommented line 42 above.
pyMPI_Sleep(20)

# Finalize Matlab MPI.
print('SUCCESS')
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
