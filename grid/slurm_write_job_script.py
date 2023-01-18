from exec_shell_cmd import *
from set_remote_cc import *

def slurm_write_job_script(grid_config,sched_job_file,py_file,cwd_path):
    """
    Generate a bare Slurm job submission script to execute the node script.
    PythonMPI/Unix_Commands.sh

    Author: Dr. Chansup Byun
    """
    
    fid = open(sched_job_file,'w')
    
    job_details = '#!/bin/bash\n'
    job_details = job_details+'#\n'
    job_details = job_details+'# Slurm-HPC submit file for PythonMPI job: '
    job_details = job_details+'%s\n\n'%(py_file)
    job_details = job_details+'#\n'

    working_dir = cwd_path+'/PythonMPI'
    if grid_config['srun']:
        job_details = job_details+'export SCRIPT_ID=$(($SLURM_NODEID+1))\n'
        job_details = job_details+'/bin/bash %s/Unix_Commands.${SCRIPT_ID}.sh\n'%(working_dir)
    else:
        job_details = job_details+'/bin/bash %s/Unix_Commands.${SLURM_ARRAY_TASK_ID}.sh\n'%(working_dir)
    
    fid.write(job_details)
    fid.close()

    return
