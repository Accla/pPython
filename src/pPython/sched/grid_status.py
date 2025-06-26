import re

from exec_shell_cmd import *
from set_remote_cc import *

def grid_status(cpu_type):
    """Retrieves the status of the grid cluster 
    as specified in grid_config, and returns the unclaimed
    number of processors and the total number of processors 
    currently reporting to the resource manager.
 
    Usage: 
    ------
    total_procs,unclaimed_procs,unclaimed_nodes,cluster_name,\
    grid_scheduler,grid_scheduler_ver = grid_status(cpu_type)
 
    cpu_type: name of the cpu type of interest
    total_procs: total number of cores available (online)
    unclaimed_procs: number of cores not being used currently
    unclaimed_nodes: number of idle nodes
    cluster_name: name of the cluster
    grid_scheduler: scheduler name
    grid_scheduler_ver: scheduler version
    
    Date: Feb 17, 2022
    Author: Dr. Chansup Byun
    
    """

    DEBUG = 0

    total_procs = 0
    unclaimed_procs = 0
    unclaimed_nodes = 0
    cluster_name = ''
    grid_scheduler = ''
    grid_scheduler_ver = ''
    
    # Check for LLGrid system availability (Use the LLGrid command)
    if DEBUG:
        cmdstr = '/home/gridsan/CH21778/LLGrid/Releases/2025-07/usr/local/bin/LLfree --hide-header'
    else:
        cmdstr = 'LLfree --hide-header'
    ecmd = ExecShellCmd(set_remote_cc())
    ecmd.run(cmdstr)
    llsc_status = ecmd.get_output()

    if DEBUG:
        print('Remote execution: %s'%(set_remote_cc()))
        print('Standard output:')
        print(ecmd.get_stdout())
        print('Standard error:')
        print(ecmd.get_stderr())
    
    i_found_cpu_type = 0
    for line in llsc_status.split('\n'):
        # print(line)
        if re.search('LLGrid',line):
            tmp = line.split()
            cluster_name = tmp[1]
            grid_scheduler = tmp[3]
            grid_scheduler_ver = tmp[-1][:-1]
        else:
            if re.search(cpu_type,line,re.IGNORECASE):
                i_found_cpu_type = 1
                tmp = line.split()
                total_procs = 0
                unclaimed_procs = int(tmp[4])
                unclaimed_nodes = int(tmp[6])
                break
                
    if not i_found_cpu_type:
        raise Exception('Error (grid_status): cpu type, %s, is not found.'%(cpu_type))
        
    return total_procs,unclaimed_procs,unclaimed_nodes,\
    cluster_name,grid_scheduler,grid_scheduler_ver

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
