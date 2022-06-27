import numpy as np

from MPI_Send import *
from MPI_Recv import *

import pPython as GPC
from Dmat import *
from Dmap import *
from size import *
from get_ind_range import *
from get_local_ind import *
from get_local_falls import *
from falls_intersection import *
from subsasgn_data import *

def subsasgn_3D(a,s,b):
    """
    SUBSASGN_3D Three dimensional subsasgn.
    
    S is of the following form [i:j, k:l, m:n]. Distributed object's dimension
    is 3. B is either a DMAT or a DOUBLE.
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """
    
    DEBUG = 1
    if DEBUG:
        print('--> Entering subsasgn_3D')

    # Instead of creating a copy of a, write directly to the memory
    # allocated for a in the caller's workspace
    # Not needed with Python: assignin('caller', inputname(1), [])
    
    if isinstance(b, (float, np.float64, np.ndarray)): 
        # RHS is a scalar (double) or an array
        if (s['subs'][0] == ':') and (s['subs'][1] == ':') and (s['subs'][2] == ':'):
            # A(:,:,:) = B
            if (size(b) == a.shape): 
                # dimensions are the same
                a.local[:,:,:] = b[a.global_ind['0'], a.global_ind['1'], a.global_ind['2']]
            else: 
                # dimensions do not match
                print('DMAT/subsasgn_2D:  Subscripted assignment dimension mismatch.')
                exit()
        else:
            # A(i:j, k:l, m:n) = B
            ind = get_ind_range(a,s)
            local_ind = get_local_ind(a.global_ind, ind)
    
            if len(size(b)) == len(size(a.local[local_ind['0'], local_ind['1'], local_ind['2']])):
                if size(b) == size(a.local[local_ind['0'], local_ind['1'], local_ind['2']]):
                    a.local[local_ind['0'], local_ind['1'], local_ind['2']] = b
            elif (len(size(b))==2) and (len(size(a.local[local_ind['0'], local_ind['1'], local_ind['2']]))==3):
                [s1,s2] = size(b)
                s3 = 1
                nds = [s1,s2,s3]
                if nds == size(a.local[local_ind['0'], local_ind['1'], local_ind['2']]):
                    a.local[local_ind['0'], local_ind['1'], local_ind['2']] = b

            elif (len(size(b))==3) and (len(size(a.local[local_ind['0'], local_ind['1'], local_ind['2']]))==2):
                [ds1,ds2] = size(a.local[local_ind['0'], local_ind['1'], local_ind['2']])
                ds3 = 1
                ds = [ds1,ds2,ds3]
                if size(b)==ds:
                    a.local[local_ind['0'], local_ind['1'], local_ind['2']] = b
        # A(i:j, k:l, m:n) = B
        
    elif isinstance(b, Dmat):
        # assignment from a distributed matrix
        # communication might be necessary
        if (s['subs'][0]==':') and (s['subs'][1]==':') and (s['subs'][2]==':'):
            # A(:,:,:) = B
            # check that dimensions match
            if a.shape != b.shape:
                print('DMAT/subsasgn_3D: Subscripted assignment dimension mismatch.')
                exit()
    
            # check if maps are the same
            if a.map==b.map:
                # maps are the same - no communication needed
                a.local[:,:,:] = b.local[:,:,:]

            else:
                # maps not the same - redistribution
                # compute falls intersections
                if (inmap(a.map, GPC.my_rank)) or (inmap(b.map, GPC.my_rank)):
                    # the local processor is either in a's or b's map
    
                    # if local processor belongs to b's map, get
                    # a's local falls and compute intersections
                    b_row_fi = dict()
                    b_col_fi = dict()
                    if inmap(b.map, GPC.my_rank): 
                        # belongs to b's map
                         for i in range(len(a.map.proc_list)):
                            a_falls = get_local_falls(a.pitfalls, a.map.grid, a.map.proc_list[i])
                            # falls intersection on b's procs
                            b_row_fi[i] = falls_intersection(b.falls[0], a_falls[0])
                            b_col_fi[i] = falls_intersection(b.falls[1], a_falls[1])
                            b_dim3_fi[i] = falls_intersection(b.falls[2], a_falls[2])
                        # belongs to b's map
    
                    # if local processor belongs to a's map, get
                    # b's local falls and compute falls
                    # intersections
                    a_row_fi = dict()
                    a_col_fi = dict()
                    if inmap(a.map, GPC.my_rank):
                        for i in range(len(b.map.proc_list)):
                            b_falls = get_local_falls(b.pitfalls, b.map.grid, b.map.proc_list[i])
                            # falls intersection on a's procs
                            a_row_fi[i] = falls_intersection(b_falls[0], a.falls[0])
                            a_col_fi[i] = falls_intersection(b_falls[1], a.falls[1])
                            a_dim3_fi[i] = falls_intersection(b_falls[2], a.falls[2])
                        # belongs to a's map
                    # the local processor is either in a's or b's map, otherwise should just fall through

                # determine which data to send and send the data
                for p1 in range(len(b.map.proc_list)): 
                    # iterate through b's processor list
                    for p2 in range(len(a.map.proc_list)):
                        # iterate through a's processor list
                        # increment tag
                        GPC.tag_num = GPC.tag_num+1
                        GPC.tag = 'tag-'+str(GPC.tag_num)
    
                        if (inmap(a.map, GPC.my_rank)) or (inmap(b.map, GPC.my_rank)):
                            # the local processor is either in a's or b's map
                            if b.map.proc_list[p1] != a.map.proc_list[p2]: # comm is needed
                                if GPC.my_rank==b.map.proc_list[p1]: # my rank is current B rank
                                    # redistribute data
                                    if b_row_fi[p2].size and a_col_fi[p2].size and b_dim3_fi[p2].size :
                                        # all intersections not empty
                                        # [data, scratch] = subsasgn_data(a, b, p2, b_row_fi, b_col_fi) 
                                        b_fi = dict()
                                        b_fi[0] = b_row_fi
                                        b_fi[1] = b_col_fi
                                        b_fi[2] = b_dim3_fi
                                        # **************************************
                                        [data, scratch] = subsasgn_data(a, b, p2, b_fi)
                                        # **************************************
                                        MPI_Send(a.map.proc_list[p2], GPC.tag, GPC.comm, data)
                                        # both intersections not empty
                                elif GPC.my_rank==a.map.proc_list[p2]: # my_rank is current A rank
                                    if a_row_fi[p1].size and a_col_fi[p1].size and a_dim3_fi[p1].size : 
                                        # all intersections not empty
                                        # [scratch, a_local_ind] = subsasgn_data(a, b, p1, a_row_fi, a_col_fi) 
                                        a_fi = dict()
                                        a_fi[0] = a_row_fi
                                        a_fi[1] = a_col_fi
                                        a_fi[2] = a_dim3_fi
                                        # **************************************
                                        [scratch, a_local_ind] = subsasgn_data(a, b, p1, a_fi) 
                                        # **************************************
                                        [data] = MPI_Recv(b.map.proc_list[p1], GPC.tag, GPC.comm)
                                        for r in range(len(data)):
                                            ind = a_local_ind[r]
                                            a.local[ind[0], ind[1], ind[2]] = data[r]
                                            # both intersections not empty
                                        # my_rank is current A rank
                            elif b.map.proc_list[p1] == a.map.proc_list[p2]: # no comm
                                if GPC.my_rank==a.map.proc_list[p2]:
                                    if b_row_fi[p2].size and b_col_fi[p2].size and b_dim3_fi[p2].size : 
                                        # all intersections not empty
                                        # [data, a_local_ind] = subsasgn_data(a, b, p2, b_row_fi, b_col_fi) 
                                        b_fi = dict()
                                        b_fi[0] = b_row_fi
                                        b_fi[1] = b_col_fi
                                        b_fi[2] = b_dim3_fi
                                        # **************************************
                                        [data, a_local_ind] = subsasgn_data(a, b, p2, b_fi)
                                        # **************************************
                                        for r in range(len(data)):
                                            ind = a_local_ind[r]
                                            a.local[ind[0], ind[1], ind[2]] = data[r]         
                                            # both intersections not empty
                                # no comm
                            # the local processor is either in a's or b's map, otherwise should just fall through
                        # iterate thorugh a's processor list
                    # iterate through b's processor list
                # maps not the same - redistribution
        else: 
            # A(i:j, k:l, m:n) = B
            # # # # # # # # # # # # # # # # # # # # # # # ADDED TO SUPPORT pMapper# # # # # # # # # # # # # # # # # # # # 
            if (s['subs'][0]==':') and (s['subs'][1]==':') and (len(s['subs'][2])==1):
                # A(:,:,i) = B
                print('Warning - dmat/subsasgn_3D: A(:,:,i) = B should be used with EXTREME caution.')
                print('Warning - dmat/subsasgn_3D: Need to check that for assignment A(:,:,i) = B, the size of the referenced part of A and size of B are the same.')
                # only support this case if this is a completely local
                # procedure, i.e. no communication is necessary
                # NOTE: B will be 2D, since this operation is assigning a 2D
                # slice
                if b.dim==2:
                    amap = a.map
                    bmap = b.map
                    # figure out the map slice local to the A(:,:,i)
                    ind = [1,1,s['2']['subs']] # indices to search for local proc
                    local_proc = get_local_proc(a.pitfalls, amap.grid, ind)
                    # find out the map grid indices for local_proc
                    grid_inds = n_dim_find(amap.grid, local_proc)
                    # add a singleton 1 if returns only 2 indices
                    if len(grid_inds)==2:
                        grid_inds[2] = 0

                    # extract the map/grid slice corresponding to the A's referenced
                    # indices
                    a_grid = amap.grid
                    a_grid_slice = a_grid[:,:,grid_inds[2]] # this should be a 2D grid
                    a_dist = amap.dist_spec
                    a_proc_list = np.transpose(a_grid_slice)
                    # create a 2D map for the grid slice
                    amap_slice = Dmap(size(a_grid_slice), a_dist[1:2], a_proc_list)
                    # NOTE: Might not even have to deal with map slices
                    # Algorithms for A(:,:,i) = B subsasgn
                    #    1. Subsref the relevant slice of A
                    #    2. Perform a 2D distributed susbasgn between slice of A
                    #     and B
                    #    3. Stuff the slice back into 3D A. At this point the
                    #     slice of A and the local part of 3D A should have the
                    #     same maps
                    subsA = subsref(a,s)
                    s2D = dict()
                    s2D['type'] = '()'
                    s2D['subs'] = {0:':',1:':'}                                   
                    subsA2 = subsasgn_2D(subsA, s2D, b)
                    if amap_slice == subsA2.map:
                        if inmap(amap_slice, GPC.my_rank):
                            # get local indices
                            ind = get_ind_range(a,s)
                            local_ind = get_local_ind(a.global_ind, ind)
    
                            # local assignment
                            if subsA2.local.size:
                                a.local[local_ind[0], local_ind[1], local_ind[2]] = subsA2.local[:,:]

                    else:
                        print('dmat/subsasgn3D: amap_slice and the map of the reference part of a should be the same.')
                        exit()
                else:
                    print('dmat/subsasgn3D: Only 2D slices can be assigned to 3D distributed arrays, i.e. b.dim MUST be 2.')
                    exit()
            else:
                print('DMAT/SUBSASGN3D: If A and B are both distributed, assignment must be of the form A(:,:,:) = B or A(:,:,i) = B.')
                exit()
            # # # # # # # # # # # # # # # # # # # # # # # ADDED TO SUPPORT pMapper# # # # # # # # # # # # # # # # # # # # 
        # A(i:j, k:l, m:n) = B        
    else: 
        # RHS is not a DMAT or a DOUBLE
        print('DMAT/subsasgn_3D: RHS must be a DOUBLE or DMAT.')
        exit()

    if DEBUG:
        print('<-- Exiting subsasgn_3D')

    return a

