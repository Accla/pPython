import pathlib

def pPython_ver():
    """pPython_ner - Return the current pPython version.
    
    Usage:
    version = pPython_Ver()
    
    location: current location of the pPython library (dtype: string)
    version:  pPython version (dtype: string)
    
    """
    
    location = pathlib.Path().absolute()
    version = '0.8.1'
    
    print('pPython version: %s'%(version))
    print('          Location: %s'%(location))
    
    return version

