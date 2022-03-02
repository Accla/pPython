import numpy as np

from PythonMPI import *
from partition_1d import *

from sample_function import *

# basic parameter sweep code
#
# Want to parallelize the for loop.
#
# Leader process Pid
leader = 0;

# Necessary setup for MPI processes
# Initialize MPI
MPI_Init()

# Create communicator. (pyMCW is imported in PythonMPI.py)
comm = pyMCW.MPI_COMM_WORLD;

# Get size and rank.
n_procs = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Print rank.
print('my_rank: %d'%(my_rank))

# Set data sizes.
m = 3   # number of output arguments
n = 16  # number of independent iterations

# Design data distribution among the MPI processes.
# (partition_1d is distributed with gridPython)
d_index,d_sizes = partition_1d(n,n_procs)
# print(d_index)
# print(d_sizes)
        
# Create z - data output matrix.
z = np.zeros((n, m),dtype=float)

# Get the local portion of the global indices
my_i_global = range(d_index[str(my_rank)]['beg'],d_index[str(my_rank)]['end']+1)

# Get the local portion of the distributed matrix
my_z = z[my_i_global,:]


# Loop over the local indices
i_local = 0
for i_global in my_i_global:
    # Determine the global index for this (local) iteration
    
    # Calculate another argument
    my_other_arg = 2.5 * i_global
    
    # call a function with the global index, and other arguments, and 
    # store the result in a local row
    my_z[i_local,:] = sample_function(i_global, my_rank, my_other_arg)

    # increase local index
    i_local += 1

# local results:
print('local results:')
print(my_z)

# Finally, aggregate all of the output onto the leader process
if my_rank == leader:
    # Update my own results:
    z[my_i_global,:] = my_z

    # while loop for proving incomming messages
    # flag for being done with all processing
    N2 = n_procs-1
    done = 0;

    # Instead of using for loops, use counters
    recvCounter = 1

    while not done:
        # Leader receives all the results.
        if recvCounter <= N2:
            # Compute who sent this message.
            # Do not include leader in data dealing
            message_ranks,message_tags = MPI_Probe('*', '*', comm)

            # if message_ranks is not empty then receive the message
            if len(message_ranks):
                # Receive output.
                source = message_ranks[0]
                tag = message_tags[0]
                print('Waiting on Pid %d' %(source))
                [t1] = MPI_Recv(source,tag,comm)
                # Reshape t1 to update a column vector
                # Note the python index is from 0 to N-1
                my_i_global = range(d_index[str(source)]['beg'],d_index[str(source)]['end']+1)
                z[my_i_global,:] = t1
                print('Received data packet number %d' %(recvCounter))
                recvCounter = recvCounter + 1
            else:
                print('Waiting on data packet %d' %(recvCounter))
                pyMPI_Sleep(2.0)
        else:
            done = 1
else:
    # Send the results back to the leader process
    MPI_Send(leader,1004,comm,my_z)

# Finally, display the resulting matrix on the leader
if my_rank == leader:
    print('globally updated:')
    print(z)

# Finalize the pMATLAB program
print('SUCCESS');

