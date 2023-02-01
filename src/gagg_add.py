import numpy as np

from D4M.assoc import Assoc
from pygraphblas import Matrix

def gagg_add(m, n, ops):
    """GAGG_ADD(m) does an operation on arrays based on their types and operator definition
 
    GAGG(M, N, Destination, Operator)
       M, N: Data to be gathered
       ops: Operator to be used for the gathering operation   
  
    Author: Dr. Chansup Byun 
    Python version: Dr. Chansup Byun
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
