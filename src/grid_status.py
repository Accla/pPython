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
    cmdstr = 'LLfree -u'
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
        print('Error (grid_status): cpu type, %s, is not found.'%(cpu_type))
        exit()
        
    return total_procs,unclaimed_procs,unclaimed_nodes,\
    cluster_name,grid_scheduler,grid_scheduler_ver

