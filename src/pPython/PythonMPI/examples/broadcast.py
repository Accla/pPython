"""broadcast.py
    Basic Python MPI script that
    broadcasts a matrix to other processors.
    To run, start Python and type:

         cmd = MPI_Run('broadcast',4,{}) )

    Or, to run a different machine type:

         cmd = MPI_Run('broadcast',4,{'machine1','machine2','machine3','machine4'}) )

    Output will be piped into 4 files:

        MatMPI/broadcast.0.out
        MatMPI/broadcast.1.out
        MatMPI/broadcast.2.out
        MatMPI/broadcast.3.out


    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratory
    {kepner,cbyun}@ll.mit.edu
"""

import numpy as np
from time import time 

from MPI_Init import *
from MPI_Finalize import *
from MPI_Comm_size import *
from MPI_Comm_rank import *
from pyMPI_Sleep import *
from pyMPI_Save_messages import *

from MPI_Send import *
from MPI_Recv import *
from MPI_Bcast import *
from MPI_Probe import *

def gen_matrix(mdim):
    newmat = np.zeros((mdim,mdim),dtype=int)
    for j in range(mdim):
        for i in range(mdim):
            newmat[i,j] = i+j
    return newmat

# Create communicator.
#
# Export Python MPI_COMM_WORLD with pyMCW (defined in PythonMPI.py)
# Kluge to mimick global behavior with MPI_COMM_WORLD
# Python global scope not working properly
# Use pyMCW module to keep MPI_COMM_WORLD as global variable
MPI_COMM_WORLD = pyMCW.MPI_COMM_WORLD
comm = MPI_COMM_WORLD

# Get size and rank.
comm_size = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Print rank.
print('my_rank: %d'%(my_rank))

# Set who is source.
source = 0;

# Create a unique tag id for this message (very important in Python MPI!).
tag = 1;

# Create a reference matrix:
data = gen_matrix(100)

# Check to make sure that we more than one processor.
if(comm_size > 1):
    # Source.
    if (my_rank == source):
        # Create data.
        # data = np.random.rand(100,100)`
        # Send it.
        comm = pyMPI_Save_messages(comm,1)
        # Measure time 
        tic = time()
        [t1, t2] = MPI_Bcast( source, tag, comm, data, data )
        toc = time() 
        comm = pyMPI_Save_messages(comm,0)
        print('Sent data in %f seconds'%(toc-tic))
    # Destination.
    if (my_rank != source):
        # Receive data.
        # data,data1 = MPI_Recv( source, tag, comm )
        [t1, t2] = MPI_Bcast( source, tag, comm, data, data )
        # Check data.
        if(np.count_nonzero(t1 - data)>0):
            raise Exception('ERROR: incorrect data sent.')

print('SUCCESS');
# Finalize Matlab MPI.
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
