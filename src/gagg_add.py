import numpy as np

from D4M.assoc import Assoc
from pygraphblas import Matrix

def gagg_add(m, n, ops):
    """GAGG_ADD(m) does an operation on arrays based on their types and operator definition
 
    GAGG(M, N, Destination, Operator)
       M, N: Data to be gathered
       ops: Operator to be used for the gathering operation   
  
    Author: Dr. Chansup Byun 
    """
    DEBUG = 0
    if DEBUG:
        print('--> Entering gagg_add')
  
    name = type((m))
    if isinstance(m, (type(Assoc('','','')), type(Matrix.sparse(float)))):
        # Associative or GrB class 
        if ops == '+':
            m = m + n
        elif ops == '-':
            m = m - n
        else:
            print('gagg: type, %s, class does not support the operator, %s'%(name,ops))

    elif isinstance(m, (float, np.float64, np.ndarray)):
        # single or double class
        if ops == 'min':
            m = min(m, n)
        elif ops == 'max':
            m = max(m, n)
        elif ops == '+' or ops == 'sum':
            # Numpy standard plus operation between two same-size arrays
            m = m + n
        else:
            print('gagg: type, %s, class does not support the operator, %s'%(name,ops))

    elif isinstance(m, (list)):
        if ops == '+':
            m = m + n
        else:
            print('gagg: type, %s, class does not support the operator, %s'%(name,ops))
    else:
        print('gagg: type, %s, class is not supported'%(name))

    return m

