from grid_status import *

def grid_resource_policy(grid_config, n_proc, interactive):
    """
    Determine if there are enough resources to fit the requested job. 

    Author: Dr. Chansup Byun
    """
    
    #
    # Check the available resources (contact the scheduler)
    total_procs,unclaimed_procs,unclaimed_nodes,\
    cluster_name,grid_scheduler,grid_scheduler_ver \
    = grid_status(grid_config['cpu_type'])
    
    requested = n_proc - interactive
    if requested <= unclaimed_procs:
        if grid_config['nnode'] > unclaimed_nodes:
            # Triple mode jobs cannot be launched.
            print('!!! The triple-mode job launch can currently only offer a total of %d idle nodes.'\
            %(unclaimed_nodes))
            raise Exception('!!! Please submit your request with fewer nodes.')
    else:
        # Not enough resources to fit my resource request currently.
        # Exit the process
        # More sophiscated resource policy implementation in gridMatlab ver.
        print('!!! The Grid can currently only offer a total of %d processors.'\
        %(total_procs))
        print('!!! Please submit your request with fewer cores.')
        raise Exception('!!! Please submit your request with fewer nodes.')

    return requested,unclaimed_procs,unclaimed_nodes

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
