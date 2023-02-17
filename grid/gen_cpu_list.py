import numpy as np

def gen_cpu_list(max_cores, ntpc, nppn, OMP_NUM_THREADS):
    """
    Generate physical threads list for taskset with the given number of prcesses per node
    Distribute all the available physical threads to the given processes as evenly as possible
     
    Input:
      max_cores: max number of physical cores on the node 
      ntpc:      number of physical threads per core
      nppn:       umber of Python processes per node
      OMP_NUM_THREADS: number of OpenMP threads (no op at the moment)
      
    Author: Dr. Chansup Byun
    """

    # max_threads: max number of physical threads on the node
    max_threads = max_cores * ntpc

    # Generate all the physical threads list for the given number of processes
    cpulist = dict()
    
    # leaders: Calculate the first core id position (starting from 1)
    if nppn > max_cores:
        print('Warning: the number of processes per node, %d, is grater than the maximum number of cores, %d' %(nppn,max_cores))
        print('*** Oversubscribing the node ***')
        # no futher calculation (no taskset enfored)
        return cpulist

    leaders = np.linspace(start = 0, stop = max_cores, num = nppn+1).astype(int)
    
    for i in range(nppn):
        # print('For the process ID = %d' %(i))
        j1 = leaders[i]
        j2 = leaders[i+1]
        # print('start=%d end=%d' %(j1,j2))
        inum = []
        if ntpc == 1:
            inum += list(np.arange(j1,j2).astype(str))
        elif ntpc == 2:
            inum += list(np.arange(j1,j2).astype(str))
            inum += list(np.arange(j1+max_cores,j2+max_cores).astype(str))
        elif ntpc == 4:
            inum += list(np.arange(j1,j2).astype(str))
            inum += list(np.arange(j1+max_cores,j2+max_cores).astype(str))
            inum += list(np.arange(j1+max_cores*2,j2+max_cores*2).astype(str))
            inum += list(np.arange(j1+max_cores*3,j2+max_cores*3).astype(str))
        else:
            print(' ')
            raise Exception('gen_cpu_list: Number of physical threads per coe, %d, is not supported!'%(ntpc))

        # Get the physical thread ID
        cpulist[i] = inum

    return cpulist

########################################################
# gridMatlab
# Dr. Albert Reuther
# reuther@ll.mit.edu
# MIT Lincoln Laboratory
########################################################
# Copyright 2003-9 Massachusetts Institute of Technology
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
