import numpy as np

from local import *
from put_local import *

class GridDmat:
    """Define GridDmat class.
    """

    def __init__(self):
        pass

    def __add__(self, other):
        """Implement addition with Dmat()
        """
        if isinstance(other,(float)):
            # Extract local portion of a distributed array
            d_local = local(self)
            # update local array
            d_local = d_local + other
            # update the distributed array
            self = put_local(self,d_local)
        elif isinstance(other,(GridDmat)):
            if (self.map == other.map) and \
                (self.size == other.size):
                self.local = self.local + other.local
            else:
                print('Error (GridDmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the add operator with GridDmat class yet.'%(type(other)))
            exit()
        return self

    def __sub__(self, other):
        """Implement subtraction with Dmat()
        """
        if isinstance(other,(float)):
            # Extract local portion of a distributed array
            d_local = local(self)
            # update local array
            d_local = d_local - other
            # update the distributed array
            self = put_local(self,d_local)
        elif isinstance(other,(GridDmat)):
            if (self.map == other.map) and \
                (self.size == other.size):
                self.local = self.local - other.local
            else:
                print('Error (GridDmat): both map and array dimension should match for the subtraction.')
                exit()
        else:
            print('The type, %s, is not supported for the subtraction operator with GridDmat class yet.'%(type(other)))
            exit()
        return self

    def __mul__(self, other):
        """Implement multiplication with Dmat()
        """
        if isinstance(other,(float)):
            # Create a copy to avoid to change the original distributed array 
            d = self.copy()
            # update local array
            d.local = d.local * other
            return d
        elif isinstance(other,(GridDmat)):
            if (self.map == other.map) and \
                (self.size == other.size):
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
        if isinstance(other,(float)):
            # Create a copy to avoid to change the original distributed array 
            d = self.copy()
            # update local array
            d.local = other * d.local 
            return d
        elif isinstance(other,(GridDmat)):
            if (self.map == other.map) and \
                (self.size == other.size):
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
        d.size = self.size
        d.pitfalls = self.pitfalls
        d.falls = self.falls
        d.local_dim = self.local_dim
        d.global_ind = self.global_ind
        # create an array same as d.local
        d.local = np.zeros(self.local.shape)
        d.local[:] = self.local
        return d

