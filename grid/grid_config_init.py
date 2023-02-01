import inspect
import os
import sys

from grid_config_local import *
import grid_config as grid

def grid_config_init():
    """
    Initialize grid_config with the local environment customization. 
    
    Author: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering grid_cofig_init')
        for p in sys.path: print(p)

    grid_config = grid.grid_config

    try:
        grid_config = grid_config_local(grid_config)
        # local grid_config customization
        loc = os.path.abspath(inspect.getfile(grid_config_local))
        # print('--> grid_config_init: updated grid_config with a local configuration, %s.'%(loc)) 
    except Exception:
        print('Failed to setup local grid_config settings')

    if DEBUG:
        print('<-- Exiting grid_cofig_init')

    return grid_config

########################################################
# pPython: Parallel Python Programming Tool
# Dr. Jeremy Kepner and Dr. Chansup Byun
# (kepner@ll.mit.edu and cbyun@ll.mit.edu)
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
