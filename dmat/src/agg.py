from MPI_Recv import *
from MPI_Send import *

import GridPython as GPC
from GridDmat import *

from inmap import *
from reconstruct import *


def agg(d, leader=None):
    """Aggregates the parts of a distributed matrix on the leader processor.
    
     AGG(D) aggregates the parts of a distributed matrix into a whole and 
     returns it as a regular matrix.
     If the current processor is the LEADER, returns the aggreagated matrix, 
     otherwise, returns the local part.
     
     This functions increments GLOBAL message TAG.
    
     NOTE: Currently, it doesn't matter whether or not the leader is in the
     map - the global matrix is returned on the leader regardless. 
 
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering agg')

    if not isinstance(d,GridDmat):
        return d

    # Set the leader for aggregation
    if hasattr(GPC, 'leader'):
        # GPC has attribute, leader, defined.
        map_leader = GPC.leader
    if leader:
        map_leader = leader
    
    # increment tag
    if hasattr(GPC, 'leader'):
        GPC.tag_num += 1
    else:
        GPC.tag_num = 0
    GPC.tag = 'tag-'+str(GPC.tag_num)
    
    if GPC.my_rank == map_leader:
        if d.dim==2:
            dim = d.map.grid.shape
            # dim(1) - number of grid rows, dim(2) - number of grid cols
            temp_mat = dict()
            for i in range(dim[0]):
                temp_mat[str(i)] = dict()
                for j in range(dim[1]):
                    if (GPC.my_rank==d.map.grid[i][j]):
                        temp_mat[str(i)][str(j)] = d.local
                        if DEBUG:
                            print('Local array, d.local:')
                            print('type(d.local): %s'%(type(d.local)))
                            print('type(d.local[0,0]): %s'%(type(d.local[0,0])))

                    else:
                        [temp] = MPI_Recv(d.map.grid[i][j], GPC.tag, GPC.comm)
                        temp_mat[str(i)][str(j)] = temp
                        if DEBUG:
                            print('Leader received msg for (i,j) = (%d,%d) from Pid, %d, with the tag, %s.'%(i,j,d.map.grid[i][j],GPC.tag))
                            print('Received array, temp:')
                            print('type(temp): %s'%(type(temp)))
                            print('type(temp[0,0]): %s'%(type(temp[0,0])))
        else:
            print('ERROR(agg): map dimension, %d, is not yet supported.'%(d.dim))
            
        if DEBUG:
            print('Leader: type of the received temp_mat is %s.'%(type(temp_mat)))
            print('The lengtth ofthe received temp_mat is %d.'%(len(temp_mat)))
            print(temp_mat)

        # reconstruct the matrix from the local pieces
        # this is a NO-OP for block distributions since the data does not
        mat = reconstruct(d.pitfalls,  d.map.grid, temp_mat, d.size)

    else: # my_rank != leader
        # send local data to the leader regardless of the matrix dimension
        if inmap(d.map, GPC.my_rank): # only send data if processor is in the map
            MPI_Send(map_leader, GPC.tag, GPC.comm, d.local)
            if DEBUG:
                print('Sent msg to %d with tag, %s'%(map_leader,GPC.tag))
                print('Sent array, d.local:')
                print('type(d.local): %s'%(type(d.local)))
                print('type(d.local[0,0]): %s'%(type(d.local[0,0])))
        mat = d.local

    if DEBUG:
        print('--> Exiting agg')
    return mat

