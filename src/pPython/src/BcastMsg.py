import numpy as np
import sys

from MPI_Bcast import *

# pPython class
import pPython as GPC

def BcastMsg(source, tag, *argv):
    """Broadcast message from current process to all other processes.

    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    DEBUG_TIMING = 0
    if DEBUG or DEBUG_TIMING:
        print('--> Entering BcastMsg')

    comm = GPC.comm
    Pid = GPC.Pid

    # BcastMsg add an additional tuple layer
    # So unpack it before returning the message.
   
    [argv] = MPI_Bcast(source,tag,comm,argv)

    if DEBUG or DEBUG_TIMING:
        if DEBUG: print('source: %d, tag: %d'%(source,tag))
        if DEBUG_TIMING: 
            for arg in argv:
                print('    size of message: %d'%(sys.getsizeof(arg)))
        print('<-- Exiting BcastMsg')
        
    return argv

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
# EXEMPLARY, OR CONSEQUEN
