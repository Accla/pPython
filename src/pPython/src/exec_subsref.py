from ndims import *

"""
A wrapper function to mimick Matlab subsref() used in pPython
Author: Dr. Chansup Byun
Date:   February 7, 025
"""

def exec_subsref(a,subs_ref,*args):
    if hasattr(a,'subsref'):
        """
        subscript reference operation for Dmap or Dmat
        """
        return a.subsref(subs_ref)
    else:
        DEBUG = 0
        if DEBUG:
            print('--> Entering exec_subsref() for arrays.')
        """
        subscript reference operation for arrays/lists
        """
        sr_length = 0
        dims = ndims(a)
        if DEBUG:
           print('Array a.shape = ',end='')
           print(a.shape)
           print('dims = ',end='')
           print(dims)
           print('subs_ref = ',end='')
           print(subs_ref)

        if isinstance(subs_ref,list):
            stype = subs_ref[0]['type']
            subs = subs_ref[0]['subs']
            sr_length = len(subs_ref)
        else:
            stype = subs_ref['type']
            subs = subs_ref['subs']
        #
        # TODO eventually support < cases
        if len(subs) >= dims:
            if len(subs) > dims:
                print('warning [exec_subsref]: Too many dimensions, apply only available dimension for a given array.')
            if dims == 1:
                b = a[subs[0]]
            elif dims == 2:
                # 1-dimension array to mimick Matlab behavior
                if len(a.shape) == 1:
                    b = a[subs[0]]
                else:
                    b = a[subs[0],subs[1]]
            elif dims == 3:
                b = a[subs[0],subs[1],subs[2]]
            elif dims == 4:
                b = a[subs[0],subs[1],subs[2],subs[3]]
            else:
                raise Exception('exec_subsref: Too few dimensions')
                raise Exception('Error [exec_subsref]: array dimension is > 4, not supported.')
        elif len(subs) < dims:
            raise Exception('Error [exec_subsref]: Too few dimensions')
        #
        # Recursive call
        #
        if sr_length > 1:
            b = exec_subsref(a, subs_ref[2:])

        if DEBUG:
            print('<-- Exiting exec_subsref() for arrays.')
        return b

########################################################
# pPython: Parallel Python Programming Tool
# Python extension: Dr. Chansup Byun (cbyun@ll.mit.edu)
# Software Engineer: Ms. Nadya Travinin (nt@ll.mit.edu)
# Architect:      Dr. Jeremy Kepner (kepner@ll.mit.edu)
# MIT Lincoln Laboratory
########################################################
# Copyright (c) 2023, Massachusetts Institute of Technology All rights
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
