import pathlib

def gridPython_ver():
    """gridPython_ner - Return the current gridPython version.
    
    Usage:
    version = gridPython_Ver()
    
    location: current location of the gridPython library (dtype: string)
    version:  gridPython version (dtype: string)
    
    """
    
    location = pathlib.Path().absolute()
    version = '0.7.0'
    
    print('gridPython version: %s'%(version))
    print('          Location: %s'%(location))
    
    return version

