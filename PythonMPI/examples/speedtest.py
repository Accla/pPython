"""speedtest.py
    This script times MPI_Send/MPI_Recv for
    a variety of message sizes.
    To run, start Python and type:

        MPI_Run('speedtest',2,{})

    Or, to run a different machine type:

        MPI_Run('speedtest',2,{'machine1' 'machine2'})

    Output will be piped into to

        PythonMPI/speedtest.0.out
        PythonMPI/speedtest.0.h5
        PythonMPI/speedtest.1.out
        PythonMPI/speedtest.1.h5
      ...


    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratory
    {cbyun,kepner}@ll.mit.edu
"""
import numpy as np
import pickle
from timeit import default_timer as timer
# import time

from PythonMPI import *
from synch_start import *

DEBUG = 0

# Initialize MPI
MPI_Init()

# Create communicator. (pyMCW is imported in PythonMPI.py)
comm = pyMCW.MPI_COMM_WORLD

# Modify common directory from default for better performance.
# (Use only when all MPI processes are on the same node)
# comm = pyMPI_Comm_dir(comm,'/tmp')

# Get size and rank.
comm_size = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Print rank.
print('my_rank: %d'%(my_rank))

# Set the number message sizes.
n_message = 28
# Test
n_message = 20

# Set the number of trials at each messages size.
n_trial = 4

# Modify common directory from default for better performance.
# Work only if all MPI processes have access to the path
# comm = MatMPI_Comm_dir(comm,'/tmp');
# comm = MatMPI_Comm_dir(comm,'/wulf/share/kepner');
# comm = MatMPI_Comm_dir(comm,'/gigabit/node-a');

# Do a synchronized start.
starter_rank = 0
# add delay in seconds to synchronize all MPI processes.
delay = 30
synch_start(comm,starter_rank,delay)

if(comm_size < 2):
    print('ERROR: too few processors (need at least 2)')
    exit()

# Set who is source and who is destination.
source = my_rank - 1
if (source < 0):
  source = comm_size - 1
dest = my_rank + 1
if (dest >= comm_size):
  dest = 0;

# Create a unique tag id for this message (very important in Python MPI!).
tag = 1

# Create timing matrices.
start_time = np.zeros([n_trial,n_message])
end_time = np.zeros([n_trial,n_message])

# Compute message sizes.
p = np.arange(n_message)+1
message_size = np.power(2,p)
byte_size = 8*message_size

# Get a zero clock.
zero_clock = timer()

# Loop over each message size.
for i_message in range(n_message):
    # Create message.
    send_data = np.zeros([1,message_size[i_message]])+ my_rank
    send_data_bytes = send_data.nbytes

    for i_trial in range(n_trial):
        # Get start time for this message.
        start_time[i_trial,i_message] = timer()

        # Send data.
        MPI_Send( dest, tag, comm, send_data )

        # Recieve data.
        [recv_data] = MPI_Recv( source, tag, comm )

        # Get end time for the this message.
        end_time[i_trial,i_message] = timer()

        if DEBUG:
            print('Start: %f'%(start_time[i_trial,i_message]))
            print('End: %f'%(end_time[i_trial,i_message]))

        total_time = end_time[i_trial,i_message] - start_time[i_trial,i_message]
        if DEBUG:
            print('time[trial:%d,message id:%d] = %f'%(i_trial,i_message,total_time))

        # Check data.
        if np.count_nonzero(recv_data - source):
            print('ERROR: incorrect data sent.')
            exit()

        # Increment message tag.
        tag = tag + 1

# Compute bandwidth.
total_time = end_time - start_time
byte_size_matrix = byte_size * np.ones([4,1])
bandwidth = 2*byte_size_matrix/total_time

# Write data to a file.
outfile = 'speedtest.'+str(my_rank)+'.pkl'
with open(outfile,'wb') as f:
    pickle.dump([byte_size,start_time,end_time,total_time,byte_size_matrix,bandwidth], f)

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
