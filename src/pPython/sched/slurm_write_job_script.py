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
    job_details = job_details+'# Increase system resources: number of open files, stack size, max. user processes\n'
    job_details = job_details+'# ulimit -n 10240\n'
    job_details = job_details+'# ulimit -s 81920\n'
    job_details = job_details+'# ulimit -u 40000\n'
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
