"""test_remote_exec.py
    Test pPython distributed array function, remote_exec()

    To run, start Pyhton and type:

        pRun('test_disp.py',4,'grid')

    Output will be piped into two files:

        PythonMPI/test_remote_exec.0.out
        . . . 
        PythonMPI/test_remote_exec.3.out

    pPython
    Dr. Chansup Byun
    MIT Lincoln Laboratory
    cbyun@ll.mit.edu
"""
import os
import numpy as np
from timeit import default_timer as timer


# Import gridPython methods.
# pPython class
import pPython as GPC

from exec_shell_cmd import *
from set_remote_cc import *

# extract QA_PARALLEL environment variable
QA_PARALLEL = os.getenv('QA_PARALLEL')
if QA_PARALLEL == '1':
    PARALLEL = 1
else:
    PARALLEL = 0

# Create communicator.
# pPython as GPC in gridPython.py
comm = GPC.comm
Np = GPC.Np
Pid = GPC.Pid

# Print rank.
print('size: %d'%(Np))
print('Pid: %d'%(Pid))

# Create the remote execution command object
ecmd = ExecShellCmd(set_remote_cc())
SLURM_ARRAY_JOB_ID = os.getenv('SLURM_ARRAY_JOB_ID')
print('SLURM_ARRAY_JOB_ID = %s'%(SLURM_ARRAY_JOB_ID))

cmdstr = 'squeue -h -j '+SLURM_ARRAY_JOB_ID+' --format="%15K %15A %N"'
print('Command to run: %s'%(cmdstr))

ecmd.run(cmdstr)
output = ecmd.get_output().strip()
print(output)
#
# Expect multiple lines
#
slurm_nodelist = ''
for line in output.split('\n'):
    print('Line: %s'%(line))
    jobArrayIndex,jobNumber,slurm_node = line.split()
    slurm_nodelist = slurm_nodelist+','+slurm_node

slurm_nodelist = slurm_nodelist[1:] # remove the first char, which is the comma.
cmdstr = 'scontrol     show hostname '+slurm_nodelist
ecmd.run(cmdstr)
output = ecmd.get_output()
print(output)


print(' ')
print(' ')
print('SUCCESS')
print(' ')
print(' ')

"""
 Copyright 2002 Massachusetts Institute of Technology
 
 Permission is herby granted, without payment, to copy, modify, display
 and distribute this software and its documentation, if any, for any
 purpose, provided that the above copyright notices and the following
 three paragraphs appear in all copies of this software.  Use of this
 software constitutes acceptance of these terms and conditions.

 IN NO EVENT SHALL MIT BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
 SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
 THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF MIT HAS BEEN ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
 
 MIT SPECIFICALLY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING,
 BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

 THIS SOFTWARE IS PROVIDED "AS IS," MIT HAS NO OBLIGATION TO PROVIDE
 MAINTENANCE, SUPPORT, UPDATE, ENHANCEMENTS, OR MODIFICATIONS.
"""

