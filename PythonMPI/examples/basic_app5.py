"""basic_app5.py
    Basic example of a typical application for which 
    PythonMPI might be used.  It uses a leader that manages, 
    and workers that conduct the processing. This example 
    takes a matrix, breaks it up among processors, does a 
    computation, and gathers the results to display in a 
    figure window.

    This example builds on basic_app4.py. It keeps track of 
    each of the jobs that must be completed, and keeps track 
    of whether each of the worker processes are busy or not. 
    If there are more jobs to be completed and one of the worker 
    processes is not busy, then it sends the next sequential 
    row of the input matrix to that process. 
    It also asynchronously receives completed columns of the 
    output matrix in that the leader uses the MPI_Probe 
    function to determine whether a worker process has 
    sent a completed computation packet. The leader sends 
    a packet to be processed and then probes for a packet 
    that was sent to itself. If a packet has 
    been sent back, the leader processes the packet; if no 
    packet has been sent, then the leader determines whether 
    another work column should be sent to another worker. 
    If all of the workers are busy, the leader just waits 
    until any competed work has been returned.  

    This example can also plot the data on a graph figure. 
    To enable this feature, set the variable UseGraphics 
    equal to 1. 

    To run, start Matlab and type:

        MPI_Run('basic_app5',4,{}) 

    Or, to run a different machine type:

        MPI_Run('basic_app5',4,{'machine1' 'machine2' 'machine3' 'machine4'})

    Output will be piped into 4 files:

        PythonMPI/basic_app5.0.out
        PythonMPI/basic_app5.1.out
        PythonMPI/basic_app5.2.out
        PythonMPI/basic_app5.3.out

    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Albert Reuther
    MIT Lincoln Laboratory
    {cbyun,reuther}@ll.mit.edu
"""

import numpy as np
from scipy.fft import fft

from PythonMPI import *

# Set whether a graph should be generated
UseGraphics = 0
if UseGraphics:
    import matplotlib.pyplot as plt

# import MPI_COMM_WORLD (defined in PythonMPI.py)
MPI_COMM_WORLD = pyMCW.MPI_COMM_WORLD

# Initialize MPI
MPI_Init()

#  Create communicator.
comm = MPI_COMM_WORLD

#  Get size and rank.
comm_size = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

# Since the leader only manages, there must be at least 2 processes
if comm_size <= 1:
    error('Cannot be run with only one process')

# Print rank.
print('my_rank: %d'%(my_rank))

# Wait momentarily.
pyMPI_Sleep(1.0)

# Set who is the leader
leader = 0
num_workers = comm_size - 1

# Create base message tags.
coefs_tag = 10000
input_tag = 20000
output_tag = 30000
end_tag = 999999

# Set data sizes.
N1 = 1024
N2 = 128

# Leader.
if (my_rank == leader):
    # Create coefficient data - simple impluse.
    coefs = np.zeros([N1,1],dtype=float)
    coefs[0] = 1.
    
    # Create input data.
    input = np.ones([N1,N2],dtype=float)
    
    # Create output data array.
    output = np.zeros([N1,N2],dtype=float)
    
    if UseGraphics:
        # Show output in a figure
        plt.imshow(output, origin = 'lower',  extent = [0, 10, 0, 10])
        plt.savefig('CData.png')
    
    print('Ready to broadcast coefficients')
    
    # Broadcast coefficients to everyone else.
    [t1] = MPI_Bcast( leader, coefs_tag, comm, coefs )
    
    # flag for being done with all processing
    done = 0

    # Instead of using for loops, use counters
    sendCounter = 1
    recvCounter = 1

    # Keep a vector of flags for whether each of the workers are busy ... 
    workers_busy = np.zeros([num_workers],dtype=int)
    # ... and whether each of the data items have been processed
    data_processed = np.zeros([N2],dtype=int)
       
    while not done:
        # Deal input data to everyone else (excluding self-leader).
        if sendCounter <= N2 :
            if np.count_nonzero(workers_busy) < num_workers:
                # Do not include leader in data dealing
                # Note that python index starts from zero (which is the leader)
                idle_workers = np.nonzero(workers_busy == 0)[0]
                dest = idle_workers[0]+1
                dest_tag = input_tag + sendCounter
                dest_data = input[:,sendCounter-1]
                   
                MPI_Send(dest,dest_tag,comm,dest_data)
                print('Sent data packet number %d to %d' %(sendCounter,dest))
                sendCounter = sendCounter + 1
                workers_busy[dest-1] = 1
           
        # Leader receives all the results.
        if np.count_nonzero(data_processed) < N2:
            message_ranks, message_tags = MPI_Probe('*', '*', comm)
            # if message_ranks is not empty then receive the message
            if len(message_ranks):
                # Receive output.
                print('Waiting on unit %d' %(recvCounter))
                   
                # Use this sort to try to service the received messages as close to actual order as possible
                m_tags_sorted_idx = np.argsort(message_tags)
                dest = message_ranks[m_tags_sorted_idx[0]]
                leader_tag = message_tags[m_tags_sorted_idx[0]]
                mesg_num = leader_tag - output_tag
                [t1] = MPI_Recv(dest,leader_tag,comm)
                # Reshape t1 to update a column vector
                # Note the python index is from 0 to N-1
                output[:,mesg_num-1] = np.reshape(t1,[1,N1])
                print('Received data packet number %d from %d' %(mesg_num,dest))
                recvCounter = recvCounter + 1
                if UseGraphics:
                    plt.imshow(output, origin = 'lower',  extent = [0, 10, 0, 10])
                    plt.savefig('CData_'+str(mesg_num)+'.png')
                data_processed[mesg_num-1] = 1
                workers_busy[dest-1] = 0
            else: 
                # messae_ranks is empty
                print('Waiting on data packet %d' %(recvCounter))
                # Add a pause
                pyMPI_Sleep(0.01)
        else:
            # recvCounter > N2
            done = 1

    # When all of the work has been done, send out a finish broadcast so that 
    # each of the worker processes exit properly
    [t1] = MPI_Bcast(leader, end_tag, comm, done)
       
    print('Sent ending broadcast')
       
else:
    # Everyone but the leader receives the coefs.
    # (my_rank ~= leader)
    # Receive coefs.
    coefs = 0
    [coefs] = MPI_Bcast( leader, coefs_tag, comm, coefs )
    print('Received coefficients')
       
    # Everyone but leader receives the input data and processes the results.
    done = 0
    while not done:
        message_ranks, message_tags = MPI_Probe('*', '*', comm)
        # if message_ranks is not empty then receive the message
        if len(message_ranks):
            # Receive input.
            # if there are multiple messages waiting, make sure that 
            # the end_tag is the last one read, since it will shut down
            # the worker process - source should be leader (0)
            source = message_ranks[0]
            in_tag = message_tags[0]
               
            if in_tag == end_tag:
                # All work is done, expected to receive the done signal via MPI_Bcast() wiht end_tag
                t1 = 0
                [done] = MPI_Bcast(leader, end_tag, comm, t1)
            else:
                mesg_num = in_tag - input_tag
                leader_tag = output_tag + mesg_num
                   
                # Receive input.
                [i_input] =  MPI_Recv(leader,in_tag,comm)
                print('Received data packet number %d from %d' %(mesg_num,source))
                   
                i_input = i_input + my_rank
                
                # Reshape i_input as a vector
                i_input = np.reshape(i_input,[N1,1])
                # Do computation.
                i_output = np.multiply(fft(coefs),i_input)

                # Send results back to the leader.
                MPI_Send(leader,leader_tag,comm,i_output)
                
                print('Processed unit %d' %(mesg_num))
        else: 
            # message_ranks is empty
            # If no message is waiting, microsleep to allow a message to be written
            pyMPI_Sleep(0.01)

print('SUCCESS')
# Finalize Matlab MPI.
MPI_Finalize()

"""
 Copyright 2003 Massachusetts Institute of Technology

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
