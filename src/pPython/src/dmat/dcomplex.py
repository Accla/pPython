import numpy as np

def dcomplex(*argv):
    """Convert each local part of the DMATs, X & y to a new local portion of DMAT with a complex number, x.local + (y.local)j.
    If x & y are not a DMAT, it returns complex(x,y)
 
    Note: complex() is renamed as dcomplex to avoid naming conflicts

    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering dcomplex')

    if len(argv) == 1:
        a = argv[0]
        if hasattr(a,'local'):
            #bad performance: a.local = np.vectorize(complex)(a.local)
            a.local = a.local + 1j*0.
        else:
            #bad performance: a = np.vectorize(complex)(a)
            a = a + 1j*0.
    elif len(argv) == 2:
        a = argv[0]
        b = argv[1]
        if hasattr(a,'local'):
            #bad performance: a.local = np.vectorize(complex)(a.local,b.local)
            a.local = a.local + 1j*b.local
        else:
            #bad performance: a = np.vectorize(complex)(a,b)
            a = a + 1j*b

    if DEBUG:
        print(f"type(a): {type(a)}")
        print('<-- Exiting dcomplex')
    return a

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
