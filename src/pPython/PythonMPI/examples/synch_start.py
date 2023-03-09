from time import time
from PythonMPI import *

"""synch_start.py

    This function tries to get all processes in a
    PythonMPI communicatior to wait and start at the same.
    Assumes clocks across the machines are synchronized
    to the level you want.

    PythonMPI
    Dr. Chansup Byun
    MatlabMPI
    Dr. Jeremy Kepner
    MIT Lincoln Laboratory
    kepner@ll.mit.edu
"""
def synch_start(comm,starter_rank,delay):
    # Get size and rank.
    comm_size = MPI_Comm_size(comm)
    my_rank = MPI_Comm_rank(comm)

    if(comm_size < 2):
        print('Too few processors (need at least 2) to synchronize')
        return

    # Create a unique tag id for the synch message.
    synch_tag = 99999

    if (my_rank == starter_rank):
        # Get a zero clock.
        zero_clock = time()

        # Get current time
        current_time = time() - zero_clock

        # Compute synchronized start time.
        start_time = current_time + delay

        # Broadcast to everyone else.
        [t1, t2] = MPI_Bcast( starter_rank, synch_tag, comm, zero_clock, start_time )

        # Get current time again.
        current_time = time() - zero_clock

        # Compute pause time.
        pause_time = start_time - current_time

        # Pause.
        pyMPI_Sleep(pause_time)

    else:

        # Receive time from starter.
        t1 = 0.
        [zero_clock,start_time] = MPI_Bcast( starter_rank, synch_tag, comm, t1, t1 )

        # Get current time again.
        current_time = time() - zero_clock

        # Compute pause time.
        pause_time = start_time - current_time

        # Pause.
        pyMPI_Sleep(pause_time)

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
