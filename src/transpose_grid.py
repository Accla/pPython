import numpy as np

# GridPython class
from MPI_Send import *
from MPI_Recv import *

import GridPython as GPC
from GridMap import *
from GridDmat import *
from ndims import *
from size import *
from zeros import *
from ones import *
from local import *
from put_local import *
from global_block_ranges import *
from grid_complex import *

def transpose_grid(B):
    """
    TRANSPOSE_GRID Redistributes a dmat by transposing its process grid.
    A = TRANSPOSE_GRID(B) creates a dmat A that has the same contents as the
    dmat B, except that the process grid for A's map is the transpose of the process grid for
    B's map.  The contents of B are automatically redistributed to A.
    TRANSPOSE_GRID is only supported for 2D dmats.
    
    TRANSPOSE_GRID is optimized to redistribute row-distributed dmats into
    column-distributions and vice versa.  For example, suppose B's map had a
    grid specification of [1 4].  Then A's map will have a grid specification
    of [4 1].  Note that B must be block distributed in both dimensions with
    no overlap.
    
    For all other distributions, e.g. dmats with row and column
    distributions, overlap, etc., SUBSASGN will be used to redistribute B.

    """

    DEBUG = 1
    if DEBUG:
        print('--> Entering transpose_grid')
    comm = GPC.comm
    my_rank = GPC.my_rank
    
    # Check that B is 2D
    if (ndims(B) != 2):
        print('TRANSPOSE_GRID for %d-D array is not defined.'%(ndims(B)))
    
    if not hasattr(B,'local'):
        # If B is not a dmat, simply do a copy
        A = B
        if DEBUG:
            print('B is not a dmat object.')
            print('<-- Exiting transpose_grid')
        return A

    else:
        # If B is a dmat, perform the redistribution
        # Get B's size, map, grid, dist, overlap and cpus list.
        B_size      = size(B)
        B_map       = B.map
        B_grid      = B_map.grid
        B_grid_spec = B_map.grid_spec
        B_dist_spec = B_map.dist_spec
        B_proc_list = B_map.proc_list
        B_overlap   = B_map.overlap
 
    # Create map for A that is the same as B's but with a transposed grid.
    A_grid_spec = [B_grid_spec[1], B_grid_spec[0]]
    if not (B_overlap == None):
        mapA = GridMap(A_grid_spec, B_dist_spec, B_proc_list)
    else:
        mapA = GridMap(A_grid_spec, B_dist_spec, B_proc_list, B_overlap)


    if DEBUG:
        print('B_size:')
        print(B_size)
        print('B_dist_spec:')
        print(B_dist_spec)
        print('B_proc_list:')
        print(B_proc_list)
        print('A_grid_spec:')
        print(A_grid_spec)

    # Construct A (for memory allocation)
    if (np.iscomplex(local(B))).any():
        A = grid_complex(ones(B_size, mapA),ones(B_size, mapA))
        if DEBUG:
            print('Creae dmat object, A, as a complex numbers in its local array')
            if isinstance(A,GridDmat):
                print('A complex dmat, A, is recognized as GridDmat')
            else:
                print('A complex dmat, A, is NOT recognized as GridDmat')
    else:
        if DEBUG:
            print('Creae dmat object, A, as a real numbers in its local array')
        A = zeros(B_size, mapA) + 1.j
    
    # Pick off everthing but the special case.
    # not (grid has a 1 in either col or row
    #      dist is block
    #      no overlap )
    if ( not( (B_grid_spec[0] == 1 or B_grid_spec[1] == 1) \
            and (B_dist_spec['0']['dist'] == 'b') \
            and (B_dist_spec['1']['dist'] == 'b') \
            and (B_overlap == None) ) ):
        # Revert to default.
        A[:,:] = B
        if DEBUG:
            print('Pick off everything but the special case.')

    else:
        if DEBUG:
            print('Optimized row to column or column to row redistribution')
        # Optimized row to column or column to row redistribution
        A_local = local(A)
        B_local = local(B)
        if (np.iscomplex(A_local)).any():
            print('A_local is a complex array')
        else:
            print('A_local is NOT a complex array')
        if (np.iscomplex(B_local)).any():
            print('B_local is a complex array')
        else:
            print('B_local is NOT a complex array')

        # Compute send and receive order
        # Need to shuffle this for best perf.?????
        my_send_order = np.roll(B_proc_list, -(my_rank+1))
        my_recv_order = np.flipud(my_send_order)

        GPC.tag_num += 1
        GPC.tag = 'tag-'+str(GPC.tag_num)

        # Column to row redistribution
        if (B_grid_spec[0] == 1):
            # Get global ranges of dmats.
            A_i_ranges  = global_block_ranges(A,0)
            B_j_ranges  = global_block_ranges(B,1)

            # Send out data.
            for dest_rank in my_send_order:
                # Get indices. ( Add "+1" due to difference with the range, :, operator in Python)
                i1 = A_i_ranges[dest_rank, 1]
                i2 = A_i_ranges[dest_rank, 2] + 1
                j1 = B_j_ranges[my_rank, 1]
                j2 = B_j_ranges[my_rank, 2] + 1

                if (dest_rank == my_rank):
                    A_local[:,j1:j2] = B_local[i1:i2,:]
                else:
                    MPI_Send(dest_rank, GPC.tag, comm, B_local[i1:i2,:])

            # Receive data.
            for recv_rank in my_recv_order:
                if (recv_rank != my_rank):
                    j1 = B_j_ranges[recv_rank, 1]
                    j2 = B_j_ranges[recv_rank, 2] + 1
                    [temp] = MPI_Recv(recv_rank, GPC.tag, comm)
                    A_local[:,j1:j2] = temp
                    if DEBUG:
                        print('Pid = %d receives A_local from Pid = %d'%(my_rank,recv_rank))
                        if (np.iscomplex(temp)).any():
                            print('Received temp for A_local is a complex array')
                            print(temp)
                        else:
                            print('Received temp for A_local is NOT a complex array')
        else:
            # Row to column redistribution
            # Get global ranges of dmats.
            A_j_ranges  = global_block_ranges(A,1)
            B_i_ranges  = global_block_ranges(B,0)

            # Send out data.
            for dest_rank in my_send_order:
                # Get indices. ( Add "+1" due to difference with the range, :, operator in Python)
                j1 = A_j_ranges[dest_rank, 1]
                j2 = A_j_ranges[dest_rank, 2] + 1
                i1 = B_i_ranges[my_rank, 1]
                i2 = B_i_ranges[my_rank, 2] + 1
                if (dest_rank == my_rank):
                    A_local[i1:i2,:] = B_local[:,j1:j2]
                else:
                    MPI_Send(dest_rank,GPC.tag,comm,B_local[:,j1:j2])

            # Receive data.
            for recv_rank in my_recv_order:
                if (recv_rank != my_rank):
                    i1 = B_i_ranges[recv_rank, 1]
                    i2 = B_i_ranges[recv_rank, 2] + 1
                    [temp] = MPI_Recv(recv_rank, GPC.tag, comm)
                    A_local[i1:i2,:] = temp
                    if DEBUG:
                        print('Pid = %d receives temp for A_local from Pid = %d'%(my_rank,recv_rank))
                        if (np.iscomplex(temp)).any():
                            print('Received temp for A_local is a complex array')
                            print(temp)
                        else:
                            print('Received temp for A_local is NOT a complex array')

        # Put local data back.
        A = put_local(A, A_local)
              
    if DEBUG:
        print('<-- Exiting transpose_grid')
    return A

