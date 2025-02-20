"""probe.py
    Basic Python MPI script that
    sends a matrix to another processor and also
    uses the MPI_Probe command.
 
    To run, start Python and type:
 
        MPI_Run('probe',2,{})
 
    Or, to run a different machine type:
 
        MPI_Run('probe',2,{'machine1' 'machine2'})
 
    Output will be piped into two files:
 
        PythonMPI/probe.0.out
        PythonMPI/probe.1.out
 
                                                        
    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratory
    {kepner,cbyun}@ll.mit.edu
"""
import pyMPI_COMM_WORLD as pyMCW
from pyMPI_Save_messages import *
from pyMPI_Sleep import *
from MPI_Init import *
from MPI_Comm_size import *
from MPI_Comm_rank import *
from MPI_Send import *
from MPI_Recv import *
from MPI_Probe import *

print('--> Entering probe')
#
# Export Python MPI_COMM_WORLD (defined in PythonMPI.py)
MPI_COMM_WORLD = pyMCW.MPI_COMM_WORLD

# Initialize MPI 
MPI_Init()

#  Create communicator.
comm = MPI_COMM_WORLD

#  Modify common directory from default for better performance.
# comm = pyMPI_Comm_dir(comm,'/tmp');

#  Uncomment if you want to save the messages that were sent.
#  comm = pyMPI_Save_messages(comm,1);

#  Get size and rank.
comm_size = MPI_Comm_size(comm)
my_rank = MPI_Comm_rank(comm)

#  Print rank.
print('my_rank: %d'%(my_rank))

#  Set who is source and who is destination.
source = 1
dest = 0

#  Check to make sure that we have exactly two processors.
if(comm_size == 2):
    # Source.
    if (my_rank == source):
        # Create data.
        data1 = range(10)
        #  Create a unique tag id for this message (very important in Python MPI!).
        tag = 100045
        MPI_Send( dest, tag, comm, data1, data1 )
        data2 = np.random.rand(3,3)
        tag = 100046
        MPI_Send( dest, tag, comm, data2)

    # Destination.
    if (my_rank == dest):
        # Check to see if we have any mesages.
        keep_waiting = 1
        while(keep_waiting):
            message_rank,message_tag = MPI_Probe('*', '*', comm)
            print('keep_waiting = %s'%(keep_waiting))
            keep_waiting = keep_waiting + 1
            pyMPI_Sleep(1)
            if (len(message_rank) > 0):
                for ii in range(len(message_rank)):
                    incoming_rank = message_rank[ii]
                    incoming_tag  = message_tag[ii]
                    print('MPI_Probe detects rank(%d), tag(%d)'%(incoming_rank,incoming_tag))
                    # Receive data.
                    [*argv] = MPI_Recv(incoming_rank, incoming_tag, comm )
                    # Check data.
                    print('--> Received message with MPI_Probe: from Pid = %d with a tag, %s'%(incoming_rank,incoming_tag))
                    for arg in argv:
                        print(arg)
                keep_waiting = 0

print(' ')
print(' ')
print('SUCCESS');
print(' ')
print(' ')

print('<-- Exiting probe')
# Finalize Python MPI.
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


