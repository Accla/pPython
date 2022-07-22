from get_global_ind import *
from get_local_ind import *

def subsasgn_data(a, b, falls_index, fi):
    """
    SUBSASGN_DATA Helper function for distributed array subsasgn.
    
    SUBSASGN_DATA(A, B, FALLS_INDEX, FI) Computes which data to send from
    distributed array B to distributed array A based on falls intersection FI.
    
    a,b: distributed arrays
    fi: a dictionary based on the dimension
    
    data, a_local_ind: dictionary variables with numeric key
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """
    DEBUG = 1
    if DEBUG:
        print('--> Entering subsasgn_data')
    
    # dimension of the distributed object
    dim = len(fi)
    
    data = dict()
    a_local_ind = dict()
    
    if dim==2:
        num_data=0
        for f1 in range(len(fi[0][falls_index])):
            for f2 in range(len(fi[1][falls_index])):
                fi_temp = []
                fi_temp.append(fi[0][falls_index][f1])
                fi_temp.append(fi[1][falls_index][f2])
                g_ind = get_global_ind(fi_temp)
                b_local_ind = get_local_ind(b.global_ind, g_ind)
                if DEBUG:
                    # print('b.local')
                    # print(b.local)
                    print('b_local_ind')
                    print(b_local_ind)
                if len(b_local_ind[0])>0 and len(b_local_ind[1])>0:
                    # Different behavior as compared to Matlab: data[num_data] = b.local[b_local_ind[0], b_local_ind[1]]
                    data[num_data] = b.local[slice(b_local_ind[0][0],b_local_ind[0][-1]+1),slice(b_local_ind[1][0],b_local_ind[1][-1]+1)]
                else:
                    # Workaround for Matlab, which still works with empty index
                    data[num_data] = None
                a_local_ind[num_data] = get_local_ind(a.global_ind, g_ind)
                num_data=num_data+1

    elif dim==3:
        num_data=0
        for f1 in range(len(fi[0][falls_index])):
            for f2 in range(len(fi[1][falls_index])):
                for f3 in range(len(fi[2][falls_index])):
                    fi_temp = []
                    fi_temp.append(fi[0][falls_index][f1])
                    fi_temp.append(fi[1][falls_index][f2])
                    fi_temp.append(fi[2][falls_index][f3])
                    g_ind = get_global_ind(fi_temp)
                    b_local_ind = get_local_ind(b.global_ind, g_ind)
                    if len(b_local_ind[0])>0 and len(b_local_ind[1])>0 and len(b_local_ind[2])>0:
                        # Workaround for Matlab, which still works with empty index
                        data[num_data] = b.local[b_local_ind[0], b_local_ind[1], b_local_ind[2]]
                    else:
                        # Workaround for Matlab, which still works with empty index
                        data[num_data] = None
                    a_local_ind[num_data] = get_local_ind(a.global_ind, g_ind)
                    num_data=num_data+1

    elif dim==4:
        num_data=0
        for f1 in range(len(fi[0][falls_index])):
            for f2 in range(len(fi[1][falls_index])):
                for f3 in range(len(fi[2][falls_index])):
                    for f4 in range(len(fi[3][falls_index])):
                        fi_temp = []
                        fi_temp.append(fi[0][falls_index][f1])
                        fi_temp.append(fi[1][falls_index][f2])
                        fi_temp.append(fi[2][falls_index][f3])
                        fi_temp.append(fi[3][falls_index][f4])
                        g_ind = get_global_ind(fi_temp)
                        b_local_ind = get_local_ind(b.global_ind, g_ind)
                        if len(b_local_ind[0])>0 and len(b_local_ind[1])>0 and len(b_local_ind[2])>0 and len(b_local_ind[3])>0:
                            # Workaround for Matlab, which still works with empty index
                            data[num_data] = b.local[b_local_ind[0], b_local_ind[1], b_local_ind[2], b_local_ind[3]]
                        else:
                            # Workaround for Matlab, which still works with empty index
                            data[num_data] = None
                        a_local_ind[num_data] = get_local_ind(a.global_ind, g_ind)
                        num_data=num_data+1
    else:
        print('DMAT/SUBSASGN_DATA: Only objects up to four (4) dimensions are supported.')
        exit()

    if DEBUG:
        print('<-- Exiting subsasgn_data')
    return  [data, a_local_ind]
 
