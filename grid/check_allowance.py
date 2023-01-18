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
    DEBUG = 0
    if DEBUG:
        print('--> Entering check_allowance')

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
        if DEBUG:
            print('squeue output:')
            print(line)
        tmp = line.split(',')
        sum += int(tmp[1])
    # print('Quota in use: %d cores'%(sum))
    
    # Check current resource limit
    # Slurm sacctmgr command to find out the current resource limit for a given user
    cmdstr = ['sacctmgr','-n','show','user',llsc_user,'withassoc','where','part='+q_name,'format=grptres%30']
    cmdstr = ' '.join(cmdstr)
    ecmd.run(cmdstr)
    output = ecmd.get_output()
    if len(output) == 0 or output.isspace():
        # output is blank if sacctmgr command is disabled for general users
        status = 0
        # no limit enforced
        return status
    else:
        if DEBUG:
            print('sacctmgr output:')
            print(output)
        tmp = output.split(',')
        cpu_q_limit = 0
        mem_q_limit = '0T'
        for arg in tmp:
            tmp2 = arg.strip().split('=')
            if tmp2[0] == 'cpu':
                cpu_q_limit = int(tmp2[1])
            elif tmp2[0] == 'mem':
                mem_q_limit = tmp2[1]
        cpu_q_avail = cpu_q_limit - sum
        # print('Quota limit: %d cores'%(cpu_q_limit))
    
        if isinstance(n_proc,list):
            n_proc_num = n_proc[0]*n_proc[1]
        elif isinstance(n_proc,int):
            n_proc_num = n_proc
        else:
            print('ERROR(check_allowance): n_proc must be either interger or list')
            exit()

        if cpu_q_avail > n_proc_num:
            # Resource limit can provide the requested resources
            status = 0
        else:
            # Requested resource is more than what is currently available
            # Check if the job is a bachgrounded triples mode job and
            # if it is, instead of rejecting the job, submit the job as a batch job
            # with Slurm srun command
            # 
            if (grid.grid_config['interactive']==0) and grid.grid_config['grid_job']:
                status = 0
                grid.grid_config['srun'] = True
                print(' ')
                strfmt = '''Note: Currently available cores for your job is %d cores.
But your job requested %d cores.
Therefor, you job has been submitted as a batch job and it will be executed when the resources become available.'''%( q_avail,n_proc)
                print(strfmt)
            else:
                status = -1
                grid.grid_config['srun'] = False
                print(' ')
                strfmt = '''Error: Currently available cores for your job is %d cores.
But your job requested %d cores.
Please reduce your job size ...'''%(q_avail,n_proc)
                print(strfmt)
            
        # Debug run for the srun job launch
        # status = 0
        # grid.grid_config['srun'] = True

        return status

