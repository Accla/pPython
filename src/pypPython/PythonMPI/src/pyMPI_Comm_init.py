#
# Work in progress: Need to add more elements in MPI_COMM_WORLD
#
import numpy as np
import re
import os

# Define global isunix, ismac, islinux, ispc 
import checkOS as OS
from dict_with_pickle import save_dict_to_pickle
from pyMPI_Comm_settings import *
from pyMPI_Dir_map import *

def pyMPI_Comm_init(n_proc,machines,**argv):
    """pyMPI_Comm_init  -  Creates generic communicator.
    
    Usage:
    ------
    MPI_COMM_WORLD = pyMPI_Comm_init(n_proc,machines)
    
    n_proc:   number of processes assigned to the MPI_COMM_WORLD (dtype: int)
    machines: list of machines assigned to the MPI_COMM_WORLD (dtype: dictionary)
              machines = { 0:'a-19-0', 1:'a-19-1', 2:'a-19-2' }  MachineID:Hosttname 
    
    Python version: Dr. Chansup Byun
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering pyMPI_Comm_init')
        print('machines:')
        print(machines)
        print('----------')

    # Set default machine.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')
        
    # Get number of machines to launch on.
    n_machines = len(machines)
    n_m = max(n_machines,1)

    # Initialize comm.
    MPI_COMM_WORLD = dict()
    MPI_COMM_WORLD['rank'] = -1
    MPI_COMM_WORLD['size'] = int(n_proc)
    MPI_COMM_WORLD['save_message_flag'] = 0
    MPI_COMM_WORLD['group'] = np.arange(0,n_proc,dtype=int)
    MPI_COMM_WORLD['machine_id'] = np.zeros((n_proc,),dtype=int)
    MPI_COMM_WORLD['host_rank'] = 0
    MPI_COMM_WORLD['host_name'] = host
    MPI_COMM_WORLD['machine_db'] = dict()
    
    # Default: EPPAC = 0 (non triples mode job)
    EPPAC = False
    # Added to save grid_config
    MPI_COMM_WORLD['grid_config'] = dict()
    for key in argv:
        if key == 'grid_config':
            MPI_COMM_WORLD['grid_config'] = argv[key]
            # Check if EPPAC (triples mode jobs) is used.
            EPPAC = MPI_COMM_WORLD['grid_config']['EPPAC']
            interactive = MPI_COMM_WORLD['grid_config']['interactive']
            nnode = MPI_COMM_WORLD['grid_config']['nnode']
            if EPPAC:
               nppn = MPI_COMM_WORLD['grid_config']['nppn']
    
    # Initialize machine database.
    machine_db = dict()
    machine_db['n_machine'] = n_m         # Number of machines.
    machine_db['type'] = dict()           # 'unix' or 'mac' or 'pc'.
    machine_db['machine'] = dict()        # Machine names.
    machine_db['dir'] = dict()            # Communication directory.
    machine_db['python_command'] = dict()  # PYthon command.
    machine_db['remote_launch'] = dict()  # Remote launch command.
    machine_db['remote_flags'] = dict()   # Remote launch flags.
    machine_db['n_proc'] = np.zeros((n_m,),dtype=int)    # # processes on this machine.
    machine_db['id_start'] = np.zeros((n_m,),dtype=int)  # Start index.
    machine_db['id_stop'] = np.zeros((n_m,),dtype=int)   # Stop index.
   
    # Start setting up machine OS.
    #

    # Evaluate how many processes per each machine
    if EPPAC:
        # For the triples mode jobs, take care of the node where the interactive process runs
        # The first node on the grid will have one less processes running due to the interactive process
        if interactive:
            if nppn==1:
                # Take care when nppn=1
                for i_machine in range(nnode):
                    machine_db['n_proc'][i_machine] = nppn
            else:
                for i_machine in range(nnode+1):
                    if i_machine == 0:
                        machine_db['n_proc'][i_machine] = 1
                    elif i_machine == 1:
                        machine_db['n_proc'][i_machine] = nppn - 1
                    else:
                        machine_db['n_proc'][i_machine] = nppn
        else:
            for i_machine in range(nnode):
                machine_db['n_proc'][i_machine] = nppn
    else:
        for i_rank in range(n_proc):
            i_machine = i_rank % n_m
            machine_db['n_proc'][i_machine] = machine_db['n_proc'][i_machine] + 1;
            # print('i_rank=%d,machine_db.n_proc=%d'%(i_rank,machine_db['n_proc'][i_rank]))
            # MPI_COMM_WORLD['machine_id'][i_rank] = i_machine

    # Get possibly user settings.
    machine_db_settings = pyMPI_Comm_settings()

    # Pass the python_module_path and python_module_name
    machine_db['python_module_path'] = machine_db_settings['python_module_path']
    machine_db['python_module_name'] = machine_db_settings['python_module_name']

    if 'local_dir_map' in machine_db_settings:
        machine_db['local_dir_map'] = machine_db_settings['local_dir_map']

    if DEBUG:
        if OS.islocal:
            print('Local python: %s'%(machine_db_settings['python_command']))
        else:
            print('LLSC python: %s'%(machine_db_settings['python_command_llsc']))

    # Set default type
    if (OS.ispc):
        default_type = 'pc'
    else:
        default_type = 'unix'

    # Set paths.
    pwd_pc,pwd_linux,pwd_mac,pwd_grid = pyMPI_Dir_map(machine_db,os.getcwd())
    pwd = os.getcwd()
    sep = os.sep

    # Set machine_db values.
    for ii in range(n_m):
        # ii now starts from 0 instead of 1
        machine_db['type'][ii] = default_type;
        # redundant machine_db['machine'][ii] = host;
        machine_db['dir'][ii] = pwd+sep+'PythonMPI'
        # machine_db['python_command'][ii] = machine_db_settings['python_command']
        machine_db['remote_launch'][ii] = machine_db_settings['remote_launch']
        machine_db['remote_flags'][ii]  = machine_db_settings['remote_flags']
       
        # Starting index is zero with python
        if ii == 0:
            machine_db['id_start'][ii] = 0
            machine_db['id_stop' ][ii] = machine_db['id_start'][ii] + machine_db['n_proc'][ii] -1
        else:
            machine_db['id_start'][ii] = machine_db['id_stop'][ii-1] + 1
            machine_db['id_stop' ][ii] = machine_db['id_start'][ii] + machine_db['n_proc'][ii] -1

        id_start = machine_db['id_start'][ii]
        id_stop  = machine_db['id_stop' ][ii]
        if DEBUG:
            print('Machine_id=%d,(Pid beg,end) = (%d,%d)'%(ii,id_start,id_stop))

        # Note that the last index in the colon operator is not used (thus add '+1')
        MPI_COMM_WORLD['machine_id'][id_start:id_stop+1] = ii

        # Check if there is a machines list.
        if (n_machines > 0):
            machine = machines[ii]
            # Check if there is a directory appended.
            dir_sep = re.search(':',machine)
            if (dir_sep):
                machine_db['machine'][ii] = machine[0:dir_sep.start()]
                machine_db['dir'][ii]     = machine[dir_sep.start()+1:]
            else:
                machine_db['machine'][ii] = machine
 
            # Strip out '&' if present.
            amp_sep = re.search('&',machine)
            # remove from string.
            if (amp_sep):
                machine = machine[:amp_sep.start()]+ machine[amp_sep.start()+1:]
                machine_db['machine'][ii] = machine
            
            # Check if same as host. DOES NOT HANDLE host:dir syntax.
            if DEBUG:
                print('machine & host: %s,%s'%(machine,host))
            if re.search(host,machine):
                # Set type to type of host.
                machine_db['type'][ii] = default_type
                machine_db['python_command'][ii] = machine_db_settings['python_command']

                if os.path.exists('/etc/llgrid.id'):
                    machine_db['dir'][ii] = pwd_grid+'/PythonMPI'
                else:
                    if OS.ispc:
                        machine_db['dir'][ii] = pwd_pc+'\PythonMPI'
                    elif OS.islinux:
                        machine_db['dir'][ii] = pwd_linux+'/PythonMPI'
                    else:
                        machine_db['dir'][ii] = pwd_mac+'/PythonMPI'
            else:
                # Use user specified default (probably 'unix').
                machine_db['type'][ii] = machine_db_settings['type']
                # Assuming the remote hosts are LLSC system for now
                machine_db['python_command'][ii] = machine_db_settings['python_command_llsc']
                machine_db['dir'][ii] = pwd_grid+'/PythonMPI'

            if DEBUG:
                print('python command updated: %s'%(machine_db['python_command'][ii]))

            # Check if ':unix' or ':pc' is appended, if so, override type.
            col_sep = re.search(':',machine)
            if (col_sep):
                if DEBUG:
                    print('user provided machine type: %s'%(machine[col_sep.start()+1:]))
                machine_db['type'][ii] = machine[col_sep.start()+1:]
                # remove from string.
                machine = machine[:col_sep.start()]
                machine_db['machine'][ii] = machine

            if machine == host:
                if (amp_sep):
                    MPI_COMM_WORLD['host_rank'] = -1;

    # Add machine_db to communicator.
    MPI_COMM_WORLD['machine_db'] = machine_db
    # MPI_COMM_WORLD['islocal'] = OS.islocal

    if DEBUG:
        print('MPI_COMM_WORLD')
        print(MPI_COMM_WORLD)
    # Write out.
    comm_pkl_file = 'PythonMPI/MPI_COMM_WORLD.pkl'
    save_dict_to_pickle(MPI_COMM_WORLD, comm_pkl_file)   
                   
    if DEBUG:
        print('<-- Exiting pyMPI_Comm_init')
    return MPI_COMM_WORLD

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
