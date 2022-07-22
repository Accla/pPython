from MPI_Comm_rank import *
from MPI_Probe import *
from MPI_Recv import *
from MPI_Send import *

from pyMPI_Sleep import *

def agg_msg(z,my_z,d_index,leader,tag,comm):
    """Aggregate distributed data by the leader process.
    
    Usage:
    z = agg_msg(z,my_z,d_index,leader,tag,comm)
    
    """
    
    # Update my own results:
    my_rank = MPI_Comm_rank(comm)
    my_i_global = range(d_index[my_rank]['beg'],d_index[my_rank]['end']+1)
    z[my_i_global,:] = my_z

    if my_rank == leader:
        # while loop for proving incomming messages
        # flag for being done with all processing
        max_count = len(d_index.items())-1
        done = 0;

        # Instead of using for loops, use counters
        recv_count = 1

        while not done:
            # Leader receives all the results.
            if recv_count <= max_count:
                # Check for incoming messages
                msg_ranks,msg_tags = MPI_Probe('*', tag, comm)

                # if msg_ranks is not empty then receive the 1st message
                if len(msg_ranks):
                    # Receive output.
                    src = msg_ranks[0]
                    print('Waiting on Pid %d' %(src))
                    [t1] = MPI_Recv(src,tag,comm)
                    # Reshape t1 to update a column vector
                    # Note the python index is from 0 to N-1
                    my_i_global = range(d_index[src]['beg'],d_index[src]['end']+1)
                    z[my_i_global,:] = t1
                    print('Received data packet number %d' %(recv_count))
                    recv_count = recv_count + 1
                else:
                    print('Waiting on data packet %d' %(recv_count))
                    pyMPI_Sleep(2.0)
            else:
                done = 1
    else:
        # Send the results back to the leader process
        MPI_Send(leader,tag,comm,my_z)

    return z
