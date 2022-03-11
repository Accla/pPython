import pathlib

def gridPython_Ver():
    """gridPython_Ver - Return the current gridPython version.
    
    Usage:
    version = gridPython_Ver()
    
    location: current location of the gridPython library (dtype: string)
    version:  gridPython version (dtype: string)
    
    """
    
    location = pathlib.Path().absolute()
    version = '0.2.1'
    
    print('gridPython version: %s'%(version))
    print('          Location: %s'%(location))
    
    return version

