"""baisc_app.py
    Basic example of a typical application PythonMPI might be used for.  
    Takes a matrix, breaks it up among processors, does a computation, 
    and gathers the results.

    To run, start Python and type:

        MPI_Run('basic_app',4,{})

    Or, to run a different machine type:

        MPI_Run('basic_app',4,{'machine1' 'machine2' 'machine3' 'machine4'})

    Output will be piped into 4 files:

        MatMPI/basic_app.0.out
        MatMPI/basic_app.1.out
        MatMPI/basic_app.2.out
        MatMPI/basic_app.3.out

    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratory
    {kepner,cbyun}@ll.mit.edu
"""

import numpy as np
from scipy.fft import fft,ifft

from MPI_Init import *
from MPI_Finalize import *
from MPI_Comm_size import *
from MPI_Comm_rank import *
from pyMPI_Sleep import *

from MPI_Send import *
from MPI_Recv import *
from MPI_Bcast import *

DEBUG = 0

# Create communicator.
"""Import MPI_COMM_WORLD with Python pyMCW module
    (defined in PythonMPI.py and called in by MPI_Run())
    This is a work around to mimick MATLAB global variable, MPI_COMM_WORLD
    becauses Python global scope is not working consistently across multiple module files.
"""
MPI_COMM_WORLD = pyMCW.MPI_COMM_WORLD
comm = MPI_COMM_WORLD;

# Get size and rank.
comm_size = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Print rank.
print('my_rank: %d'%(my_rank))

# Wait momentarily.
pyMPI_Sleep(2.0)

# Set who is the leader
leader = 0;

# Create base message tags.
coefs_tag = 10000;
input_tag = 20000;
output_tag = 30000;

if DEBUG:
    # Debugging purpose
    N1 = 10
    N2 = 7
else:
    # Set data sizes.
    N1 = 1000
    N2 = 70
    N1 = 10
    N2 = 7

# Leader.
if (my_rank == leader):
    # Create coefficient data.
    coefs = np.ones([N1,1],dtype=int)

    # Create input data.
    input = np.ones([N1,N2],dtype=int)

    # Create output data array.
    output = np.zeros([N1,N2],dtype=int)

    # Broadcast coefficients to everyone else.
    [t1] = MPI_Bcast( leader, coefs_tag, comm, coefs );

    # Deal input data to everyone else including self.
    for i in range(N2):
        dest = i%comm_size
        dest_tag = input_tag + i;
        # Keep the data as a column vector
        # dest_data = input[:,i]
        dest_data = np.reshape(input[:,i],[N1,1])
        if DEBUG:
            print('dest_data:')
            print(dest_data)
        MPI_Send(dest,dest_tag,comm,dest_data)

# Everyone but the leader receives the coefs.
if (my_rank != leader):
    coefs = 0
    # Receive coefs.
    # coefs = MPI_Recv( leader, coefs_tag, comm )
    [coefs] = MPI_Bcast( leader, coefs_tag, comm, coefs );

# Everyone receives the input data and processes the results.
for i in range(N2):
    # Compute who the destination is for this message.
    dest = i%comm_size

    # Check if this destination is me.
    if (my_rank == dest):
        # Compute tags.
        dest_tag = input_tag + i
        leader_tag = output_tag + i

        # Receive input.
        [i_input] =  MPI_Recv(leader,dest_tag,comm);
        if DEBUG:
            print('i_input:')
            print(i_input)

        # Do computation.
        i_output = ifft(np.multiply(fft(coefs),i_input))

        # Send results back to the leader.
        if DEBUG :
            # i_output is a list data type
            print('i_output:')
            print(i_output)
            # print(type(i_output))
        MPI_Send(leader,leader_tag,comm,i_output)

# Leader receives all the results.
if (my_rank == leader):
    for i in range(N2):
        # Compute who sent this message.
        dest = i % comm_size
        leader_tag = output_tag + i
        # Receive output.
        [t1] = MPI_Recv(dest,leader_tag,comm)
        if DEBUG == False :
            print('Received array:')
            print(t1)
            # print(type(t1))
        # t1 = np.asarray(t1)
        output[:,i] = np.reshape(t1,[1,N1])
    if DEBUG :
        print('output:')
        print(output)

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
