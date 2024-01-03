import inspect
import os

import checkOS as OS

# Check if $HOME/ppython_conf exists
PYTHON_CONF_LOCAL=os.getenv('HOME')+os.sep+'ppython_conf'
if os.path.exists(PYTHON_CONF_LOCAL):
    import sys
    sys.path.append(PYTHON_CONF_LOCAL)
    from pyMPI_Comm_settings_local import *

def pyMPI_Comm_settings():
    """pyMPI_Comm_settings  -  Function for setting values in the MPI Communicator.

    Usage:
    ------
    machine_db_settings = pyMPI_Comm_settings()
    
    User can copy this script and put it in their path 
    and edit these values to customize the internals PythonMPI.

    machine_db_settings:   an internal machine database (dtype: dictionary)

    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering pyMPI_Comm_settings')

    machine_db_settings = dict()
    
    # Set default type of remote machines to 'unix' (for linux and mac OSes) or 'pc'
    machine_db_settings['type'] = 'unix';     # [OK TO CHANGE.]

    # Set location of python on unix systems.
    # Generic location.  
    python_location = ' python ';   # [OK TO CHANGE.]

    # If this is a unix system, we can
    # try and guess a better location of python on remote
    # machines.  If wrong, then this needs to be hard coded (see below).
    if OS.isunix:
        # python_location = '/usr/bin/python'
        if os.path.exists('/etc/llgrid.id'):
           python_location = '/state/partition1/llgrid/pkg/anaconda/anaconda3-2022a/bin/python'
        else:
           python_location = 'python'
    elif OS.ispc:
        python_location = 'python.exe '

    # Lincoln cluster common.
    # python_location = ' /tools/python/bin/python';
    # Lincoln cluster local.
    # python_location = ' /wulf/local/pythonr13/bin/python';
    # MHPCC local copy.
    # python_location = ' /scratch/tempest/users/kepner/python6/bin/python';

    # Build unix python launch command based. [DON'T CHANGE]
    # machine_db_settings.python_command = [python_location ' -display null -nojvm -nosplash '];
    # -u: unbuffered standard output
    machine_db_settings['python_command'] = python_location + ' -u '
    machine_db_settings['python_module_path'] = '/etc/environment-modules/modules'
    machine_db_settings['python_module_name'] = 'anaconda/2022a'

    # Remote launch command.
    # To use ssh, change ' rsh ' to ' ssh ' in line below.
    machine_db_settings['remote_launch'] = ' ssh ';

    # Remote launch flags.
    machine_db_settings['remote_flags'] = ' -n ';

    # local directory mapping.
    machine_db_settings['local_dir_map'] = ['Z:', '/home/gridsan/ch21778', '/Volumes/ch21778']

    # if there is local update, please update machine_db_settings
    try:
        machine_db_settings = pyMPI_Comm_settings_local(machine_db_settings)
        loc = os.path.abspath(inspect.getfile(pyMPI_Comm_settings_local))
        # print('--> pyMPI_Comm_settings: updated machine_db_settings with a local configuration, %s.'%(loc))
    except:
        raise Exception('pyMPI_Comm_settings: Failed to update the local machine_db_settings.')

    if DEBUG:
        print('<-- Exiting pyMPI_Comm_settings')
    return machine_db_settings

########################################################
# MatlabMPI
# Dr. Jeremy Kepner
# MIT Lincoln Laboratory
# kepner@ll.mit.edu
########################################################
# Copyright 2002 Massachusetts Institute of Technology
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
