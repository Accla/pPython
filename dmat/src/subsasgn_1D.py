import numpy as np

import pPython as GPC
from GridDmat import *
from size import *
from subsasgn_2D import *
from subsasgn_3D import *
from subsasgn_4D import *

def subsasgn_1D(a,s,b):
    """
    subsasgn_1D One dimensional subsasgn.
    
    S is of the following form [:], independent of the dimension of the
    distributed object dimension.
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """

    DEBUG = 1
    if DEBUG:
        print('--> Entering subsasgn_1D')

    # Instead of creating a copy of a, write directly to the memory
    # allocated for a in the caller's workspace
    # Not needed with Python: assignin('caller', inputname(1), [])
    
    if isinstance(b, (float, np.float64, np.ndarray)): # RHS is a scalar or an array
        if s['subs'][0]==':':
            if (len(size(b))==2) and (size(b)==[1,1]): 
                # b is a scalar
                # if (size(b)==[1 1])
                if inmap(a.map, GPC.my_rank):
                    # assigment to a scalar
                    a.local[:] = b

            else:
                # b is a regular non distributed matrix
                # check that dimensions are the same and redistribute
                # according to a's map
                if (size(b) == a.shape): # dimensions are the same
                    if a.dim == 2: # 2-D
                        a.local[:,:] = b[a.global_ind['0'], a.global_ind['1']]
                    elif a.dim == 3: # 3-D
                        a.local[:,:,:] = b[a.global_ind['0'], a.global_ind['1'], a.global_ind['2']]
                    elif a.dim == 4: # 4-D
                        a.local[:,:,:,:] = b[a.global_ind['0'], a.global_ind['1'], a.global_ind['2'], a.global_ind['3']]
                    else: # dimension > 4
                        print('DMAT/subsasgn_1D: Only up to 4 dimensional objects supported.')
                        exit()
                        # distributed object dimension
        else:
            print('unsupported indexing')
            exit()

    elif isinstance(b, GridDmat): # RHS is a DMAT
        if isinstance(s['subs'][0], str):  # subscript is a CHAR
            if s['subs'][0] == ':': # subscript is a ':'
                if a.dim == 2: # 2-D
                    s['subs'][1] = ':'
                    a = subsasgn_2D(a,s,b)
                elif a.dim == 3: # 3-D
                    s['subs'][1] = ':'
                    s['subs'][2] = ':'
                    a = subsasgn_3D(a,s,b)
                elif a.dim == 4: # 4-D
                    s['subs'][1] = ':'
                    s['subs'][2] = ':'
                    s['subs'][3] = ':'
                    a = subsasgn_4D(a,s,b)
                else:
                    # >4-D
                    print('DMAT/subsasgn_1D: Only up to 4 dimensional objects supported.')
                    exit()
                    # >4-D
            else:
                # subscript is not ':'
                print('unsupported indexing')
                exit()
                # subscript is not ':'
        else:
            # subscript is NOT a CHAR
            print('unsupported indexing')
            exit()
            # subscript is NOT a CHAR
    else: 
        # RHS is a not a DMAT or a DOUBLE
        print('DMAT/subsasgn_1D: RHS must be a DOUBLE or DMAT.')
        exit()
        # RHS is a not a DMAT or a DOUBLE

    if DEBUG:
        print('<-- Exiting subsasgn_1D')
    return a

