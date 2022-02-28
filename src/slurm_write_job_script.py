def slurm_write_job_script(sched_job_file,py_file,cwd_path):
    """Generate a Slurm job submission script."""
    
    fid = open(sched_job_file,'w')
    
    job_details = '#!/bin/bash\n'
    job_details = job_details+'#\n'
    job_details = job_details+'# Slurm-HPC submit file for PythonMPI job: '
    job_details = job_details+'%s\n\n'%(py_file)
    job_details = job_details+'#\n'

    working_dir = cwd_path+'/PythonMPI'
    job_details = job_details+'/bin/bash %s/Unix_Commands.${SLURM_ARRAY_TASK_ID}.sh\n'%(working_dir)
    
    fid.write(job_details)
    fid.close()

