"""test_probemsg.py
    Basic Python MPI script that
    sends a matrix to another processor and also
    uses the MPI_Probe command.
 
    To run, start Python and type:
 
        MPI_Run('test_probemsg',2,{})
 
    Or, to run a different machine type:
 
        MPI_Run('test_probemsg',2,{'machine1' 'machine2'})
 
    Output will be piped into two files:
 
        PythonMPI/test_probemsg.0.out
        PythonMPI/test_probemsg.1.out
 
                                                        
    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratory
    {kepner,cbyun}@ll.mit.edu
"""

import pPython as GPC
from pyMPI_Sleep import *
from MPI_Send import *
from MPI_Recv import *
from ProbeMsg import *

print('--> Entering ProbeMsg Test')
#
#  Create communicator.
comm = GPC.comm

#  Get size and rank.
Np = GPC.Np
Pid = GPC.Pid

#  Print rank.
print('Pid: %d among %d processes'%(Pid,Np))

#  Set who is source and who is destination.
source = 1
dest = 0

#  Create a unique tag id for this message (very important in Python MPI!).
tag = 100045

#  Check to make sure that we have exactly two processors.
# Source.
if (Pid == source):
    # Create data.
    data = range(10)
    # Send it.
    MPI_Send( dest, tag, comm, data, data )

# Destination.
if (Pid == dest):
    # Check to see if we have any mesages.
    keep_waiting = 1
    while(keep_waiting):
        keep_waiting = keep_waiting + 1
        print('keep_waiting = %s'%(keep_waiting))
        message_rank,message_tag = ProbeMsg('*', '*' )

        pyMPI_Sleep(0.05)
        if (len(message_rank) > 0):
            for ii in range(len(message_rank)):
                incoming_rank = message_rank[ii]
                incoming_tag  = message_tag[ii]
            print('ProbeMsg detects rank(%d), tag(%d)'%(incoming_rank,incoming_tag))
            keep_waiting = 0

    # Receive data.
    [data,data1] = MPI_Recv( source, tag, comm )
    # Check data.
    print(data)

print('SUCCESS');
print('<-- Exiting ProbeMsg Test')

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

