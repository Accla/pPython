import inspect
import os
import sys

from grid_config_local import *
import grid_config as grid

def grid_config_init():
    """Initialize grid_config with the local environment customization. """

    DEBUG = 0
    if DEBUG:
        print('--> Entering grid_cofig_init')
        for p in sys.path: print(p)

    grid_config = grid.grid_config

    try:
        grid_config = grid_config_local(grid_config)
        # local grid_config customization
        loc = os.path.abspath(inspect.getfile(grid_config_local))
        # print('--> grid_config_init: updated grid_config with a local configuration, %s.'%(loc)) 
    except Exception:
        print('Failed to setup local grid_config settings')

    if DEBUG:
        print('<-- Exiting grid_cofig_init')

    return grid_config

