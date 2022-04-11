from local import *
from put_local import *

class GridDmat:
    """Define GridDmat class.
    """

    def __init__(self):
        pass

    def __add__(self, other):
        """Implement addition of Dmat() + Float
        """
        if isinstance(other,(float)):
            # Extract local portion of a distributed array
            d_local = local(self)
            # update local array
            d_local = d_local + other
            # update the distributed array
            self = put_local(self,d_local)
        else:
            print('The type, %s, is not supported for the add operator with GridDmat class yet.'%(type(other)))
            exit()
        return self

    def __sub__(self, other):
        """Implement subtraction of Dmat() - Float
        """
        if isinstance(other,(float)):
            # Extract local portion of a distributed array
            d_local = local(self)
            # update local array
            d_local = d_local - other
            # update the distributed array
            self = put_local(self,d_local)
        else:
            print('The type, %s, is not supported for the subtraction operator with GridDmat class yet.'%(type(other)))
            exit()
        return self

