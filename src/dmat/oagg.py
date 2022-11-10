from MPI_Recv import *
from MPI_Send import *

import pPython as GPC
from Dmat import *

from inmap import *
from reconstruct import *


def oagg(d, leader=None):
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

    if not isinstance(d,Dmat):
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
    
    if GPC.Pid == map_leader:
        if d.dim==2:
            if DEBUG:
                print('DMAT is 2-D')
            dim = d.map.grid.shape
            # dim[0] - number of grid rows, dim[1] - number of grid cols
            temp_mat = dict()
            for i in range(dim[0]):
                temp_mat[i] = dict()
                for j in range(dim[1]):
                    if (GPC.Pid==d.map.grid[i][j]):
                        temp_mat[i][j] = d.local
                        if DEBUG>2:
                            print('Local array, d.local:')
                            print('type(d.local): %s'%(type(d.local)))
                            print('type(d.local[0,0]): %s'%(type(d.local[0,0])))
                    else:
                        [temp] = MPI_Recv(d.map.grid[i][j], GPC.tag, GPC.comm)
                        temp_mat[i][j] = temp
                        if DEBUG>2:
                            print('Leader received msg for (i,j) = (%d,%d) from Pid, %d, with the tag, %s.'%(i,j,d.map.grid[i][j],GPC.tag))
                            print('Received array, temp:')
                            print('type(temp): %s'%(type(temp)))
                            print('type(temp[0,0]): %s'%(type(temp[0,0])))
        elif d.dim==3:
            if DEBUG:
                print('DMAT is 3-D')
            dim = d.map.grid.shape
            # dim[0] - number of grid rows, dim[1] - number of grid cols
            # dim[2] - number of grid 3rd dimension
            temp_mat = dict()
            for i in range(dim[0]):
                temp_mat[i] = dict()
                for j in range(dim[1]):
                    temp_mat[i][j] = dict()
                    for k in range(dim[2]):
                        if (GPC.Pid==d.map.grid[i][j][k]):
                            temp_mat[i][j][k] = d.local
                            if DEBUG>2:
                                print('Local array, d.local:')
                                print('type(d.local): %s'%(type(d.local)))
                                print('type(d.local[0,0,0]): %s'%(type(d.local[0,0,0])))
                        else:
                            [temp] = MPI_Recv(d.map.grid[i][j][k], GPC.tag, GPC.comm)
                            temp_mat[i][j][k] = temp
                            if DEBUG>2:
                                print('Leader received msg for (i,j,k) = (%d,%d,%d) from Pid, %d, with the tag, %s.'%(i,j,k,d.map.grid[i][j][k],GPC.tag))
                                print('Received array, temp:')
                                print('type(temp): %s'%(type(temp)))
                                print('type(temp[0,0,0]): %s'%(type(temp[0,0,0])))
        elif d.dim==4:
            if DEBUG:
                print('DMAT is 4-D')
            dim = d.map.grid.shape
            # dim[0] - number of grid rows, dim[1] - number of grid cols
            # dim[2] - number of grid 3rd dimension
            temp_mat = dict()
            for i in range(dim[0]):
                temp_mat[i] = dict()
                for j in range(dim[1]):
                    temp_mat[i][j] = dict()
                    for k in range(dim[2]):
                        temp_mat[i][j][k] = dict()
                        for m in range(dim[3]):
                            if (GPC.Pid==d.map.grid[i][j][k][m]):
                                temp_mat[i][j][k][m] = d.local
                                if DEBUG>2:
                                    print('Local array, d.local:')
                                    print('type(d.local): %s'%(type(d.local)))
                                    print('type(d.local[0,0,0,0]): %s'%(type(d.local[0,0,0,0])))
                            else:
                                [temp] = MPI_Recv(d.map.grid[i][j][k][m], GPC.tag, GPC.comm)
                                temp_mat[i][j][k][m] = temp
                                if DEBUG>2:
                                    print('Leader received msg for (i,j,k,m) = (%d,%d,%d,%d) from Pid, %d, with the tag, %s.'%(i,j,k,m,d.map.grid[i][j][k][m],GPC.tag))
                                    print('Received array, temp:')
                                    print('type(temp): %s'%(type(temp)))
                                    print('type(temp[0,0,0]): %s'%(type(temp[0,0,0,0])))
        else:
            raise Exception('Error (oagg): DMAT/AGG: Only up to 4-D objects currently supported')

        if DEBUG>2:
            print('Leader: type of the received temp_mat is %s.'%(type(temp_mat)))
            print('The lengtth ofthe received temp_mat is %d.'%(len(temp_mat)))
            print(temp_mat)

        # reconstruct the matrix from the local pieces
        # this is a NO-OP for block distributions since the data does not
        mat = reconstruct(d.pitfalls,  d.map.grid, temp_mat, d.shape)

    else: # my_rank != leader
        if DEBUG:
            if d.dim==2:
                print('DMAT is 2-D')
            elif d.dim==3:
                print('DMAT is 3-D')
        # send local data to the leader regardless of the matrix dimension
        if inmap(d.map, GPC.Pid): # only send data if processor is in the map
            MPI_Send(map_leader, GPC.tag, GPC.comm, d.local)
            if DEBUG>2:
                print('Sent msg to %d with tag, %s'%(map_leader,GPC.tag))
                print('Sent array, d.local:')
                print('type(d.local): %s'%(type(d.local)))
                print('type(d.local[0,0]): %s'%(type(d.local[0,0])))
        mat = d.local

    if DEBUG:
        print('d.local.shape')
        print(d.local.shape)
        print('mat.shape')
        print(mat.shape)
        print('--> Exiting agg')
    return mat

