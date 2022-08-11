# import PythonMPI and pPython
import pyMPI_COMM_WORLD as pyMCW

# from pPython import *
from MPI_Init import *
from MPI_Comm_rank import *
from MPI_Comm_size import *

# pPython class
import pPython as GPC

def pPython_init():
    """Initialize Grid Python environment.
    """

    # PythonMPI initialization

    # Initialize PYthonMPI
    MPI_Init()

    # Create communicator. 
    # pyMCW is imported in PythonMPI.py
    # GPC is imported in pPython.py
    GPC.comm = pyMCW.MPI_COMM_WORLD

    # Get size and rank.
    GPC.Np = MPI_Comm_size(GPC.comm)
    GPC.Pid = MPI_Comm_rank(GPC.comm)

    # Set the default leader
    GPC.leader = 0

    # Set the message number and tag
    GPC.tag_num = 0;
    # message tag - MUST be unique for each message
    GPC.tag = 'tag-'+str(GPC.tag_num)

