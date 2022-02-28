"""basic_app4.py 

    Basic example of a typical application for which 
    PythonMPI might be used.  It uses a leader that manages, 
    and workers that conduct the processing. This example 
    takes a matrix, breaks it up among processors, does a 
    computation, and gathers the results to display in a 
    figure window. 

    This example is different from basic_app, basic_app2,
    and basic_app3 in that the leader uses the MPI_Probe
    function to determine whether a worker process has
    sent a completed computation packet. The leader sends
    a packet to be processed and then probes for a packet
    that was sent to itself. If a packet has
    been sent back, the leader processes the packet; if no
    packet has been sent, then the leader proceeds to
    sending another packet to be processed. If no other
    packets to be processed need to be sent, then it loops
    waiting to receive a processed packet.

    This example can also plot the data on a graph figure. 
    To enable this feature, set the variable UseGraphics 
    equal to 1. 

    To run, start Matlab and type:

        MPI_Run('basic_app4',4,{})

    Or, to run a different machine type:

        MPI_Run('basic_app4',4,{'machine1' 'machine2' 'machine3' 'machine4'})

    Output will be piped into 4 files:

        MatMPI/basic_app4.0.out
        MatMPI/basic_app4.1.out
        MatMPI/basic_app4.2.out
        MatMPI/basic_app4.3.out

    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Albert Reuther
    MIT Lincoln Laboratory
    {reuther,cbyun}@ll.mit.edu
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

# Create base message tags.
coefs_tag = 10000;
input_tag = 20000;
output_tag = 30000;

# Set data sizes.
N1 = 1024;
N2 = 128;

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
    
    print('Ready to broadcast coefficients');
    
    # Broadcast coefficients to everyone else.
    [t1] = MPI_Bcast( leader, coefs_tag, comm, coefs );
    
    # flag for being done with all processing
    done = 0;

    # Instead of using for loops, use counters
    sendCounter = 1
    recvCounter = 1

    while not done:
        # Deal input data to everyone else (excluding self-leader).
        if sendCounter <= N2:
            # Do not include leader in data dealing
            dest = (sendCounter - 1)%(comm_size-1) + 1
            dest_tag = input_tag + sendCounter
            # Note the python index is from 0 to N-1
            dest_data = input[:,sendCounter-1]

            MPI_Send(dest,dest_tag,comm,dest_data)
            print('Sent data packet number %d with tag, %d' %(sendCounter,dest_tag))
            sendCounter = sendCounter + 1

        # Leader receives all the results.
        if recvCounter <= N2:
            # Compute who sent this message.
            # Do not include leader in data dealing
            dest = (recvCounter - 1)%(comm_size-1) + 1
            leader_tag = output_tag + recvCounter

            message_ranks,message_tags = MPI_Probe(dest, leader_tag, comm)

            # if message_ranks is not empty then receive the message
            if len(message_ranks):
                # Receive output.
                print('Waiting on unit %d' %(recvCounter))
                [t1] = MPI_Recv(dest,leader_tag,comm)
                # Reshape t1 to update a column vector
                # Note the python index is from 0 to N-1
                output[:,recvCounter-1] = np.reshape(t1,[1,N1])
                print('Received data packet number %d' %(recvCounter))

                if UseGraphics:
                    plt.imshow(output, origin = 'lower',  extent = [0, 10, 0, 10])
                    plt.savefig('CData_'+str(recvCounter)+'.png')
                recvCounter = recvCounter + 1
            else:  
                print('Waiting on data packet %d' %(recvCounter))
                pyMPI_Sleep(2.2)
        else:
            done = 1

else:
    # Everyone but the leader receives the coefs.
    # Receive coefs.
    coefs = 0
    [coefs] = MPI_Bcast( leader, coefs_tag, comm, coefs )
    print('Read in coefficients');

    # Everyone but leader receives the input data and processes the results.
    for i in range(N2):
        # Compute who the destination is for this message.
        # Do not include leader in data dealing
        dest = i%(comm_size-1)+1
        
        # Check if this destination is me.
        if (my_rank == dest):
            # Compute tags (i+1) corresponds to sendCounter.
            # Note the python index is from 0 to N-1
            dest_tag = input_tag + (i+1)
            leader_tag = output_tag + (i+1)
            
            print('Waiting on data packet %d with tag, %d' %(i,dest_tag))
            #  Receive input.
            [i_input] =  MPI_Recv(leader,dest_tag,comm);
            
            i_input = i_input + my_rank;
            
            # Reshape i_input as a vector
            i_input = np.reshape(i_input,[N1,1])
            # Do computation.
            i_output = np.multiply(fft(coefs),i_input)
            
            # Send results back to the leader.
            MPI_Send(leader,leader_tag,comm,i_output);
            
            print('Processed unit %d' %(i))
            pyMPI_Sleep(0.2)

print('SUCCESS');
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
