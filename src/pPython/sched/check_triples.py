import numpy as np
import os

from get_cpu_info import *

def check_triples(cluster_name,cpu_type,n_proc,grid_config):
    """
    Check whether a job is a triples mode job or not

    Author: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering check_triples')

    # Check environment varialbe to determine using the triples mode for traditional n_proc input
    # Only supported for backgrounded jobs
    PPYTHON_IMPLICIT_EPPAC = os.getenv('PPYTHON_IMPLICIT_EPPAC','')

    # If needed, preprocess triples mode resource request
    # check if n_proc is not an integer but an array of numerals
    if not isinstance(n_proc,(int,np.int64,np.int32)):
        # Triples mode resource request
        if DEBUG:
            print(' ')
            print('Triples mode jobs:')
            print('check_runtime: Turn on the manycore optimization by default unless specified otherwise')
            print(' ')
        [max_slots, default_slots, max_cores, max_threads] = get_cpu_info(cpu_type,cluster_name)
        #
        if len(n_proc) == 2:
            #
            # When n_proc is given as [NNODE, NPPN]
            #
            nnode = n_proc[0]
            nppn  = n_proc[1]
            ntpp = 1
            os.environ['OMP_NUM_THREADS'] = '1'
        elif len(n_proc) == 3:
            #
            # When n_proc = [NODES, NPPN, NTPP]
            #
            nnode = n_proc[0]
            nppn  = n_proc[1]
            ntpp  = n_proc[2]
            os.environ['OMP_NUM_THREADS'] = str(ntpp)
        else:
            raise Exception('check_runtime: not supported input format. Please check your input arguments')
            
        if nppn > max_slots:
            # Overloading compute node by allowing more processes than the number of slots (max_slots)
            # Actual number of physical cores requested is calculated with max_slots
            n_proc_req = nnode * max_slots
        else:
            n_proc_req = nnode * nppn
        
        # Special case: interactive triples mode job with [1,1,NTPP], in order words, n_proc_req = 1
        if grid_config['interactive'] and n_proc_req == 1:
            print('interactive triples mode job with NNODE*NPPN=1')
            grid_config['EPPAC'] = False
            grid_config['IMPLICIT_EPPAC'] = False
            grid_config['grid_job'] = False
            return n_proc_req, grid_config

        # update grid_config for triples mode job
        grid_config['nnode'] = nnode
        grid_config['ntasks'] = nnode
        grid_config['nppn'] = nppn
        grid_config['ntpp'] = ntpp
        grid_config['EPPAC'] = True
        grid_config['IMPLICIT_EPPAC'] = False
        if os.getenv('PPYTHON_PROC_BIND',default='Yes').lower() == 'no':
            grid_config['proc_bind'] = False
        else:
            grid_config['proc_bind'] = True
        #
        # ToDo: should check and limit the total number of threads < max_threads?
        #
        nl = '\n'
        total = nppn * ntpp
        triple_job = 'Your triples mode job ['+str(nnode)+','+str(nppn)+','+str(ntpp)+'] requests '+str(nppn)\
                     +'*'+str(ntpp)+' = '+str(total)  
        if total < max_cores:
            print('\nWarning: Underutilizing the node.\n\n%s < %d threads on the node.\n'%(triple_job,max_cores)+\
                'You may not be using all of the %d cores on the node you requested, which may be sub-optimal.\n'%(max_cores)+\
                'See https://supercloud.mit.edu/faq#triples-warning for more information.\n')
            print()
        elif total > max_cores:
            print('\nWarning: Oversubscribing the node.\n\n%s < %d threads on the node.\n'%(triple_job,max_cores)+\
                'You are launching more threads than the %d cores on the node you requested, which may be sub-optimal.\n'%(max_cores)+\
                'See https://supercloud.mit.edu/faq#triples-warning for more information.\n')
    
    elif len(PPYTHON_IMPLICIT_EPPAC)>0 :
        # If implicitly define EPPAC with the old Np inpu, set nppn with PPYTHON_NP_PER_NODE environment variable
        # Set the default nppn as 24
        nppn = int(os.getenv('PPYTHON_NP_PER_NODE','24'))
        grid_config['nnode'] = int(np.ceil(n_proc / nppn))
        # Should this keep the old style Np?
        # grid_config['ntasks'] = grid_config['nnode']
        grid_config['ntasks'] = n_proc
        grid_config['nppn'] = nppn
        grid_config['ntpp'] = 1

        if os.getenv('PPYTHON_PROC_BIND',default='Yes').lower() == 'no':
            grid_config['proc_bind'] = False
        else:
            grid_config['proc_bind'] = True

        # Inherit old style Np input case
        grid_config['EPPAC'] = False
        grid_config['IMPLICIT_EPPAC'] = True
        n_proc_req = n_proc

    else:
        # nproc is an integer
        # Check if n_proc cores available for the user
        # Exit with an error if not
        #
        grid_config['EPPAC'] = False
        grid_config['IMPLICIT_EPPAC'] = False
        n_proc_req = n_proc

    if DEBUG:
        print('returning grid_config as')
        print(grid_config)
        print('<-- Exiting check_triples')

    return n_proc_req, grid_config

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
