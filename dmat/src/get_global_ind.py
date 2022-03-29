from GridFalls import *

def get_global_ind(falls, grid_dims=None):
    """Returns a list array of global indices stored locally given
    a FALLS object (list array of FALLS, one for each dimension)
    
    Usage:
    ------
    ind = get_global_ind(falls)
    ind = get_global_ind(falls,grid_dim)
    
    FALLS: array of FALLS objects
    grid_dims:
    IND:
        len(IND) is equal to the number of dimensions of the distributed
        object. IND(i) is of the form [ind1 ind2 ind3 ...] where ind_i is a
        global index of the distributed object that is local to the current
        processor.
        
        ToDo: should it be a list or a dictionary?
        
    Author:   Nadya Travinin (pMatlab)
    Python version: Dr. Chansup Byun (gridPython)
    """
    
    DEBUG = 0
    
    if DEBUG:
        print('--> Entering get_global_ind')
    
    dim = len(falls)
    if not grid_dims:
        grid_dims=[]
    
    if dim <= 4:
        ind = dict()
        for i in range(dim):
            temp = []
            falls_i = falls[i]
            if isinstance(falls_i,type(GridFalls())):
                # falls is an instance of GridFalls class
                if (len(grid_dims)>0) and (grid_dims[i] == 1): 
                    # dimension is not distributed
                    # print('get_global_ind: To be checked, am i here?')
                    temp += list(range(falls_i.local_len))
                else: #dimension is distributed
                    # get the indices for the first n-1 cycles
                    # NOTE: This takes care of the case when complete_cycle==0 and
                    #       complete_block==1
                    if DEBUG:
                        print('falls_i.n-1 = %d'%(falls_i.n-1))
                    for j in range(0,falls_i.n-1):
                        lval = falls_i.l+j*falls_i.s
                        rval = falls_i.r+j*falls_i.s+1
                        temp += list(range(lval,rval))
                        if DEBUG:
                            print('j = %d'%(j))
                            print('(Left,Right): %d,%d'%(lval,rval))
                            print(temp)
                        
                    # get indices for the n-th cycle, if it exists
                    if (falls_i.complete_cycle and falls_i.complete_block): 
                        # complete n-th cycle, complete block
                        if DEBUG:
                            print('complete n-th cycle & complete block')
                            print(falls_i.l+(falls_i.n-1)*falls_i.s)
                            print(falls_i.r+(falls_i.n-1)*falls_i.s+1)
                        i_left = falls_i.l+(falls_i.n-1)*falls_i.s
                        i_rght = falls_i.r+(falls_i.n-1)*falls_i.s+1
                        temp += list(range(i_left,i_rght))
 
                    elif (not falls_i.complete_cycle) and (not falls_i.complete_block):
                        if DEBUG:
                            print('incomplete n-th cycle & incomplete block')
                        # incomplete n-th cycle, incomplete block  
                        block_size = falls_i.r-falls_i.l+1
                        rem_block = falls_i.local_len%block_size
                        if falls_i.dist == 'b':
                            temp += list(range(falls_i.l,falls_i.r+1))
                        else:
                            i_left = falls_i.l+(falls_i.n-1)*falls_i.s
                            i_rght = falls_i.l+(falls_i.n-1)*falls_i.s+rem_block
                            temp += list(range(i_left,i_rght))
                            # temp += list(range(falls_i.l+(falls_i.n-1)*falls_i.s,falls_i.l+(falls_i.n-1)*falls_i.s+rem_block))
            else:
                print('falls instance is not GridFalls type.')
                
            # store temp in ind
            ind[str(i)] = temp
                
    else:
        print('ERROR(get_global_ind): Only objects up to 4-D are supported')
        exit()

    if DEBUG:
        print(ind)
        print('--> Eexiting get_global_ind')

    return ind

