import math
import numpy as np

from MPI_Send import *
from MPI_Recv import *

import pPython as GPC
from GridDmat import *
from n_dim_find import *
from inmap import *

def synch(d):
    """Syncronize the data in the distribute matrix. 
    
    Usage:
    ------
    d = synch(d) 
    
    SYNCH(D) No-op if there is no overlap. If overlap is present, the owner
        processor of the overlaping data sends its data to the processor that
        owns the copy of the overlapping data. The owner is the processor with
        the higher index in the grid in the corresponding dimension. For
        example, if the overlap is in the second dimension the owner is the
        processor in the column of the grid with the higher index.
    
    d: distributed array
 
    Author: Nadya Travinin
    python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering synch')

    if not isinstance(d,GridDmat):
        return d

    p = d.map
    # find current processor index in the grid
    proc_grid = p.grid
    my_grid_ind = n_dim_find(proc_grid, GPC.my_rank)
    # obtain the process grid dimensions
    grid_dims = list(proc_grid.shape)

    if inmap(p, GPC.my_rank):
        subs = []
        for i  in range(d.dim): # syncronize each dimension of distributed array
            if bool(p.overlap): # overlap description defined
                if p.overlap[i]>0: # overlap is greater than 0
                
                    ind_adjuster = np.zeros(d.dim,dtype=int)
                    ind_adjuster[i] = -1
                                    
                    # increment tag
                    GPC.tag_num = GPC.tag_num+1
                    GPC.tag = 'tag-'+str(GPC.tag_num)
                
                    # CB: the following implicitly assumes that both process grid and data dimensions match
                    recv_proc_ind = my_grid_ind+ind_adjuster
                    if DEBUG:
                        print('recv_proc_ind:')
                        print(recv_proc_ind)
                
                    # if the rank is not at the starting edge in the i-th direction (dimension)
                    if my_grid_ind[i] > 0:
                        str_sub_data = 'd.local['
                        for s in range(len(p.overlap)):
                            if p.overlap[s] > 0:
                                str_sub_data += '0:'+str(p.overlap[s])+','
                            else:
                                str_sub_data += ':,'
                        # Take care of the last character
                        str_sub_data = str_sub_data[0:-1]+']'
                        if DEBUG:
                            print('string representation for subset array: %s'%(str_sub_data))
                        data = eval(str_sub_data)
                        
                        # Construct a string to extract process rank to send the data
                        str_proc_grid = 'proc_grid['
                        for j in range(d.dim):
                            str_proc_grid += 'recv_proc_ind['+str(j)+'],'
                        str_proc_grid = str_proc_grid[0:-1]+']'
                        if DEBUG:
                            print(str_proc_grid)
                        send_to_rank = eval(str_proc_grid)
                        MPI_Send(send_to_rank, GPC.tag, GPC.comm, data)
                
                    ind_adjuster[i] = 1
                    send_proc_ind = my_grid_ind+ind_adjuster
                    if DEBUG:
                        print('send_proc_ind:')
                        print(send_proc_ind)
                
                    if my_grid_ind[i] < grid_dims[i]-1:
                        # Construct a string to extract process rank to send the data
                        str_proc_grid = 'proc_grid['
                        for j in range(d.dim):
                            str_proc_grid += 'send_proc_ind['+str(j)+'],'
                        str_proc_grid = str_proc_grid[0:-1]+']'
                        if DEBUG:
                            print(str_proc_grid)
                        recv_from_rank = eval(str_proc_grid)
                        [data] = MPI_Recv(recv_from_rank, GPC.tag, GPC.comm)

                        local_dims = (d.local).shape
                        
                        
                        str_sub_data = 'd.local['
                        for s in range(len(p.overlap)):
                            if p.overlap[s] > 0:
                                str_sub_data += str(local_dims[s]-p.overlap[s])+':'+str(local_dims[s])+','
                            else:
                                str_sub_data += ':,'
                        # Take care of the last character
                        str_sub_data = str_sub_data[0:-1]+'] = data'
                        if DEBUG:
                            print('string representation for subset array: %s'%(str_sub_data))
                        exec(str_sub_data)
               # End of section with overlap is greater than 0
            # End of section for overlap description defined
        # syncronize each dimension

    if DEBUG:
        print('--> Exiting synch')

    return d

