import sys

import checkOS as OS
from exec_shell_cmd import *
from set_remote_cc import *
from pPython_ver import *

def slurm_submit_job(grid_config,sched_job_file,py_file,dir_llsc):
    """
    Submit PythonMPI job to run on LLGrid via Slurm.
    
    Author: Dr. Chansup Byun
    """  
    
    PPYTHON_DEBUG = os.getenv('PPYTHON_DEBUG')
    if PPYTHON_DEBUG:
        DEBUG = 1
    else:
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
    ntasks = grid_config['ntasks']
    if grid_config['EPPAC']:
        if grid_config['srun']:
            cmdstr = cmdstr+' --exclusive --nodes=%d --ntasks=%d'%(ntasks,ntasks)
        else:
            cmdstr = cmdstr+' --exclusive -a 1-%d'%(ntasks)
    else:
        cmdstr = cmdstr+' -a 1-%d'%(ntasks)
        
    # Standard output or Slurm log
    cmdstr = cmdstr+' -o '+dir_llsc+'/PythonMPI/pRUN.log'
        
    # Standard error or Slurm error
    cmdstr = cmdstr+' -e '+dir_llsc+'/PythonMPI/pRUN.err'
        
    # Additional job informaiton
    tmp = sys.version
    version = tmp.split()[0]
    ppython_ver = pPython_ver(False)
    interactive = grid_config['interactive']
    local_fs = grid_config['local_fs']
    if grid_config['EPPAC']:
        str_eppac = 'EPPAC=1,[%d,%d,%d]'%(grid_config['nnode'],grid_config['nppn'],grid_config['ntpp'])
    else:
        str_eppac = 'EPPAC=0'
    if grid_config['grid_job']:
        grid_job = 1
    else:
        grid_job = 0
    cmdstr = cmdstr+' --comment='+q+'Python:%s,pPython:%s,nTasks=%d,grid_job:%d,isInteractive=%d,isLocalFS=%d,%s'%(version,ppython_ver,ntasks,grid_job,interactive,local_fs,str_eppac)+q
        
    # Construct the final sbatch command
    
    # Submit the job
    remote_cc = set_remote_cc()
    ecmd = ExecShellCmd(remote_cc)
    if DEBUG:
        print('remote_cc: %s'%(remote_cc))
    if remote_cc:
        if grid_config['srun']:
            # Note: change file permission before executing
            ecmd.run(qq+cmd_chdir+";"+'chmod u+x '+sched_job_file+qq)
            # Launch the job using srun as a single job
            cmdstr = qq+cmd_chdir+";"+cmdstr+" --wrap='srun "+dir_llsc+'/'+sched_job_file+"'"+qq
        else: 
            # Launch the job as an array job
            cmdstr = qq+cmd_chdir+";"+cmdstr+' '+dir_llsc+'/'+sched_job_file+qq
        if DEBUG:
            print(cmdstr)
        ecmd.run(cmdstr)
    else:
        # Running on the grid
        # Not able to execute sbatch command as is.
        # Workaround to make it work on the grid environment
        save_cwd = os.getcwd()
        os.chdir(dir_llsc)
        if grid_config['srun']:
            # Note: change file permission before executing
            ecmd.run('chmod u+x '+sched_job_file)
            cmdstr = qq+cmdstr+" --wrap='srun "+dir_llsc+'/'+sched_job_file+"'"+qq
        else:
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
