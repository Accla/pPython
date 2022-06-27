import numpy as np

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

class Dmat:
    """Define Dmat class.
    """
    def __init__(self, *array_sizes, **keywords):
        """Distributed matrix constructor.
        Creates the necessary data structures for the distributed matrix.

        Input:
        array_sizes: array sizes
        keywords:
            'dmap': 1 or distributed map, Dmap object
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
        
        DEBUG = 1
        if DEBUG:
            print('--> Entering Dmat.init')
        #
        m = n = q = r = None
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
            dims.append(array_sizes[0])
            if ndim>1:
                dims.append(array_sizes[1])
            if ndim>2:
                dims.append(array_sizes[2])
            if ndim>3:
                dims.append(array_sizes[3])
        if DEBUG:
            print('Dimension of distributed dmat array: %d'%(len(dims)))
            print(array_sizes)
            print(dims)
    
        if ndim>4:
            print('ERROR(Dmat): array dimension larger than 4-D is not supported')
            exit()
    
        dmap = None
        if 'dmap' in keywords:
            if isinstance(keywords['dmap'], Dmap):
                dmap = keywords['dmap']
            elif isinstance(keywords['dmap'], int):
                dmap = 1
    
        dtype = np.float64
        if 'dtype' in keywords:
            dtype = keywords['dtype']
    
        if not isinstance(dmap,Dmap):
            # Not a distributed array 
            self.local = np.array(dims)
            return
        
        if len(dims) == 1: # DMAT(M, P)
            dims = dims + dims
        
        self.map = dmap
        self.dim = len(dims)
        #obsolete self.size = dims
        self.shape = dims
        if isinstance(dmap,Dmap) and (dmap.dim != len(dims)):
            print('ERROR(Dmat): Map and distributed object dimensions must match')
            exit()
            
        # create a PITFALLS for each dimension
        pitfalls = []
        for i in range(dmap.dim):
            if DEBUG:
                print('Dmat: axis, i = %d'%(i))
                print(dmap.grid.shape[i])
                print(dmap.dist_spec[str(i)])
                print(dims[i])
            if not (dmap.overlap):
                # dmap.grid.shape: tuple of the dim length
                # dmap.dist_spec: a dictionary of dictoary with key in str(dim)
                # print('no overlap')
                pitfalls.append(gen_pitfalls(dmap.grid.shape[i], dmap.dist_spec[str(i)], dims[i]))
            elif dmap.overlap[i]==0:
                # Same as not defined dmap.overlap
                # print('zero overlap')
                pitfalls.append(gen_pitfalls(dmap.grid.shape[i], dmap.dist_spec[str(i)], dims[i]))
            else:
                # non-zero dmap.overlap is defined.
                if DEBUG:
                    print('non-zero overlap')
                    print('dmap.overlap: %d in axis, i = %d'%(dmap.overlap[i],i))
                pitfalls.append(gen_pitfalls(dmap.grid.shape[i], dmap.dist_spec[str(i)], dims[i], dmap.overlap[i]))
        
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
        self.falls = get_local_falls(self.pitfalls, dmap.grid, my_rank)
        if DEBUG:
            print(dmap.grid)
            print(my_rank)
            for i in range(len(self.falls)):
                f = self.falls[i]
                print('grid_mat: FALLS in axis, i = %d'%(i))
                print_falls(f)
            
        # figure out local dimensions (d.local_dim added with pPython)
        local_dim = local_dims(self.falls, self.dim);
        self.local_dim = local_dim
        
        # Allocating memory is the responsibility of map functions
        # (e.g. ones, zeros, rand and sparse)
        # d.local = zeros(local_dim);
        self.local = []
        
        # get the local indices for the current processor
        grid_dims = dmap.grid_spec
        if len(grid_dims)<dmap.dim:
            for i in range(len(grid_dims),dmap.dim+1):
                grid_dims.append(0)
        
        self.global_ind = get_global_ind(self.falls, grid_dims)
        if DEBUG:
            print('--> Exiting Dmat.init')

    def __setitem__(self, index, d):
        """Implement __setitem__ with Dmat()
           d: RHS distributed array, Dmat 
           self: LHS distributed array, Dmat object, to be set by b 
        """
        # Invoke Python equivalent function similar to a MATLAB subsasgn operator 
        DEBUG = 0
        if DEBUG:
            print('--> Entering Dmat.setitem() ')
            print('Class Dmat: see if this is calleb by A[:,:] = B where A and B are Dmat()')
            print('What is passed as index: ')
            print(index)
        # [:,:] -> (slice(None, None, None), slice(None, None, None))
        # check the dimension of the distributed array, b
        s = []
        ss = dict()
        if not isinstance(index,tuple): # 1-D distributed array
            print('Dmat: 1-D assignment, not implemented yet.')
            exit()
        else:
            if len(index)==2: # 2-D distributed array
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
                    print('Dmat: 2-D assignment, not implemented this index type yet.')
                    print('type(index[0]')
                    print(type(index[0]))
                    exit()
            elif len(index)==3: # 3-D distributed array
                print('Dmat: 3-D assignment, nOt implemented yet.')
                exit()
            elif len(index)==4: # 4-D distributed array
                print('Dmat: 4-D assignment, nOt implemented yet.')
                exit()
            else: # unsupported distributed array dimension
                print('Dmat: supported distributed dimension.')
                exit()

        # construct s for sub-assignment operations
        if DEBUG:
            print('<-- Exiting Dmat.setitem() with calling subsasgn(d, s, self)')
        self = subsasgn(self, s, d)


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
                print('Error (Dmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the add operator with Dmat class yet.'%(type(other)))
            exit()
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
                print('Error (Dmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the subtraction operator with Dmat class yet.'%(type(other)))
            exit()
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
                print('Error (Dmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the subtraction operator with Dmat class yet.'%(type(other)))
            exit()
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
                print('Error (Dmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the subtraction operator with Dmat class yet.'%(type(other)))
            exit()
        return self

    def copy(self):
        """Copy the given dmat."""
        d = Dmat()
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

