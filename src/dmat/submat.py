import GridPython as GPC

from GridMap import *
from GridDmat import *
from get_ind_range import *
from get_local_ind import *
from get_local_proc import *
from gen_pitfalls import *
from get_local_falls import *
from size import *

def submat(a, s):
    """
    SUBMAT  Helper function used by subsref.
    
    SUBMAT(A, S) Helper function used by subscripted reference. A is a
    distributed array, S is a structure array with the fields:
    type -- string containing '()', '{}', or '.' specifying the subscript type.
    subs -- Cell array or string containing the actual subscripts.
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """
    DEBUG = 1
    if DEBUG:
        print('--> Entering submat')

    #CB Introduce s_type and s_subs to deal with a single or a list of dictionary variable(s)
    if isinstance(s,list):
        s_type = s[0]['type']
        s_subs = s[0]['subs']
    else:
        s_type = s['type']
        s_subs = s['subs']

    b = GridDmat()
    
    if a.dim==2:  # 2-D
        if isinstance(s_subs[0], str) and isinstance(s_subs[1], str):
            if (s_subs[0]==':') and (s_subs[1]==':'): # A(:,:)
                b = a

        elif (len(s_subs[0])==1) and (len(s_subs[1])==1) and \
        (not isinstance(s_subs[0], str)) and (not isinstance(s_subs[1], str)): # A(i,j)
            # ----CASE 1 on SUBSREF development plan----
            ind = get_ind_range(a,s)
            local_ind = get_local_ind(a.global_ind, ind)
    
            # need to figure out on all procs where the index is local
            r = get_local_proc(a.pitfalls, a.map.grid, [ind[0],ind[1]])
            # define new map
            new_map = GridMap([1,1], {}, [r])
            # create a new GridDmat object
            """
            Properties need to be set:
            d.map = self.map
            d.dim = self.dim
            d.shape = self.shape (size in pMatlab)
            d.pitfalls = self.pitfalls
            d.falls = self.falls
            d.local_dim = self.local_dim # added with gridPython
            d.global_ind = self.global_ind
            # create an array same as d.local
            d.local = np.zeros(self.local.shape)
            d.local[:] = self.local
            """
            b.map = new_map
            b.dim = a.dim
            b.shape = [len(ind[0]),len(ind[1])]
            # create a PITFALLS for each dimension
            for i in range(new_map.dim):
                b.pitfalls[i] = gen_pitfalls(size(new_map.grid,i), new_map.dist_spec[i], 1)
            b.falls = get_local_falls(b.pitfalls, new_map.grid, GPC.my_rank)
            b.local = a.local[local_ind[0], local_ind[1]]
            b.local_dim = size(b.local)  # added with gridPython
            grid_dims = size(new_map.grid)
            b.global_ind = get_global_ind(b.falls, grid_dims)
            # ----CASE 1 on SUBSREF development plan----
        else:
            ind = get_ind_range(a,s)
            local_ind = get_local_ind(a.global_ind, ind)
            b.map = a.map
            b.dim = a.dim
            b.shape = [len(ind[0]),len(ind[1])]
            b.pitfalls = a.pitfalls
            b.falls = a.falls
            b.local = a.local[local_ind[0], local_ind[1]]
            b.local_dim = size(b.local)  # added with gridPython
            b.global_ind = a.global_ind
    elif a.dim==3:  # 3-D
        if (s_subs[0]==':') and (s_subs[1]==':') and (s_subs[2]==':'): # A(:,:,:)
            b = a
        else:
            ind = get_ind_range(a,s)
            local_ind = get_local_ind(a.global_ind, ind)
            b.map = a.map
            b.dim = a.dim
            b.shape = [len(ind[0]),len(ind[1]),len(ind[2])]
            b.pitfalls = a.pitfalls
            b.falls = a.falls
            b.local = a.local[local_ind[0], local_ind[1], local_ind[2]]
            b.local_dim = size(b.local)  # added with gridPython
            b.global_ind = a.global_ind
    elif a.dim==4: # 4-D
        if (s_subs[0]==':') and (s_subs[1]==':') and (s_subs[2]==':') and (s_subs[3]==':'): # A(:,:,:,:)
            b = a
        else:
            ind = get_ind_range(a,s)
            local_ind = get_local_ind(a.global_ind, ind)
            b.map = a.map
            b.dim = a.dim
            b.shape = [len(ind[0]),len(ind[1]),len(ind[2]),len(ind[3])]
            b.pitfalls = a.pitfalls
            b.falls = a.falls
            b.local = a.local[local_ind[0], local_ind[1], local_ind[2], local_ind[3]]
            b.local_dim = size(b.local)  # added with gridPython
            b.global_ind = a.global_ind

    else:
        print('SUBMAT: Only up to 4 dimensions are supported.')
        exit()

    if DEBUG:
        print('<-- Exiting submat')
           
    return b

