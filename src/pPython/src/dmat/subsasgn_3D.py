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
from inmap import *
from get_local_proc import *

def subsasgn_3D(a,s,b):
    """
    SUBSASGN_3D Three dimensional subsasgn.
    
    S is of the following form [i:j, k:l, m:n]. Distributed object's dimension
    is 3. B is either a DMAT or a DOUBLE.
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering subsasgn_3D')

    # Instead of creating a copy of a, write directly to the memory
    # allocated for a in the caller's workspace
    # Not needed with Python: assignin('caller', inputname(1), [])
    
    if isinstance(b, (int,float,np.float64,np.float32,np.ndarray)): 
        # RHS is a scalar (double) or an array
        if (s['subs'][0] == ':') and (s['subs'][1] == ':') and (s['subs'][2] == ':'):
            # A(:,:,:) = B
            if (size(b) == a.shape): 
                # dimensions are the same
                # Assuming global_ind is a tuple object of a range object or more
                # Only works if there is no missing indices when multiple range objects are in the tuple
                robj1 = []
                for i in range(len(a.global_ind[0])):
                    robj1 += list(a.global_ind[0][i])
                robj2 = []
                for i in range(len(a.global_ind[1])):
                    robj2 += list(a.global_ind[1][i])
                robj3 = []
                for i in range(len(a.global_ind[2])):
                    robj3 += list(a.global_ind[2][i])
                a.local[:,:,:] = b[robj1[0]:robj1[-1]+1,robj2[0]:robj2[-1]+1,robj3[0]:robj3[-1]+1]
            elif (size(b)==[1,1,1]):
                # b is a scalar
                a.local[:,:,:] = b
            else: 
                # dimensions do not match
                raise Exception('DMAT/subsasgn_3D:  Subscripted assignment dimension mismatch.')
        else:
            # A(i:j, k:l, m:n) = B
            ind = get_ind_range(a,s)
            local_ind = get_local_ind(a.global_ind, ind)
            # Key for local_ind is numberic key
            # subslicing array is done differently between MATLAB and Python.
            s0 = None; s1 = None; s2 = None
            if len(local_ind[0]):
                s0 = slice(local_ind[0][0],local_ind[0][-1]+1,None)
            if len(local_ind[1]):
                s1 = slice(local_ind[1][0],local_ind[1][-1]+1,None)
            if len(local_ind[2]):
                s2 = slice(local_ind[2][0],local_ind[2][-1]+1,None)
    
            if len(size(b)) == len(size(a.local[local_ind[0]][:, local_ind[1]][:, local_ind[2]])):
                if size(b) == size(a.local[local_ind[0]][:, local_ind[1]][:, local_ind[2]]):
                    a.local[s0, s1, s2] = b
            elif (len(size(b))==2) and (len(size(a.local[local_ind[0]][:, local_ind[1]][:, local_ind[2]]))==3):
                [t0,t1] = size(b)
                t2 = 1
                nds = [t0,t1,t2]
                if nds == size(a.local[local_ind[0]][:, local_ind[1]][:, local_ind[2]]):
                    a.local[s0, s1, s2] = b
            elif (len(size(b))==3) and (len(size(a.local[local_ind[0]][:, local_ind[1]][:, local_ind[2]]))==2):
                [ds1,ds2] = size(a.local[local_ind[0]][:, local_ind[1]][:, local_ind[2]])
                ds3 = 1
                ds = [ds1,ds2,ds3]
                if size(b)==ds:
                    a.local[s0, s1, s2] = b
        # A(i:j, k:l, m:n) = B
        
    # The following caused undefined Dmat error because its circular reference.
    # elif isinstance(b, Dmat):
    # elif hasattr(b, 'Dmat'):
    # elif hasattr(b, 'Dmap'):
    # elif isinstance(b, Dmat.Dmat):
    else:
        # RHS is a DMAT, assignment from a distributed matrix
        # communication might be necessary
        if isinstance(s['subs'][0],str) and isinstance(s['subs'][1],str) and isinstance(s['subs'][2],str):
            # A(:,:,:) = B
            # check that dimensions match
            if a.shape != b.shape:
                raise Exception('DMAT/subsasgn_3D: Subscripted assignment dimension mismatch.')
    
            # check if maps are the same
            if a.map==b.map:
                # maps are the same - no communication needed
                a.local[:,:,:] = b.local[:,:,:]

            else:
                if DEBUG:
                    print('  --> A(:,:,:) = B where A & B have different distribution maps')
                # maps not the same - redistribution
                # compute falls intersections
                if (inmap(a.map, GPC.Pid)) or (inmap(b.map, GPC.Pid)):
                    # the local processor is either in a's or b's map
    
                    # if local processor belongs to b's map, get
                    # a's local falls and compute intersections
                    b_row_fi = dict()
                    b_col_fi = dict()
                    b_dim3_fi = dict()
                    if inmap(b.map, GPC.Pid): 
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
                    a_dim3_fi = dict()
                    if inmap(a.map, GPC.Pid):
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
    
                        if (inmap(a.map, GPC.Pid)) or (inmap(b.map, GPC.Pid)):
                            # the local processor is either in a's or b's map
                            if b.map.proc_list[p1] != a.map.proc_list[p2]: # comm is needed
                                if GPC.Pid==b.map.proc_list[p1]: # my rank is current B rank
                                    # redistribute data
                                    if len(b_row_fi[p2])>0 and len(b_col_fi[p2])>0 and len(b_dim3_fi[p2])>0 :
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
                                elif GPC.Pid==a.map.proc_list[p2]: # my_rank is current A rank
                                    if len(a_row_fi[p1])>0 and len(a_col_fi[p1])>0 and len(a_dim3_fi[p1])>0 :
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
                                            # Different behavior compared to Matlab: a.local[ind[0], ind[1]] = data[r]
                                            a.local[slice(ind[0][0],ind[0][-1]+1),slice(ind[1][0],ind[1][-1]+1),slice(ind[2][0],ind[2][-1]+1)] = data[r]
                                            # both intersections not empty
                                        # my_rank is current A rank
                            elif b.map.proc_list[p1] == a.map.proc_list[p2]: # no comm
                                if GPC.Pid==a.map.proc_list[p2]:
                                    if len(b_row_fi[p2])>0 and len(b_col_fi[p2])>0 and len(b_dim3_fi[p2])>0 :
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
                                            # Different behavior compared to Matlab: a.local[ind[0], ind[1], ind[2]] = data[r]
                                            a.local[slice(ind[0][0],ind[0][-1]+1),slice(ind[1][0],ind[1][-1]+1),slice(ind[2][0],ind[2][-1]+1)] = data[r]
                                            # both intersections not empty
                                # no comm
                            # the local processor is either in a's or b's map, otherwise should just fall through
                        # iterate thorugh a's processor list
                    # iterate through b's processor list
                # maps not the same - redistribution
        else: 
            # A(i:j, k:l, m:n) = B
            # # # # # # # # # # # # # # # # # # # # # # # ADDED TO SUPPORT pMapper# # # # # # # # # # # # # # # # # # # # 
            # if (s['subs'][0]==':') and (s['subs'][1]==':') and (len(s['subs'][2])==1):
            if isinstance(s['subs'][0],slice) and isinstance(s['subs'][1],slice) and isinstance(s['subs'][2],int):
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
                    if DEBUG:
                        print("s['subs']")
                        print(s['subs'])
                    ind = [0,0,s['subs'][2]] # indices to search for local proc
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
                    amap_slice = Dmap(size(a_grid_slice), a_dist[0:2], a_proc_list)
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
                        if inmap(amap_slice, GPC.Pid):
                            # get local indices
                            ind = get_ind_range(a,s)
                            local_ind = get_local_ind(a.global_ind, ind)
    
                            # local assignment
                            if subsA2.local.size:
                                # Different behavior compared to Matlab: a.local[ind[0], ind[1], ind[2]] = data[r]
                                a.local[slice(local_ind[0][0],local_ind[0][-1]+1),slice(local_ind[1][0],local_ind[1][-1]+1),slice(local_ind[2][0],local_ind[2][-1]+1)] = subsA2.local[:,:]
                    else:
                        raise Exception('dmat/subsasgn3D: amap_slice and the map of the reference part of a should be the same.')
                else:
                    raise Exception('dmat/subsasgn3D: Only 2D slices can be assigned to 3D distributed arrays, i.e. b.dim MUST be 2.')
            else:
                raise Exception('DMAT/SUBSASGN3D: If A and B are both distributed, assignment must be of the form A(:,:,:) = B or A(:,:,i) = B.')
            # # # # # # # # # # # # # # # # # # # # # # # ADDED TO SUPPORT pMapper# # # # # # # # # # # # # # # # # # # # 
        # A(i:j, k:l, m:n) = B        
    # How to raise exception when RHS is not a DMAT nor a DOUBLE?
    # else: 
    # How to raise exception when RHS is not a DMAT nor a DOUBLE?
    # # RHS is not a DMAT or a DOUBLE
    #    raise Exception('DMAT/subsasgn_3D: RHS must be a DOUBLE or DMAT.')

    if DEBUG:
        print('<-- Exiting subsasgn_3D')

    return a

########################################################
# pMatlab: Parallel Matlab Toolbox
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2005, Massachusetts Institute of Technology All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#      * Neither the name of the Massachusetts Institute of Technology nor
#        the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written
#        permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

