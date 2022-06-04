import numpy as np

from MPI_Send import *
from MPI_Recv import *

import GridPython as GPC
from GridDmat import *
from size import *
from get_ind_range import *
from get_local_ind import *
from get_local_falls import *
from falls_intersection import *
from subsasgn_data import *
from inmap import *

def subsasgn_2D(a,s,b):
    """
    SUBSASGN_2D Two dimensional subsasgn.
    
    S is of the following form [i:j, k:l]. Distributed object's dimension
    is 2. B is either a DMAT or a DOUBLE.
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """
    
    DEBUG = 1
    if DEBUG:
        print('--> Entering subsasgn_2D')
        print(b)

    # Instead of creating a copy of a, write directly to the memory
    # allocated for a in the caller's workspace
    # Not needed with Python: assignin('caller', inputname(1), [])
    
    if isinstance(b, (float, np.float64, np.ndarray)): 
        # RHS is a scalar (double) or an array
        if isinstance(s['subs'][0],str) and isinsttance(s['subs'][1],str):
            if (s['subs'][0] == ':') and (s['subs'][1] == ':'):
                # A[:,:] = B
                if (size(b) == a.shape): 
                    # dimensions are the same
                    a.local[:,:] = b[a.global_ind['0'], a.global_ind['1']]
                elif (size(b)==[1,1]):   
                    # b is a scalar
                    a.local[:,:] = b
                else: 
                    # dimensions do not match
                    print('DMAT/subsasgn_2D:  Subscripted assignment dimension mismatch.')
                    exit()
        else: 
            # A[i:j, k:l] = B
            indr = get_ind_range(a,s)
            local_ind = get_local_ind(a.global_ind, indr)
            # Key for local_ind is numberic key
            # subslicing array is done differently between MATLAB and Python.
            if size(b) == size(a.local[local_ind[0], local_ind[1]]):
                a.local[local_ind[0], local_ind[1]] = b
        # A(i:j, k:l) = B
        
    # The following caused undefined GridDmat error because its circular reference.
    # elif isinstance(b, GridDmat):
    # elif hasattr(b, 'GridDmat'):
    # elif hasattr(b, 'GridMap'):
    # elif isinstance(b, GridDmat.GridDmat):
    else:
        # RHS is a DMAT, assignment from a distributed matrix
        # communication might be necessary
        if isinstance(s['subs'][0],str) and isinstance(s['subs'][1],str): 
            # A(:,:) = B
            # check that dimensions match
            if a.shape != b.shape:
                print('DMAT/subsasgn_2D: Subscripted assignment dimension mismatch.')
                exit()
    
            # check if maps are the same
            if a.map==b.map:
                # maps are the same - no communication needed
                a.local[:,:] = b.local[:,:]
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
                                    if len(b_row_fi[p2])>0 and len(b_col_fi[p2])>0:
                                        # both intersections not empty
                                        # [data, scratch] = subsasgn_data(a, b, p2, b_row_fi, b_col_fi) 
                                        b_fi = dict()
                                        b_fi[0] = b_row_fi
                                        b_fi[1] = b_col_fi
                                        [data, scratch] = subsasgn_data(a, b, p2, b_fi)
                                        if DEBUG:
                                            print('Send data to Pid=%d'%(a.map.proc_list[p2]))
                                            print(data)
                                        MPI_Send(a.map.proc_list[p2], GPC.tag, GPC.comm, data)
                                        # both intersections not empty
                                elif GPC.my_rank==a.map.proc_list[p2]: # my_rank is current A rank
                                    if len(a_row_fi[p1])>0 and len(a_col_fi[p1])>0:
                                        # both intersections not empty
                                        # [scratch, a_local_ind] = subsasgn_data(a, b, p1, a_row_fi, a_col_fi) 
                                        a_fi = dict()
                                        a_fi[0] = a_row_fi
                                        a_fi[1] = a_col_fi
                                        [scratch, a_local_ind] = subsasgn_data(a, b, p1, a_fi) 
                                        if DEBUG:
                                            print('Receive data from Pid=%d with index, a_local_ind'%(b.map.proc_list[p1]))
                                            print(a_local_ind)
                                        # Python workaround for zero lengh index in subsasgn_data() issue, which is fine in Matlab
                                        [data] = MPI_Recv(b.map.proc_list[p1], GPC.tag, GPC.comm)
                                        for r in range(len(data)):
                                            ind = a_local_ind[r]
                                            # Different behavior compared to Matlab: a.local[ind[0], ind[1]] = data[r]
                                            a.local[slice(ind[0][0],ind[0][-1]+1),slice(ind[1][0],ind[1][-1]+1)] = data[str(r)]
                            elif b.map.proc_list[p1] == a.map.proc_list[p2]: # no comm
                                if GPC.my_rank==a.map.proc_list[p2]:
                                    if len(b_row_fi[p2])>0 and len(b_col_fi[p2])>0:
                                        # both intersections not empty
                                        # [data, a_local_ind] = subsasgn_data(a, b, p2, b_row_fi, b_col_fi) 
                                        b_fi = dict()
                                        b_fi[0] = b_row_fi
                                        b_fi[1] = b_col_fi
                                        [data, a_local_ind] = subsasgn_data(a, b, p2, b_fi)
                                        for r in range(len(data)):
                                            ind = a_local_ind[r]
                                            # Different behavior compared to Matlab: a.local[ind[0], ind[1]] = data[r]
                                            a.local[slice(ind[0][0],ind[0][-1]+1),slice(ind[1][0],ind[1][-1]+1)] = data[str(r)]
                        # the local processor is either in a's or b's map, otherwise should just fall through
                    # iterate thorugh a's processor list
                # iterate through b's processor list
            # maps not the same - redistribution
        else:
            # A[i:j, k:l] = B
            ind[0] = s['subs'][0]
            ind[1] = s['subs'][1]
            a_local_ind = get_local_ind(a.global_ind, ind)
            if size(a.local[a_local_ind[:]])==size(b.local):
                a.local[a_local_ind[:]] = b.local
            else:
                print('DMAT/subsasgn_2D: Subscripted assignment dimensions mismatch.')
                exit()
    if DEBUG:
        print('<-- Exiting subsasgn_2D')
    
    return a

