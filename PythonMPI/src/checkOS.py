import platform

"""checkOS - identify and set OS identification variables
    
    Windows OS:  ispc = 1
    Mac OS:   ismac = 1
    Linux OS: islinux = 1
    Either Linux or Mac: isunix = 1
    
"""
# Check if one of them is defined
try: ispc
except NameError: ispc = None
if ispc is None:
    isunix=0
    ismac=0
    islinux=0
    ispc=0
    # List of supported OS system names
    listMacSystem = ['Darwin']
    listLinuxSystem = ['Linux']
    listPCSystem = ['Windows']
    
    systemName = platform.system()
    if systemName in listMacSystem:
        ismac = 1
        isunix = 1
    elif systemName in listLinuxSystem:
        islinux = 1
        isunix = 1
    elif systemName in listPCSystem:
        ispc = 1
    else:
        raise Exception('Error in checking OS. Update OS names in _checkOS() with platform.system() output')


