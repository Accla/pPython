import os

import checkOS as OS

def pyMPI_Comm_settings_local(machine_db_settings):
    """pyMPI_Comm_settings_local  -  Update values in the MPI Communicator setting for local environment.

    Usage:
    ------
    machine_db_settings = pyMPI_Comm_settings(machine_db_settings)
    
    machine_db_settings:   an internal machine database (dtype: dictionary)
    USER:   username (local or remote user depending on where pPYthon job is dispatched to run)

    python_location: python binary to be used on the grid and on local machine
    python_command: python binary with additional option(s) for python
    python_command_llsc: python binary with additional option(s) for python on LLGrid
    python_module_path: module path on LLGrid where anaconda modules are located
    python_module_name: anaconda module name to be used for PythonMPI

    local_dir_map: local paths matching with the LLGrid home directory path
                   for PC, Linux, and Mac OS environment

    """
    DEBUG = 0

    # Grid user (ToDo: need a better way to set the grid username)
    # pick up the local username
    if OS.ispc:
        USER = os.getenv('USERNAME')
    else:
        USER = os.getenv('USER')

    # Set default type of remote machines to 'unix' (for linux and mac OSes) or 'pc'
    machine_db_settings['type'] = 'unix';     # [OK TO CHANGE.]

    python_location_llsc = '/state/partition1/llgrid/pkg/conda/python-ML-2025b-pytorch/bin/python'

    if os.path.exists('/etc/llgrid.id'):
    	# LLSC python location
    	# python_location = '/state/partition1/llgrid/pkg/anaconda/anaconda3-2021b/bin/python'
    	# machine_db_settings['python_module_name'] = 'anaconda/2021b'
    	python_location = '/state/partition1/llgrid/pkg/anaconda/python-ML-2024b/bin/python'
    	machine_db_settings['python_module_path'] = '/etc/environment-modules/modules'
    	machine_db_settings['python_module_name'] = 'conda/Python-ML-2025b-pytorch'

    else:
        # Set location of python on unix systems.
        # Generic location.  
        python_location = 'python';   # [OK TO CHANGE.]

        # If this is a unix system, we can
        # try and guess a better location of python on remote
        # machines.  If wrong, then this needs to be hard coded (see below).
        if OS.islocal:
            if OS.ispc:
                sep = os.sep
                python_location = 'C:'+sep+'ProgramData'+sep+'Anaconda3'+sep+'python.exe'
                machine_db_settings['python_command'] = python_location + ' -u '
            elif OS.islinux:
                python_location = 'python'
                machine_db_settings['python_command'] = python_location + ' -u '
            elif OS.ismac:
                # python_location = '/usr/bin/python'
                # python_location = '/state/partition1/llgrid/pkg/anaconda/anaconda3-2022a/bin/python'
                python_location = '/opt/anaconda3/bin/python'
                machine_db_settings['python_command'] = python_location + ' -u '
            else:
                raise Exception('Error (pyMPI_Comm_settings_local): unsupported OS.')
        else:
            # Assuming running on LLSC
            python_location = 'python'
            machine_db_settings['python_module_path'] = '/etc/environment-modules/modules'
            machine_db_settings['python_module_name'] = 'conda/Python-ML-2025b-pytorch'

    machine_db_settings['python_command'] = python_location + ' -u '
    machine_db_settings['python_command_llsc'] = python_location_llsc + ' -u '

    # local directory mapping. (pc, linux, mac, grid, sgrp_1, sgrp_2, sgrp_3)
    machine_db_settings['local_dir_map'] = ['Z:', '/home/gridsan/'+USER, '/Volumes/'+USER, '/home/gridsan/'+USER, '/home/gridsan/groups', '/data2/groups', '/state/partition1/user/'+USER]

    if DEBUG:
        print(machine_db_settings)
    return machine_db_settings

########################################################
# PythonMPI
# Dr. Jeremy Kepner & Dr. Chansup Byun
# MIT Lincoln Laboratory
# kepner@ll.mit.edu & cbyun@ll.mit.edu
########################################################
# Copyright 2023 Massachusetts Institute of Technology
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
