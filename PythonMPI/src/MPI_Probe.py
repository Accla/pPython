import re
import os
from glob import glob

from pyMPI_Lock_file import *
from pyMPI_Sleep import *
from MPI_Comm_rank import *

def MPI_Probe(source, tag, comm, nargout=2):
    """MPI_Probe  -  Returns a list of all messages waiting to be received.

    Usage:
    ------
    message_rank, numeric_tag, string_tag = MPI_Probe(source, tag, comm)
    
    source: can be an integer or a wildcard '*'.
    tag:    can be an integer or a string, including wildcards.
    comm:   MPI communicator  (dtype: dictionary)
    message_rank: a column-vector of source ranks, which may be empty. (dtype: list?)
    numeric_tag:  a corresponding column-vector of numeric tags (dtype: list?)
                    non-numeric tags are reported as NaN.
    string_tag:   a column-array of strings, both numeric or non-numeric. (dtype: dictionary?)
    
    """

    # Control debugging message
    DEBUG = 0
    if DEBUG:
        print('--> Entering MPI_Probe')
    
    # Create arrays to store rank and tag.
    rank = list()
    message_rank = list()
    numeric_tag = list()
    string_tag = list()

    # 
    # Get processor rank.
    my_rank = MPI_Comm_rank(comm);

    # MPI_Probe is always checking the incoming message either on a central filesystem 
    # or a local filesystem connected to my own rank
    innode = 1
    # ToDo: how to handle if source is a wildcard (*)?
        
    grid_config = comm['grid_config']
    if grid_config['local_fs'] == 1 :
        local_fs  = 1
        tmpdir = comm['tmpdir']
        machines =  comm['machine_db']['machine']
        #CB if not (grid_config['PPYTHON_MANYCORE'].lower() == 'yes'):
        #CB     raise Exception('ERROR(MPI_Probe): no support for using a local filesystem without the manycore optimization')   
    else:
        local_fs  = 0

    # Get lock file names.
    lock_file = pyMPI_Lock_file(source, my_rank, tag, comm, local_fs=local_fs,msg_type='recv',innode=innode)

    if DEBUG:
        print('locak_file: %s'%(lock_file))

    # Get and count the pending messages.
    message_files = glob(lock_file)
    n_files = len(message_files)
    if DEBUG:
        print('Number of incoming messages: %d'%(n_files))

    # Parse out the source rank and tag for each message.
    pattern = r'.*p(\d+)_p\d+_t(.*)_lock.pkl'
    if DEBUG:
        print('MPI_Probe: pattern = %s'%(pattern))

    for message_file in message_files:
        # Extract the rank and and tag character strings.
        if DEBUG:
            print('message file: %s'%(message_file))

        ext_r, ext_t = re.match(pattern,message_file).groups()
        rank.append(ext_r)
        string_tag.append(ext_t)

    # Convert to numeric.
    #
    # Find indices for only numeric tags from the str_tag list
    numericTags = [i for i,x in enumerate(string_tag) if x.isdigit()]
    # Construct corresponding rank and tag lists from the indices
    list_str_tag = [string_tag[ii] for ii in numericTags]
    list_rank = [rank[ii] for ii in numericTags]

    rank_map = map(int,list_rank)
    message_rank = list(rank_map)
    str_map = map(int,list_str_tag)
    numeric_tag = list(str_map)

    # The frequency of calling MPI_Probe is set by the programmer
    # in the code where MPI_Probe is called.

    if DEBUG:
        print('<-- Exiting MPI_Probe')
    
    if nargout == 2:
        return message_rank, numeric_tag
    else:
        return message_rank, numeric_tag, string_tag

