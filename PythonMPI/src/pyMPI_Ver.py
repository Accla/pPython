import pathlib

def pyMPI_Ver():
    """pyMPI_Ver - Return the current PythonMPI version.
    
    Usage:
    version = pyMPI_Ver()
    
    location: current location of the PythonMPI library (dtype: string)
    version:  PythonMPI version (dtype: string)
    
    """
    
    location = pathlib.Path().absolute()
    version = '0.0.1'
    
    print('PythonMPI version: %s'%(version))
    print('         Location: %s'%(location))
    
    return version

