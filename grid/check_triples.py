import numpy as np
import os

#from get_cpu_info import *

def check_triples(cluster_name,cpu_type,n_proc,grid_config):
    DEBUG = 0
    # If needed, preprocess triples mode resource request
    # check if n_proc is not an integer but an array of numerals
    if not isinstance(n_proc,(int,np.int64,np.int32)):
        # Triples mode resource request
        if DEBUG:
            print(' ')
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
        
        # update grid_config for triples mode job
        grid_config['nnode'] = nnode
        grid_config['nppn'] = nppn
        grid_config['ntpp'] = ntpp
        grid_config['EPPAC'] = True
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
    
    else:
        # nproc is an integer
        # Check if n_proc cores available for the user
        # Exit with an error if not
        #
        grid_config['EPPAC'] = False
        n_proc_req = n_proc

    return n_proc_req, grid_config

