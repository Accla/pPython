import numpy as np

def put_local(x, x_local):
    """Assigns new data to the local part of the distributed array.
    
    Usage:
    ------
    X = PUT_LOCAL(X, X_LOCAL) 
        X: distributed array
        X_LOCAL: local part of the distributed array, X
        
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering put_local')

    if hasattr(x,'local'):
        if (np.iscomplex(x_local)).any():
            y = np.real(x_local)
            z = np.imag(x_local)
            x.local = np.vectorize(complex)(y,z)
        else:
            x.local[:] = x_local
    else:
        if (np.iscomplex(x_local)).any():
            y = np.real(x_local)
            z = np.imag(x_local)
            x = np.vectorize(complex)(y,z)
        else:
            x = np.zeros(x.shape,x.dtype)
            x[:] = x_local

    if DEBUG:
        print('<-- Exiting put_local')
    return x

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
