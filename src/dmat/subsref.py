from multipledispatch import dispatch
import numpy as np
from math import ceil,floor

import pPython as GPC
from Dmap import *
from Dmat import *
from size import *
from find import *
from inmap import *
from submat import *

@dispatch(Dmap,object)
def subsref(a,s):
    """
    SUBSREF Subscripted reference.
    A.FIELD - allows the fields of a MAP objects to be referenced using
    the '.' notation (complies with structure behavior).
    
    This functionality might be deprecated from the final API, to limit
    control the user has of private members of the MAP object. SUBSREF
    might be replaced by getter functions.
    
    Python version: Dr. Chansup Byun
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering subsref for Dmap objects')
        
    """
    Note: Matlab is flexible to deal with whether s is a single structure or an array.
    In order to deal with that behavior in Python, coding becomes a little bit lengthy.
    s can be a single dictionary variable or a list of dictionary variables.
    """
    
    if isinstance(s,list):
        if s[0]['type']=='.': #subscripting type
            # switch s(1).subs
            if s[0]['subs']=='dim':
                b = a.dim
            elif s[0]['subs']=='proc_list':
                b = a.proc_list
            elif s[0]['subs']=='dist_spec':
                b = a.dist_spec
            elif s[0]['subs']=='grid_spec':
                # added for Python implementation
                b = a.grid_spec
            elif s[0]['subs']=='grid':
                b = a.grid
            elif s[0]['subs']=='overlap':
                b = a.overlap
            else:
                raise Exception('%s is not a field of Dmap.'%(s['subs']))
        if DEBUG:
            print(b)
        # recursive call
        b = subsref(a, s[1:])
    else:
        if s['type']=='.': #subscripting type
            # switch s(1).subs
            if s['subs']=='dim':
                b = a.dim
            elif s['subs']=='proc_list':
                b = a.proc_list
            elif s['subs']=='dist_spec':
                b = a.dist_spec
            elif s['subs']=='grid_spec':
                # added for Python implementation
                b = a.grid_spec
            elif s['subs']=='grid':
                b = a.grid
            elif s['subs']=='overlap':
                b = a.overlap
            else:
                raise Exception('%s is not a field of Dmap.'%(s['subs']))
    if DEBUG:
        print('<--> Exiting subsref for Dmap objects')
    return b

@dispatch(Dmat,object)
def subsref(a,s):
    """
    SUBSREF Subscripted reference. Called for syntax A(S).
    Should not be called directly.
    SUBSREF(A, S) Subscripted reference on a distributed array A.
    S is a structure array with the fields:
    type -- string containing '()', '{}', or '.' specifying the subscript type.
    subs -- Cell array or string containing the actual subscripts.
    
    Note: Matlab is flexible to deal with whether s is a single structure or an array.
    In order to deal with that behavior in Python, coding becomes a little bit lengthy.
    s can be a single dictionary variable or a list of dictionary variables.

    !!!WARNING: Does not produce a stand-alone distributed array.
    
    Python version: Dr. Chansup Byun
    Author:  Nadya Travinin
    Edited:  Edmund L. Wong (elwong@ll.mit.edu)
    """
    DEBUG = 1
    if DEBUG:
        print('--> Entering subsref for distributed objects')
    
    sizeA = size(a)
    if isinstance(s,list):
        subs = s[0]['subs']
        stype = s[0]['type']
    else:  
        # assuming a single dictionary variable
        subs = s['subs']
        stype = s['type']

    #
    # Array access.
    #
    if stype=='()': #subscripting type
        # TODO eventually support < cases
        if len(subs) > ndims(a):
            raise Exception('@dmat/subsref: Too many dimensions')
        elif len(subs) < ndims(a):
            raise Exception('@dmat/subsref: Too few dimensions')

        #set submat flag to 0
        submat_flag = 0
    
        # check to make sure that the indices before the last are
        # within bounds
        f_all = 1
        for i in range(ndims(a)):
            if subs[i] != ':':
                f_all = 0
                if len(subs[i]) != 1:
                    #adjust submat flag
                    submat_flag = 1
                elif subs[i] > sizeA[i]: # && i <= ndims(a)
                    raise Exception('@dmat/subsref: Index exceeds dmat dimensions')
    
        if not submat_flag: #if reference consist of combinations of : and single numbers, use this code
            # expand the dimensions if needed
            # TODO doesn't follow Matlab semantics if last specified
            # dimension is : and it needs to be expanded, so it has been
            # disabled for the time being
            #
            #excess = subs{len(subs)}
            #for i=len(subs):ndims(a)
            #  subs[i] = mod(excess-1, sizeA) + 1
            #  excess = floor((excess-1) / sizeA(len(subs))) + 1
            #end
    
            #
            # If all subscripts are :, return the entire matrix otherwise
            # call submatrix.
            #
            if f_all:
                b = a.copy()
            else:
                #
                # Commonly used variables.
                #
                m = a.map
                gridA = m.grid
                distA = m.dist_spec
                sizeB = sizeA # initialize size of B to be size of A
    
                #
                # TODO should use FALLS structure if handling subscript ranges, but
                # currently that is not supported.  Thus using simpler approach.
                #
                s_map = dict()
                s_map['subs'] = dict()
                s_data = dict()
                s_data['subs'] = dict()
                for i in range(len(subs)):
                    if len(subs[i]) == 1:
                        if subs[i] != ':':
                            if subs[i] < 1 or subs[i] > sizeB[i]:
                                raise Exception('@dmat/subsref: The %d-th subscript exceeds size of dmat'%(i))
    
                            # figure out distribution
                            if distA[i]['dist']=='b':
                                # block - take the subscript and divide by the block size =
                                # size(a, i) / size(gridA, i)
                                b_size = ceil(size(a, i) / size(gridA, i))
                                idx = floor((subs[i]) / b_size) 
                                off = subs[i]%b_size
    
                            elif distA[i]['dist']=='c':
                                # cyclic - find the remainder of the subscript divided by
                                # the number of processors in that dimension
                                idx = subs[i]%size(gridA, i)
                                off = floor(subs[i] / size(gridA, i))
    
                            elif distA[i]['dist']=='bc':
                                # block cyclic - find out which block this would lie on (block),
                                # and then find out which processor owns this block (cyclic)
                                idx = floor(subs[i] / distA[i]['b_size'])
                                off = distA[i]['b_size'] * floor(idx / size(gridA, i)) + subs[i]%distA[i]['b_size']
                                idx = idx%size(gridA, i)
    
                            else:
                                raise Exception('@dmat/subsref: Unsupported distribution type: %s'%(distA.type))
                            #
                            # Set up the subscripts.
                            #
                            s_map['subs'][i] = idx
                            s_data['subs'][i] = off
                            sizeB[i] = 1
                        else:
                            s_map['subs'][i] = ':'
                            s_data['subs'][i] = ':'
                    else:
                        raise Exception('@dmat/subsref: Unsupported subscript: %s'%(subs[i]))
                #
                # Find the map that would contain these processors and create a
                # dmat using this map.
                #
                s_map['type'] = '()'
                s_data['type'] = '()'
                # find() returns a list
                maxGenDim = max(find(sizeB != 1)+[2])
                sizeB = sizeB[0:maxGenDim]
                gridB = subsref(gridA, s_map)
                mapB = Dmap(size(gridB), m.dist_spec[0:maxGenDim], reshape(gridB, 1, np.prod(size(gridB))))
                b = Dmat(sizeB, map=mapB)
    
                #
                # If local processor has data that needs to be sent, send it.
                #
                if np.prod(size(a.local)) > 0 and inmap(mapB, GPC.Pid):
                    b.local = subsref(a.local, s_data)

        else: #make a call to submat with a warning
            print(
                '''Warning:
                dmat/subsref: Fully functional sibscripted reference
                is only supported for indices that consist of combinatioons
                of : and single number. Otherwise, please restrict operation
                to the local part of the referenced structure. Stand alone
                distirbuted array will not be returned.
                ''')
            b = submat(a,s)

        #
        # Structure reference.
        #
    elif stype=='.': #subscripting type
        if subs == 'local':
            b = a.local
        elif subs == 'map':
            b = a.map
        else:
            raise Exception('@dmat/subsref: %s cannot be accessed directly or is not a field of DMAT.'%(subs))
    #
    # Recursive call
    #
    if len(s) > 1:
        b = subsref(a, s[2:end])
    end

        
    if DEBUG:
        print('<--> Exiting subsref for distributed objects')
    return b
    
