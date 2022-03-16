# import PythonMPI and gridPython
from gridPython import *

def gridPython_init():
    """Initialize Grid Python environment.
    """

    # PythonMPI initialization

    # Initialize MatlabMPI
    MPI_Init()

    # Create communicator. 
    # pyMCW is imported in PythonMPI.py
    # GPC is imported in gridPython.py
    GPC.comm = pyMCW.MPI_COMM_WORLD

    # Get size and rank.
    GPC.comm_size = MPI_Comm_size(GPC.comm)
    GPC.my_rank = MPI_Comm_rank(GPC.comm)

    # Set the default leader
    GPC.leader = 0

    # Set the message number and tag
    GPC.tag_num = 0;
    # message tag - MUST be unique for each message
    GPC.tag = 'tag-'+str(GPC.tag_num)

