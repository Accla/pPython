from detect_transport import *
import grid_config as grid

def set_remote_cc():
    """Set the remote connection command. """
    # Remote execution command
    if 'local' == detect_transport():
        return ''
    else:
        return ' '.join([grid.grid_config['remote_launch'],grid.grid_config['remote_flags'],grid.grid_config['remote_host']])

