import os
import shutil

def pyMPI_Delete_all():
    """pyMPI_Delete_all  -  Deletes leftover PythtonMPI files.
    
    Usage:
    ------
    pyMPI_Delete_all()
        
    """

    # Delete 'PythonMPI and its contents' at the current working directory
    checkPath = '.'+os.sep+'PythonMPI'
    if os.path.isdir(checkPath):
        shutil.rmtree('PythonMPI')

