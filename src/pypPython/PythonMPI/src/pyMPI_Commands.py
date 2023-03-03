import os

from MPI_Comm_size import *

import checkOS as OS
from pyMPI_Host_rank import *
from pyMPI_Dir_map import *
from gen_commands import *

def pyMPI_Commands(py_file,rank,MPI_COMM_WORLD,**argv):
    """pyMPI_Commands  -  Commands to launch a python script remotely.

    Usage:
    ------
    defscommands, unix_command = pyMPI_Commands(py_file,rank,MPI_COMM_WORLD)
    
    py_file: a python script name (dtype: string)
    rank: a MPI process rank (dtype: int)
    MPI_COMM_WORLD: MPI communicator (dtype: dictionary)
    defscommands: Python commands to be executed by remotely launched Python processes
                  to start coressponding Python MPI processes under the hood.
    unix_command: Command to start PythonMPI script.

    Python version: Dr. Chansup Byun
    """

    DEBUG = 0
    if DEBUG:
        print('--> Entering pyMPI_Commands:')
        print('rank = %d'%(rank))
        print('MPI_COMM_WORLD-machine_id')
        print(MPI_COMM_WORLD['machine_id'])
        print('MPI_COMM_WORLD-machine_db-machine')
        print(MPI_COMM_WORLD['machine_db']['machine'])

    DONE = False
    grid_job = False
    EPPAC = False
    for key in argv:
        if key == 'grid_config':
            grid_config = argv[key]
            grid_job = grid_config['grid_job']
            EPPAC = grid_config['EPPAC']
        elif key == 'start':
            i_rank_start = argv[key]
        elif key == 'stop':
            i_rank_stop = argv[key]

    Np = MPI_Comm_size(MPI_COMM_WORLD)

    # Unix vs. Windows file seperator.
    dir_sep = os.sep;

    # Get host.
    if (OS.isunix):
        host = os.uname()[1]
    elif (OS.ispc):
        host = os.getenv('computername')
        
    # Set some strings for special characters.
    qq = '"'
    sp = ' '
    nl = '\n'
    # Get single quote character. 
    q = '\''

    # Get info on the target machine.
    machine_id = MPI_COMM_WORLD['machine_id'][rank]
    if EPPAC and (grid_config['interactive']) and (grid_config['nppn'] == 1) and rank > 0:
        machine_id = machine_id-1
    machine = MPI_COMM_WORLD['machine_db']['machine'][machine_id]
    remote_launch = MPI_COMM_WORLD['machine_db']['remote_launch'][machine_id]
    remote_flags = MPI_COMM_WORLD['machine_db']['remote_flags'][machine_id]
    python_base  = MPI_COMM_WORLD['machine_db']['python_command'][machine_id]
    type = MPI_COMM_WORLD['machine_db']['type'][machine_id]

    # Create filename each Python job will run at startup.
    if EPPAC:
       defsbase = 'PythonMPI/PythonMPIdefs'
    else:
       defsbase = 'PythonMPI/PythonMPIdefs' + str(rank)
    defsfile = defsbase + '.py'

    # Replace my_script_file with py_file basename (withoutt .py)
    if EPPAC:
       outfile = '$OUTPUT_DIR/' + py_file + '.' + str(rank) +'.out'
    else:
       outfile = 'PythonMPI/' + py_file + '.' + str(rank) +'.out'
    # Store redirected errors from MPI processes
    errfile = 'PythonMPI/pRUN.err'

    # Create Python MPI setup commands.
    # Find the location for PythonMPI modules
    python_mpi_path = os.getenv("PYTHONMPI_PATH")
    if not python_mpi_path:
        raise Exception('pyMPI_Commands: PYTHONMPI_PATH is not set to find PythonMPI modules')
    
    # Generate a series of commands to be executed to setup pPython runtime 
    # for each Python MPI process
    # the commands are stored in a dictionary
    commands = gen_commands(py_file,python_mpi_path,rank,machine,MPI_COMM_WORLD,EPPAC)

    defscommands = '';

    # Print name of the target machine we are launching on.
    # CB: Reduce the output when Np > 16
    if EPPAC:
       # nnode = grid_config['nnode']
       # Use the following to deal with an interactive triples mode job with nppn=1
       nnode = grid_config['ntasks']
       if (nnode>=8):
           if ((machine_id > (nnode-3)) or (nnode < 2)) and (rank == i_rank_stop):
               print('Launching MPI rank: %d to %d on %s.' %(i_rank_stop,i_rank_start,machine))
           elif (machine_id==(nnode-3)):
               print('Continuing to launch MPI processes ......')
       else:
           if (rank == i_rank_stop):
               print('Launching MPI rank: %d to %d on %s.' %(i_rank_stop,i_rank_start,machine))
    else:
        if (Np>=16):
            if (rank > (Np-3)) or (rank < 2):
                print('Launching MPI rank: %d on %s.' %(rank,machine))
            elif (rank==(Np-3)):
                print('Continuing to launch MPI processes ......')
        else:
            print('Launching MPI rank: %d on %s.' %(rank,machine))

    # Create base python command.
    python_command = python_base+' '+defsfile+' &> '+outfile

    # Determine how to run script and where to send output.
    if DEBUG:
        print('Launch from %s to machine, %s'%(host,machine))
    if machine == host: # Target is host.
        # Check if running with host& set.
        if ((rank == 0) and (pyMPI_Host_rank(MPI_COMM_WORLD) == 0)):
            # Run defsfile scipt interactively.
            defscommands = commands[0]+commands[1]+commands[2]+commands[3]+commands[5]
            unix_command = '';
            defscommands = defscommands

        else:
            # Write commands to a .py text file.
            if EPPAC:
                # Write only once when the triples mdoe job is launched
               if not DONE:
                  fid = open(defsfile,'w')
                  n_command = len(commands)
                  for k,v in commands.items():
                      #print('k,v: %d, %s'%(k,v))
                      fid.write(v)
                  fid.close()
                  DONE = True
            else:
               # Non-triples mode jobs. Each MPI process has its own defsfile
               fid = open(defsfile,'w')
               n_command = len(commands)
               for k,v in commands.items():
                   #print('k,v: %d, %s'%(k,v))
                   fid.write(v)
               fid.close()

            # Create command to run defsfile locally and pipe output to another file.
            if type == 'pc':
                # Target is a pc.
                # PC equivalent to touch is 'copy nul filename.txt'
                python_command = python_base+' '+defsfile+' > '+outfile
                unix_command = 'start /b '+python_command+nl+'copy nul PythonMPI\pid.'+machine+'.pc'+nl 
            else:
                # Forward standard error output to the log and err file on Unix environment
                if EPPAC:
                    FORWARD_ERR = ' 2> >(awk '+q+'BEGIN{FS="\\n"}{print "Pid=" ENVIRON["MPI_COMM_WORLD_RANK"] ": " $1}'+q+' |tee -a '+errfile+' >&2)'
                else:
                    FORWARD_ERR = ' 2> >(awk '+q+'BEGIN{FS="\\n"}{print "Pid='+str(rank)+': " $1}'+q+' |tee -a '+errfile+' >&2)'
                unix_command = python_command+FORWARD_ERR+' &'+nl+'touch PythonMPI/pid.'+machine+'.$!'+nl
    else:
        # Target is a remote machine.
        # Write commands to a .py text file.
        if EPPAC:
           if not DONE:
               fid = open(defsfile,'w')
               n_command = len(commands)
               for k,v in commands.items():
                   #print('k,v: %d, %s'%(k,v))
                   fid.write(v)
               fid.close()
               DONE = True
        else:
            fid = open(defsfile,'w');
            n_command = len(commands)
            for k,v in commands.items():
                # if DEBUG:
                #     print('k,v: %d, %s'%(k,v))
                fid.write(v)
            fid.close()

        # Create command to run defsfile locally and pipe output to another file.
        if type == 'pc':
            if DEBUG:
                print('-> Remote machine is a pc')
            # Remote machine is a pc.
            # PC equivalent to touch is 'copy nul filename.tx&t'
            python_command = python_base+' '+defsfile+' > '+outfile
            unix_command = 'start /b '+python_command+nl+'copy nul PythonMPI\pid.'+machine+'.pc'+nl 
        else:
            if DEBUG:
                print('-> Remote machine is NOT a pc')
            if grid_job and rank>0:
                python_command = 'python '+defsfile+' &> '+outfile
            # Forward standard error output to the log and err file on Unix environment
            if EPPAC:
                FORWARD_ERR = ' 2> >(awk '+q+'BEGIN{FS="\\n"}{print "Pid=" ENVIRON["MPI_COMM_WORLD_RANK"] ": " $1}'+q+' |tee -a '+errfile+' >&2)'
            else:
                FORWARD_ERR = ' 2> >(awk '+q+'BEGIN{FS="\\n"}{print "Pid='+str(rank)+': " $1}'+q+' |tee -a '+errfile+' >&2)'
            unix_command = python_command+FORWARD_ERR+' &'+nl+'touch PythonMPI/pid.'+machine+'.$!'+nl
    if EPPAC:
        # prepend to export MPI_COMM_WORLD_RANK=<mpi_rank>
        unix_command = 'export MPI_COMM_WORLD_RANK='+str(rank)+nl+ \
                       '$TASKSET_CMD '+unix_command

    if DEBUG:
        print('unix_command: %s'%(unix_command))
        print('<-- Exiting pyMPI_Commands:')
    return defscommands, unix_command

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
