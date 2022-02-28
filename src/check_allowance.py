import grid_config as grid
from exec_shell_cmd import *
from set_remote_cc import *

def check_allowance(n_proc,cpu_type):
    """Check whether the requested number of cores exceeds the number of currently allowed cores for the user
    If exceed the allowance, exit with an error message 

    Usage:
    ------
    status = check_allowance(n_proc,cpu_type)
            -1: requested more core than what is allowed
            0: no check or enough cores to meet the requested cores
            
    
    n_proc: requested numbrer of cores
    cpu_type: CPU type of the compute nodes
    status: 
    
    Reference: Slurm command to check the current resource usage
    squeue -h -u $USER -o%u,%c,%f
    USERNAME,1,xeon-p8

    Check the current resource allocation with the Slurm sacctmgr command
    sacctmgr show user ch21778 withassoc where part=manycore format=user,part,grptres%30
          User  Partition                        GrpTRES
    ---------- ---------- ------------------------------
    USERNAME   xeon-p8                         cpu=3072
 
    """
    status = 0
    
    # Create the remote execution command object
    ecmd = ExecShellCmd(set_remote_cc())
    llsc_user = grid.grid_config['remote_user']
    
    # Set the corresponding partition (queue) name 
    if cpu_type == 'xeon-e5' or cpu_type == 'opteron':
        q_name = 'normal'
    elif cpu_type == 'xeon64c':
        q_name = 'manycore'
    elif cpu_type == 'xeon-p8':
        q_name = cpu_type
    
    # Check current resource usage
    # Slurm squeue command to find out the current resource usage for a given user
    cmdstr = ['squeue','-h','-t','r','-p',q_name,'-u',llsc_user,'-o%u,%c,%f']
    cmdstr = ' '.join(cmdstr)
    ecmd.run(cmdstr)
    output = ecmd.get_output()
    sum = 0
    for line in output.splitlines():
        # print(line)
        tmp = line.split(',')
        sum += int(tmp[1])
    # print('Quota in use: %d cores'%(sum))
    
    # Check current resource limit
    # Slurm sacctmgr command to find out the current resource limit for a given user
    cmdstr = ['sacctmgr','-n','show','user',llsc_user,'withassoc','where','part='+q_name,'format=grptres%30']
    cmdstr = ' '.join(cmdstr)
    ecmd.run(cmdstr)
    output = ecmd.get_output()
    if len(output) == 0:
        status = 0
        # no limit enforced
        return status
    else:
        # print(output)
        tmp = output.split('=')
        q_limit = int(tmp[1])
        q_avail = q_limit - sum
        # print('Quota limit: %d cores'%(q_limit))
    
        if q_avail > n_proc:
            # Resource limit can provide the requested resources
            status = 0
        else:
            # Requested resource is more than what is currently available
            status = -1
            print(' ')
            strfmt = '''Error: Currently available cores for your job is %d cores.
But your job requested %d cores.
Please reduce your job size ...'''%(q_avail,n_proc)
            print(strfmt)
            
        return status

