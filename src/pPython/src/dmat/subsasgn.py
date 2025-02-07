from subsasgn_1D import *
from subsasgn_2D import *
from subsasgn_3D import *
from subsasgn_4D import *

def subsasgn(a, ss, b):
    """
    SUBSASGN Subscripted assignment to a distributed object. Called for syntax A[I] = B.
    
    Should not be called directly.
    SUBSASGN(A, S, B) Subscripted assignment of B (right hand side) to A
    (left hand side). A is a DMAT (distributed array). B can be a DMAT or a
    DOUBLE. 
    
    S is a dictionary list of s[0] (level 1), s[1] (level 2) with the fields:
    type -- string containing '()', '{}', or '.' specifying the
            subscript type. s['type'] = '()|{}|.'
    subs -- Cell array or string containing the actual subscripts.
            s['subs'] = {0: 1, 1:dim, 3: 1} or s['subs'] = 'local'
    
    Not relavant to python: Instead of creating a copy of a, write directly to the memory
    allocated for a in the caller's workspace
    
    Author:   Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering subsasgn')

    if len(ss)==1: # subscripting level
        if DEBUG:
            print('   a single level subscripting level')
        s = ss[0]
        if s['type'] == '()': # subscripting type -> parenthesis
            if len(s['subs']) ==1:    # 1-D subscripted assignment
                a = subsasgn_1D(a, s, b)
            elif len(s['subs']) == a.dim:  # number of dimensions of indices must match the number of dimensions of the matrix
                if len(s['subs'])==2:   # 2-D subscripted assignment
                    if DEBUG:
                        print('Calling a = subsasgn_2D(a,s,b)')
                    a = subsasgn_2D(a,s,b)
                elif len(s['subs'])==3: # 3-D subscripted assignment
                    if DEBUG:
                        print('Calling a = subsasgn_3D(a,s,b)')
                    a = subsasgn_3D(a,s,b)
                elif len(s['subs'])==4: # 4-D subscripted assignment
                    a = subsasgn_4D(a,s,b)
                else:
                    raise Exception('DMAT/SUBSASGN: Only objects up to four (4) dimensions are supported.')
                # End of N-D subscripted assignment
            else:
                raise Exception('DMAT/SUBSASGN: The number of index dimensions must match the number of dimensions of the distributed array.')
        elif s['type'] == '.': # subscripting type - members of dmat structure
            if s['subs']=='local':
                a.local=b

    elif len(ss) == 2:       # subscripting level
        if ss[0]['type'] == '.': # subscripting type - members of dmat structure
            if ss[0]['subs'] == 'local':
                #CB: need to figure out what should be set with s[1]['subs']
                a.local[ss[1]['subs']] = b
            else:
                raise Exception('DMAT/SUBSASGN: Incorrect subscripting.')

        else: # subscripting type
            raise Exception('DMAT/SUBSASGN: Incorrect subscripting type.')
        # End subscripting type

    else: # subscripting level > 2
        raise Exception('DMAT/SUBSASGN: Incorrect subscripting level.')
    # End subscripting level
    
    if DEBUG:
        print('<-- Exiting subsasgn')
    
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

