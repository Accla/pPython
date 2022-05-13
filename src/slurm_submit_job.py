import sys

import checkOS as OS
from exec_shell_cmd import *
from set_remote_cc import *

def slurm_submit_job(grid_config,sched_job_file,py_file,dir_llsc):
    """Submit PythonMPI job to run on LLGrid via Slurm."""  
    
    DEBUG = 0
    
    # Set some strings for special characters.
    # Get single quote character. 
    q = '\''
    qq = '"'

    # Construct the batch submission command
    cmd_chdir = 'cd '+dir_llsc
    cmdstr = 'sbatch'

    # Add additional scheduler options if provided
    if 'sched_options' in grid_config:
        cmdstr = cmdstr+' '+grid_config['sched_options']
    
    # Partition
    cmdstr = cmdstr+' -p '+grid_config['q_name']
    
    # CPU type (if needed)
    if (grid_config['cpu_type'] == 'xeon-e5') or \
    (grid_config['cpu_type'] == 'xeon64c') or \
    (grid_config['cpu_type'] == 'xeon-g6') or \
    (grid_config['cpu_type'] == 'opteron'):
        cmdstr = cmdstr+' -C '+grid_config['cpu_type']
        
    # Job name
    cmdstr = cmdstr+' -J '+py_file
        
    # Array job
    cmdstr = cmdstr+' -a 1-%d'%(grid_config['ntasks'])
        
    # Standard output or Slurm log
    cmdstr = cmdstr+' -o '+dir_llsc+'/PythonMPI/pRUN.log'
        
    # Standard error or Slurm error
    cmdstr = cmdstr+' -e '+dir_llsc+'/PythonMPI/pRUN.err'
        
    # Additional job informaiton
    tmp = sys.version
    version = tmp.split()[0]
    cmdstr = cmdstr+' --comment='+q+'Python:%s,PythonMPI,'%(version)+q
        
    # Construct the final sbatch command
    
    # Submit the job
    remote_cc = set_remote_cc()
    ecmd = ExecShellCmd(remote_cc)
    if DEBUG:
        print('remote_cc: %s'%(remote_cc))
    if remote_cc:
        cmdstr = qq+cmd_chdir+";"+cmdstr+' '+dir_llsc+'/'+sched_job_file+qq
        if DEBUG:
            print(cmdstr)
        ecmd.run(cmdstr)
    else:
        # Not able to execute sbatch command as is.
        # Workaround to make it work on the grid environment
        save_cwd = os.getcwd()
        os.chdir(dir_llsc)
        cmdstr = qq+cmdstr+' '+dir_llsc+'/'+sched_job_file+qq
        if DEBUG:
            print('chdir to %s'%(dir_llsc))
            print(cmdstr)
        ecmd.run('/bin/bash -c '+cmdstr)
        
    output = ecmd.get_output().strip()
    print('\n'+output+'\n')
    if DEBUG:
        errout = ecmd.get_stderr()
        print(errout)

    # Save the job id
    job_id = 0
    if len(output)>0:
        tmp = output.split()
        job_id = tmp[-1]
        cmdstr = 'touch PythonMPI/pid.slurm.%s'%(job_id)
        if remote_cc:
            ecmd.run(cmd_chdir+";"+cmdstr)
        else:
            ecmd.run(cmdstr)
            os.chdir(save_cwd)

    return job_id

