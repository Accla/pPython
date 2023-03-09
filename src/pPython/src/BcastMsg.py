import numpy as np

from MPI_Bcast import *

# pPython class
import pPython as GPC

def BcastMsg(source, tag, *argv):
    """Broadcast message from current process to all other processes.

    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering BcastMsg')

    comm = GPC.comm
    Pid = GPC.Pid

    # BcastMsg add an additional dictionary layer
    # So unpack it before returning the message.

    msg = dict()
    if Pid == source:
        # Send after packing the message into a dictionary
        ii = 0
        if DEBUG:
            print('Length of argv: %d'%(len(argv)))
        for arg in argv:
            if DEBUG:
                print(arg)
            msg[ii] = arg
            ii = ii + 1
   
    [out] = MPI_Bcast(source,tag,comm,msg)

    if DEBUG:
        print('source: %d, tag: %d'%(source,tag))
        print('<-- Exiting BcastMsg')
        
    return list(out.values())

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
