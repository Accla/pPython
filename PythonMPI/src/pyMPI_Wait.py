import os

from pyMPI_Sleep import *

def pyMPI_Wait(funcname,filename,logical_state):
    """
    Wait until the given file reached the desired status
    funcname: calling function
    filename: name of the file to check
    logical_state: True: -> exits already
                   False -> not exist yet
    """

    # How much the pause time gets increased each iteration
    pause_rate = 0.03
    # Initial pause time
    pause_init = 0.1
    # max iteration
    max_iter = 100

    # Spin on the file until its desired status is reached.
    loop = 0;
    sum = 0;
    pause_time = pause_init
    while os.path.exists(filename) == logical_state :
        # Sleep statement allows cleaner profiling, but adds latency.
        sum += pause_time
        pyMPI_Sleep(pause_time);
        if loop > max_iter:
            print('Loop: %d, total wait time: %f, last pause interval: %f'%(loop,sum,pause_time))
            raise Exception('%s: failed to find the %s file.'%(funcname,filename))
        loop = loop + 1
        pause_time += pause_time * pause_rate
    return

########################################################
# PythonMPI
# Dr. Jeremy Kepner & Dr. Chansup Byun
# MIT Lincoln Laboratory
# kepner@ll.mit.edu & cbyun@ll.mit.edu
########################################################
# Copyright 2023 Massachusetts Institute of Technology
#
# Permission is herby granted, without payment, to copy, modify, display
# and distribute this software and its documentation, if any, for any
# purpose, provided that the above copyright notices and the following
# three paragraphs appear in all copies of this software.  Use of this
# software constitutes acceptance of these terms and conditions.
#
# IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
# THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
#
# THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
# MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.
