import numpy as np
from sys import getsizeof

import pyMPI_COMM_WORLD as pyMCW
from MPI_Comm_rank import *

from Dmap import *
from local import *
from put_local import *
from subsasgn import *
from gen_pitfalls import *
from get_local_falls import *
from local_dims import *
from get_global_ind import *
from print_pitfalls import *
from print_falls import *
from submat import *
from ndims import *
from tup2ary import *
from exec_subsref import *
from size import *

class Dmat:
    """Define Dmat class.
    """
    def __init__(self, nbytes, dtype, *array_sizes, **keywords):
        """Distributed matrix constructor.
        Creates the necessary data structures for the distributed matrix.

        Input:
        array_sizes: array sizes
        keywords:
            'map': 1 or distributed map, Dmap object
            'dtype': data type of array element
        
        NOTE: DMAT does not allocate memory for the distributed matrix
        and should never be called directly.  A distributed matrix should
        always be created with an appropriate constructor (ZEROS, ONES, RAND
        or SPARSE) which will be responsible for allocating memory.
        
        DMAT(N, P) If N is a scalar, creates the necessary data
            structures for an NxN distributed matrix; if N is a vector, 
            creates the necessary structures for an N distributed matrix
        DMAT(M, N, P) Creates the necessary data structures for an MxN
            distributed matrix.
        DMAT(M, N, Q, P) Creates the necessary data structures for an MxNxQ
            distributed array.
        DMAT(M, N, Q, R, P) Creates the necessary data structures for an
            MxNxQxR distributed array.
        
        D:
        D.MAP - processor map onto which the distributed array is mapped.  
        D.DIM - dimension of the distributed array. The dimension of the map has 
            to be consistent with the dimension of the distributed array.
        D.SIZE - size of the distributed array, i.e. number of elements in each
            dimension.
        D.PITFALLS - pitfalls structure that describes the distribution of the
            distributed array among the processors in the map.
        D.FALLS - falls structure that describes the distribution of the
            distributed object on the local processor.
        D.LOCAL - numerical part of the distributed array stored on the local
            processor.  Memory for D.LOCAL will be allocated by constructor
            functions, such as ZEROS, ONES, RAND and SPARSE.
        D.LOCAL_DIM - the size of local part of the distributed array (added with pPython)
        D.GLOBAL_IND - global indices of the distributed array local to the
            current processor.
        
        See also: ONES, ZEROS, RAND, SPARSE.
        
        Author:  Nadya Travinin
        Edited:  Edmund L. Wong (elwong@ll.mit.edu)
        Python version: Dr. Chansup Byun
        """
        
        DEBUG = 0
        if DEBUG:
            print('--> Entering Dmat.init')
        #
        # Initialize properties
        self._nbytes = nbytes
        self._dtype = dtype
        if DEBUG:
            print('Dmat: define dtype = %s'%(self._dtype))

        # form dims vector
        if array_sizes == None or len(array_sizes)==0:
            self.local = None
            return
        elif isinstance(array_sizes[0],list):
            ndim = len(array_sizes[0])
            dims = array_sizes[0]
        else:
            ndim = len(array_sizes)
            dims = []
            for k in range(ndim):
                dims.append(array_sizes[k])
        if DEBUG:
            print('Dimension of distributed dmat array: %d'%(len(dims)))
            print(array_sizes)
            print('dims = ',end='')
            print(dims)
    
        if ndim>4:
            raise Exception('ERROR(Dmat): array dimension larger than 4-D is not supported')
    
        dmap = None
        if 'map' in keywords:
            if isinstance(keywords['map'], Dmap):
                dmap = keywords['map']
            elif isinstance(keywords['map'], int):
                dmap = 1
    
        if not isinstance(dmap,Dmap):
            # Not a distributed array 
            self.local = np.zeros(dims,dtype)
            return
        
        if len(dims) == 1: # DMAT(M, P)
            dims = dims + dims
        
        self.map = dmap
        self.dim = len(dims)
        # Use 'shape' instead of 'size' in order to be compatible with a NumPy array
        # Deprecated: self.size = dims
        self.shape = dims
        if isinstance(dmap,Dmap) and (dmap['dim'] != len(dims)):
            raise Exception('ERROR(Dmat): Map and distributed object dimensions must match')
            
        # create a PITFALLS for each dimension
        pitfalls = []
        for i in range(dmap['dim']):
            if DEBUG:
                print('Dmat: axis, i = %d'%(i))
                print(dmap['grid'].shape[i])
                print(dmap['dist_spec'][i])
                print(dims[i])
            if not (dmap['overlap']):
                # dmap['grid'].shape: tuple of the dim length
                # dmap['dist_spec']: a dictionary of dictoary with key in str(dim)
                # print('no overlap')
                pitfalls.append(gen_pitfalls(dmap['grid'].shape[i], dmap['dist_spec'][i], dims[i]))
            elif dmap['overlap'][i]==0:
                # Same as not defined dmap['overlap']
                # print('zero overlap')
                pitfalls.append(gen_pitfalls(dmap['grid'].shape[i], dmap['dist_spec'][i], dims[i]))
            else:
                # non-zero dmap['overlap'] is defined.
                if DEBUG:
                    print('non-zero overlap')
                    print("dmap['overlap']: %d in axis, i = %d"%(dmap['overlap'][i],i))
                pitfalls.append(gen_pitfalls(dmap['grid'].shape[i], dmap['dist_spec'][i], dims[i], dmap['overlap'][i]))
        
        self.pitfalls = pitfalls
        if DEBUG:
            print(type(pitfalls))
            for i in range(len(pitfalls)):
                pf = pitfalls[i]
                print('grid_mat: pitfalls in axis, i, %d'%(i))
                print_pitfalls(pf)
                
        # get the local rank
        comm = pyMCW.MPI_COMM_WORLD
        my_rank = MPI_Comm_rank(comm)
        
        # get the local falls
        self.falls = get_local_falls(self.pitfalls, dmap['grid'], my_rank)
        if DEBUG:
            print(dmap['grid'])
            print(my_rank)
            for i in range(len(self.falls)):
                f = self.falls[i]
                print('grid_mat: FALLS in axis, i = %d'%(i))
                print_falls(f)
            
        # figure out local dimensions (d.local_dim added with pPython)
        local_dim = local_dims(self.falls, self.dim);
        self.local_dim = local_dim
        if DEBUG:
            print('global Dmat shape: ', end='')
            print(self.shape)
            print('local dimension: ', end='')
            print(local_dim)
        
        # Allocating memory is the responsibility of map functions
        # (e.g. ones, zeros, rand and sparse)
        # pPython: allocate memory for sparse method
        self.local = np.zeros(self.local_dim, dtype)
        if DEBUG:
            print('Dmat local array: ')
            print(self.local)
        
        # get the local indices for the current processor
        grid_dims = dmap['grid_spec']
        if len(grid_dims)<dmap['dim']:
            for i in range(len(grid_dims),dmap['dim']+1):
                grid_dims.append(0)
        
        self.global_ind = get_global_ind(self.falls, grid_dims)

        # Calculate the actual memory usage
        nbytes = getsizeof(self.shape)+getsizeof(self.map)+getsizeof(self.local)+\
                getsizeof(self.falls)+getsizeof(self.dim)+getsizeof(self.pitfalls)+\
                getsizeof(self.local_dim)+getsizeof(self.global_ind)+getsizeof(self._dtype)+\
                64
                # getsizeof(self.copy)
        self._nbytes = nbytes

        if DEBUG:
            print('<-- Exiting Dmat.init')

    @property
    def nbytes(self):
        # print("Getting nbytes value...")
        return self._nbytes
    @nbytes.setter
    def nbytes(self, value):
        # print("Setting nbytes value...")
        self._nbytes = value

    @property
    def dtype(self):
        # print("Getting dtype value...")
        return self._dtype
    @dtype.setter
    def dtype(self, value):
        # print("Setting dtype value...")
        self._dtype = value

    def __getitem__(self, item):
        """
        Make the Dmat object scriptable
        """
        DEBUG = 0
        if DEBUG:
            print('  --> Entering __getitem__ in Dmat')
            print(item)
        # return getattr(self, item)

    def __setitem__(self, index, d):
        """Implement __setitem__ with Dmat()
           d: RHS distributed array, Dmat 
           self: LHS distributed array, Dmat object, to be set by d 
        """
        # Invoke Python equivalent function similar to a MATLAB subsasgn operator 
        DEBUG = 0
        if DEBUG:
            print('--> Entering Dmat.setitem() ')
            print('Class Dmat: see if this is called by A[:,:] = B where A and B are Dmat()')
            print('What is passed as index: ')
            print(index)
        # [:,:] -> (slice(None, None, None), slice(None, None, None))
        # check the dimension of the distributed array, b
        s = []
        ss = dict()
        if not isinstance(index,tuple): # 1-D distributed array
            raise Exception('Dmat: 1-D assignment, not implemented yet.')
        else:
            if len(index)==2: # 2-D distributed array
                if DEBUG:
                    print('Dmat: 2-D assignment update')
                if index[0]==slice(None, None, None) and index[1]==slice(None, None, None):
                    ss['type'] = '()'
                    ss['subs'] = dict()
                    ss['subs'][0] = ':'
                    ss['subs'][1] = ':'
                    s.append(ss)
                elif isinstance(index[0],(np.int32,int)) and isinstance(index[1],(np.int32,int)):
                    if DEBUG:
                        print('Dmat: single element update')
                    ss['type'] = '()'
                    ss['subs'] = dict()
                    ss['subs'][0] = slice(index[0],index[0]+1,None)
                    ss['subs'][1] = slice(index[1],index[1]+1,None)
                    s.append(ss)
                else:
                    print('type(index[0]')
                    print(type(index[0]))
                    raise Exception('Dmat: 2-D assignment, not implemented this index type yet.')
            elif len(index)==3: # 3-D distributed array
                if index[0]==slice(None, None, None) and index[1]==slice(None, None, None) and index[2]==slice(None, None, None):
                    if DEBUG:
                        print('Dmat: 3-D assignment update with case 1')
                    ss['type'] = '()'
                    ss['subs'] = dict()
                    ss['subs'][0] = ':'
                    ss['subs'][1] = ':'
                    ss['subs'][2] = ':'
                    s.append(ss)
                elif isinstance(index[0],slice) and isinstance(index[1],slice) and isinstance(index[2],(np.int32,int)):
                    if DEBUG:
                        print('Dmat: 3-D assignment update with case 2')
                    ss['type'] = '()'
                    ss['subs'] = dict()
                    ss['subs'][0] = index[0]
                    ss['subs'][1] = index[1]
                    ss['subs'][2] = index[2]
                    s.append(ss)
                elif isinstance(index[0],(np.int32,int)) and isinstance(index[1],(np.int32,int)) and isinstance(index[2],(np.int32,int)):
                    if DEBUG:
                        print('Dmat: single element update')
                    ss['type'] = '()'
                    ss['subs'] = dict()
                    ss['subs'][0] = slice(index[0],index[0]+1,None)
                    ss['subs'][1] = slice(index[1],index[1]+1,None)
                    ss['subs'][2] = slice(index[2],index[2]+1,None)
                    s.append(ss)
                else:
                    for ii in range(len(index)):
                        print('type(index[%d])=%s'%(ii,type(index[ii])))
                    raise Exception('Dmat: 3-D assignment, not implemented this index type yet.')
            elif len(index)==4: # 4-D distributed array
                if DEBUG:
                    print('Dmat: 4-D assignment update')
                if index[0]==slice(None, None, None) and index[1]==slice(None, None, None) and index[2]==slice(None, None, None) and index[3]==slice(None, None, None):
                    ss['type'] = '()'
                    ss['subs'] = dict()
                    ss['subs'][0] = ':'
                    ss['subs'][1] = ':'
                    ss['subs'][2] = ':'
                    ss['subs'][3] = ':'
                    s.append(ss)
                elif isinstance(index[0],(np.int32,int)) and isinstance(index[1],(np.int32,int)) and isinstance(index[2],(np.int32,int)) and isinstance(index[3],(np.int32,int)):
                    if DEBUG:
                        print('Dmat: single element update')
                    ss['type'] = '()'
                    ss['subs'] = dict()
                    ss['subs'][0] = slice(index[0],index[0]+1,None)
                    ss['subs'][1] = slice(index[1],index[1]+1,None)
                    ss['subs'][2] = slice(index[2],index[2]+1,None)
                    ss['subs'][3] = slice(index[3],index[3]+1,None)
                    s.append(ss)
                else:
                    print('type(index[0]')
                    print(type(index[0]))
                    raise Exception('Dmat: 4-D assignment, not implemented this index type yet.')
            else: # unsupported distributed array dimension
                raise Exception('Dmat: un-supported distributed dimension.')

        # construct s for sub-assignment operations
        if DEBUG:
            print('s for subscripted assignment:')
            print(s)
            print('<-- Exiting Dmat.setitem() with calling subsasgn(d, s, self)')
        #
        return subsasgn(self, s, d)

    def __add__(self, other):
        """Implement addition with Dmat()
        """
        # Create a copy to avoid to change the original distributed array 
        d = self.copy()
        if isinstance(other,(float,int)):
            # Extract local portion of a distributed array
            # Unnecessary: d.local = local(self)
            # update local array
            d.local = d.local + other
        elif isinstance(other,(Dmat)):
            if (self.map == other.map) and \
                (self.shape == other.shape):
                d.local = self.local + other.local
            else:
                raise Exception('Error (Dmat): both map and array dimension should match for the subtraction.')
        else:
            raise Exception('The type, %s, is not supported for the add operator with Dmat class yet.'%(type(other)))
        return d

    def __sub__(self, other):
        """Implement subtraction with Dmat()
        """
        # Create a copy to avoid to change the original distributed array 
        d = self.copy()
        if isinstance(other,(float,int)):
            # Extract local portion of a distributed array
            d.local = local(self)
            # update local array
            d.local = d.local - other
        elif isinstance(other,(Dmat)):
            if (self.map == other.map) and \
                (self.shape == other.shape):
                d.local = self.local - other.local
            else:
                raise Exception('Error (Dmat): both map and array dimension should match for the subtraction.')
        else:
            raise Exception('The type, %s, is not supported for the subtraction operator with Dmat class yet.'%(type(other)))
        return d

    def __mul__(self, other):
        """Implement multiplication with Dmat()
        """
        if isinstance(other,(float,int,np.float64)):
            # Create a copy to avoid to change the original distributed array 
            d = self.copy()
            # update local array
            d.local = d.local * other
            return d
        elif isinstance(other,(Dmat)):
            if (self.map == other.map) and \
                (self.shape == other.shape):
                # ToDo: Need to implement the multiplicaiton of distributed arrays.
                self.local = self.local * other.local
            else:
                raise Exception('Error (Dmat): both map and array dimension should match for the subtraction.')
        else:
            raise Exception('The type, %s, is not supported for the subtraction operator with Dmat class yet.'%(type(other)))
        return self

    def __rmul__(self, other):
        """Implement multiplication with Dmat()
        """
        if isinstance(other,(float,int,np.float64)):
            # Create a copy to avoid to change the original distributed array 
            d = self.copy()
            # update local array
            d.local = other * d.local 
            return d
        elif isinstance(other,(Dmat)):
            if (self.map == other.map) and \
                (self.shape == other.shape):
                # ToDo: Need to implement the multiplicaiton of distributed arrays.
                d = self.copy()
                d.local = other.local * self.local
                return d
            else:
                raise Exception('Error (Dmat): both map and array dimension should match for the subtraction.')
        else:
            raise Exception('The type, %s, is not supported for the subtraction operator with Dmat class yet.'%(type(other)))
        return self

    def __eq__(self,other):
        """
        == Equal (distributed matrices).
        A==B compares dimensions, maps and data.
        If maps are equal and dimensions agree then the output is a
        distribituted array with 0 where elements are not equal and 1s where
        elements are equal (similarly to serial MATLAB).
        
        If the maps are not equal, then a 0 is returned regardless of any
        other properties. Also, if the dimensions and/or sizes are not equal,
        then an error gets thrown (analogous to serial MATLAB behavior).
        
        Author:   Nadya Travinin
        
        NOTES:
        A possible other approach to the case where the maps are not equal,
        but the data is, is to return a distributed matrix (distributed along
        A's or B's map with 0 and 1 as described above. However, this approach
        would incur sever communication costs, additionally it is not clear
        what the distribution of the output matrix should be. Thus for now,
        this is left as an unimplemented open ended question.
        """
        
        if hasattr(other,'map'):
            if (self.map == other.map): #compare maps
                if (self.dim == other.dim): #compare dimensions
                    if (self.shape == other.shape): #compare shape (a.k.a. size)
                        if self.dim == 2:
                            c = Dmat(self._nbytes, self._dtype, self.shape[0],self.shape[1], map=self.map)
                        elif self.dim == 3:
                            c = Dmat(self._nbytes, self._dtype, self.shape[0], self.shape[1], self.shape[2], map=self.map)
                        elif self.dim == 4:
                            c = Dmat(self._nbytes, self._dtype, self.shape[0], self.shape[1], self.shape[2], self.shape[3], map=self.map)
                        else:
                            print('Dmat/eq: Only distributed arrays of up to 4D are supported')
                            exit(-1)
                        c.local = (self.local == other.local)
                        # Check if c.local is all True
                        if (c.local).any():
                            c = True
                        else:
                            c = False
                    else: #shape not equal
                        print('dmat/eq:Matrix dimensions must agree')
                        c = False
                else: #dimensions not equal
                    print('@dmat/eq:Matrix dimensions must agree')
                    c = False
            else: #maps not equal
                c = False
        else: #is not a Dmat object.
            c = False
        return c

    def subsref(self,s):
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
        DEBUG = 0
        if DEBUG:
            print('--> Entering subsref for Dmat objects')
    
        sizeA = size(self)
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
            if len(subs) > ndims(self):
                raise Exception('@dmat/subsref: Too many dimensions')
            elif len(subs) < ndims(self):
                raise Exception('@dmat/subsref: Too few dimensions')

            #set submat flag to 0
            submat_flag = 0
    
            # check to make sure that the indices before the last are
            # within bounds
            f_all = 1
            for i in range(ndims(self)):
                # In Python, slice(None) is equivalent to using the colon : operator in array slicing.
                # if not isinstance(subs[i],slice) and subs[i].start != None :
                if not isinstance(subs[i],slice) :
                    f_all = 0
                    # if len(subs[i]) != 1:
                    if not isinstance(subs[i],int):
                        #adjust submat flag
                        if DEBUG:
                            print('Dmat.subsref: adjust submat flag = 1')
                        submat_flag = 1
                    elif subs[i] > sizeA[i]: # && i <= ndims(self)
                        raise Exception('@dmat/subsref: Index exceeds dmat dimensions')
    
            if not submat_flag: #if reference consist of combinations of : and single numbers, use this code
                # expand the dimensions if needed
                # TODO doesn't follow Matlab semantics if last specified
                # dimension is : and it needs to be expanded, so it has been
                # disabled for the time being
                #
                #excess = subs{len(subs)}
                #for i=len(subs):ndims(self)
                #  subs[i] = mod(excess-1, sizeA) + 1
                #  excess = floor((excess-1) / sizeA(len(subs))) + 1
                #end
    
                #
                # If all subscripts are :, return the entire matrix otherwise
                # call submatrix.
                #
                if f_all:
                    b = self.copy()
                else:
                    #
                    # Commonly used variables.
                    #
                    m = self.map
                    gridA = m['grid']
                    distA = m['dist_spec']
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
                        # if len(subs[i]) == 1:
                        # Not sure what it means if len(subs[i]) != 1 ?
                        #     if subs[i] != ':':
                        # Onlf access if a direction has a specified index to address ...
                        if not isinstance(subs[i],slice) and isinstance(subs[i],int):
                                if subs[i] < 0 or subs[i] > sizeB[i]-1:
                                    raise Exception('@dmat/subsref: The %d-th subscript exceeds size of dmat'%(i))
    
                                # figure out distribution
                                if distA[i]['dist']=='b':
                                    # block - take the subscript and divide by the block size =
                                    # size(a, i) / size(gridA, i)

                                    if DEBUG:
                                        print(size(self,i))
                                        print(size(gridA,i))
                                    # size() returns a list
                                    b_size = ceil(size(self, i)[0] / size(gridA, i)[0])
                                    idx = floor((subs[i]) / b_size) 
                                    off = subs[i]%b_size
    
                                elif distA[i]['dist']=='c':
                                    # cyclic - find the remainder of the subscript divided by
                                    # the number of processors in that dimension
                                    idx = subs[i]%size(gridA, i)[0]
                                    off = floor(subs[i] / size(gridA, i)[0])
    
                                elif distA[i]['dist']=='bc':
                                    # block cyclic - find out which block this would lie on (block),
                                    # and then find out which processor owns this block (cyclic)
                                    idx = floor(subs[i] / distA[i]['b_size'])
                                    off = distA[i]['b_size'] * floor(idx / size(gridA, i)[0]) + subs[i]%distA[i]['b_size']
                                    idx = idx%size(gridA, i)[0]
    
                                else:
                                    raise Exception('@dmat/subsref: Unsupported distribution type: %s'%(distA.type))
                                #
                                # Set up the subscripts.
                                #
                                s_map['subs'][i] = idx
                                s_data['subs'][i] = off
                                sizeB[i] = 1
                        #    else:
                        elif isinstance(subs[i],slice):
                                s_map['subs'][i] = subs[i]
                                s_data['subs'][i] = subs[i]
                        else:
                            raise Exception('@dmat/subsref: Unsupported subscript: %s'%(subs[i]))
                    #
                    # Find the map that would contain these processors and create a
                    # dmat using this map.
                    #
                    s_map['type'] = '()'
                    s_data['type'] = '()'
                    # find() returns a list
                    # np.where( sizeB != 1)[0] returns a list of indices where its elements is not 1
                    maxGenDim = np.max((np.max(np.where( sizeB != 1)[0]),2))
                    sizeB = sizeB[0:maxGenDim]
                    gridA = gridA.flatten()
                    gridB = exec_subsref(gridA,s_map)

                    # Downsize the distribution specification for the first 2 dimensions
                    m_dist_spec = {key: m['dist_spec'][key] for key in [0,1] if key in m['dist_spec']}
                    # proc_list = np.reshape(gridB, (1, np.prod(size(gridB))))[0]
                    proc_list = np.reshape(gridB, (np.prod(size(gridB)),))
                    if DEBUG:
                       print('Dmat.subsref: check some variables')
                       print('size(gridB) = ',end='')
                       print(size(gridB))
                       print(m_dist_spec)
                       print(proc_list)
                    mapB = Dmap(size(gridB), m_dist_spec, proc_list)
                    b = Dmat(self.nbytes,self.dtype,sizeB, map=mapB)
    
                    #
                    # If local processor has data that needs to be sent, send it.
                    #
                    if DEBUG:
                        print('Dmat.subsref: before exec_subsref(self.local,s_data) call . . . ')
                        print('. . . Check Dmat b with ndims(): ')
                        b.show()
                        print(ndims(b))

                    if np.prod(size(self.local)) > 0 and inmap(mapB, GPC.Pid):
                        # print('. . . calling b.local = exec_subsref(self.local,s_data) ')
                        b.local = exec_subsref(self.local,s_data)
                    if DEBUG:
                        print('... after exec_subsref(self.local,s_data) call . . . ')
                        print('b.local = ',end='') 
                        print(b.local)
                        b.show()
            else: #make a call to submat with a warning
                print(
                    '''Warning:
                    dmat/subsref: Fully functional sibscripted reference
                    is only supported for indices that consist of combinatioons
                    of : and single number. Otherwise, please restrict operation
                    to the local part of the referenced structure. Stand alone
                    distirbuted array will not be returned.
                    ''')
                b = submat(self,s)

            #
            # Structure reference.
            #
        elif stype=='.': #subscripting type
            if subs == 'local':
                b = self.local
            elif subs == 'map':
                b = self.map
            else:
                raise Exception('@dmat/subsref: %s cannot be accessed directly or is not a field of DMAT.'%(subs))
        #
        # Recursive call
        #
        if isinstance(s,list) and len(s) > 1:
            b = exec_subsref(self, s[2:])

        if DEBUG:
            print('<-- Exiting subsref for Dmat objects')
        return b

    def copy(self):
        """Copy the given dmat."""
        d = Dmat(self._nbytes, self._dtype)
        d.map = self.map
        d.dim = self.dim
        d.shape = self.shape
        d.pitfalls = self.pitfalls
        d.falls = self.falls
        d.local_dim = self.local_dim
        d.global_ind = self.global_ind
        # create an array same as d.local
        if (np.iscomplex(self.local)).any():
            d.local = np.vectorize(complex)(np.zeros(self.local.shape),np.zeros(self.local.shape))
        else:
            d.local = np.zeros(self.local.shape)
        d.local[:] = self.local
        return d

    def show(self):
        """
        Show the Dmat properties
        '"""
        print('*** Dmat object')
        self.map.show()
        print('   global Dmat shape: ',end='')
        print(self.shape)
        print('   local array shape: ',end='')
        print(self.local.shape)
        print('   global index: ',end='')
        print(self.global_ind)
        print('   local dimension: ',end='')
        print(self.local_dim)

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

