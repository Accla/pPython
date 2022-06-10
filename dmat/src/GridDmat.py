import numpy as np

from local import *
from put_local import *
from subsasgn import *

class GridDmat:
    """Define GridDmat class.
    """
    def __init__(self):
        pass

    def __setitem__(self, index, d):
        """Implement __setitem__ with Dmat()
           d: RHS distributed array, GridDmat 
           self: LHS distributed array, GridDmat object, to be set by b 
        """
        # Invoke Python equivalent function similar to a MATLAB subsasgn operator 
        DEBUG = 1
        if DEBUG:
            print('--> Entering GridDmat.setitem() ')
            print('Class GridDmat: see if this is calleb by A[:,:] = B where A and B are GridDmat()')
            print('What is passed as index: ')
            print(index)
        # [:,:] -> (slice(None, None, None), slice(None, None, None))
        print(' ')
        # check the dimension of the distributed array, b
        s = []
        ss = dict()
        if not isinstance(index,tuple): # 1-D distributed array
            print('GridDmat: 1-D assignment, not implemented yet.')
            exit()
        else:
            if len(index)==2: # 2-D distributed array
                if index[0]==slice(None, None, None) and index[1]==slice(None, None, None):
                    ss['type'] = '()'
                    ss['subs'] = dict()
                    ss['subs'][0] = ':'
                    ss['subs'][1] = ':'
                    s.append(ss)
                else:
                    print('GridDmat: 2-D assignment, not implemented this index type yet.')
                    exit()
            elif len(index)==3: # 3-D distributed array
                print('GridDmat: 3-D assignment, nOt implemented yet.')
                exit()
            elif len(index)==4: # 4-D distributed array
                print('GridDmat: 4-D assignment, nOt implemented yet.')
                exit()
            else: # unsupported distributed array dimension
                print('GridDmat: supported distributed dimension.')
                exit()

        # construct s for sub-assignment operations
        if DEBUG:
            print('<-- Exiting GridDmat.setitem() with calling subsasgn(d, s, self)')
        self = subsasgn(self, s, d)


    def __add__(self, other):
        """Implement addition with Dmat()
        """
        # Create a copy to avoid to change the original distributed array 
        d = self.copy()
        if isinstance(other,(float,int)):
            # Extract local portion of a distributed array
            d.local = local(self)
            # update local array
            d.local = d.local + other
        elif isinstance(other,(GridDmat)):
            if (self.map == other.map) and \
                (self.shape == other.shape):
                d.local = self.local + other.local
            else:
                print('Error (GridDmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the add operator with GridDmat class yet.'%(type(other)))
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
        elif isinstance(other,(GridDmat)):
            if (self.map == other.map) and \
                (self.shape == other.shape):
                d.local = self.local - other.local
            else:
                print('Error (GridDmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the subtraction operator with GridDmat class yet.'%(type(other)))
            exit()
        return d

    def __mul__(self, other):
        """Implement multiplication with Dmat()
        """
        if isinstance(other,(float,int)):
            # Create a copy to avoid to change the original distributed array 
            d = self.copy()
            # update local array
            d.local = d.local * other
            return d
        elif isinstance(other,(GridDmat)):
            if (self.map == other.map) and \
                (self.shape == other.shape):
                # ToDo: Need to implement the multiplicaiton of distributed arrays.
                self.local = self.local * other.local
            else:
                print('Error (GridDmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the subtraction operator with GridDmat class yet.'%(type(other)))
            exit()
        return self

    def __rmul__(self, other):
        """Implement multiplication with Dmat()
        """
        if isinstance(other,(float,int)):
            # Create a copy to avoid to change the original distributed array 
            d = self.copy()
            # update local array
            d.local = other * d.local 
            return d
        elif isinstance(other,(GridDmat)):
            if (self.map == other.map) and \
                (self.shape == other.shape):
                # ToDo: Need to implement the multiplicaiton of distributed arrays.
                d = self.copy()
                d.local = other.local * self.local
                return d
            else:
                print('Error (GridDmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the subtraction operator with GridDmat class yet.'%(type(other)))
            exit()
        return self

    def copy(self):
        """Copy the given dmat."""
        d = GridDmat()
        d.map = self.map
        d.dim = self.dim
        d.shape = self.shape
        d.pitfalls = self.pitfalls
        d.falls = self.falls
        d.local_dim = self.local_dim
        d.global_ind = self.global_ind
        # create an array same as d.local
        d.local = np.zeros(self.local.shape)
        d.local[:] = self.local
        return d

