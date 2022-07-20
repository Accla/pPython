def inmap(m, r):
    """Checks if a processor is in the map.
    Takes a map and a processor rank as arguments.
    Returns TRUE if processor is in the map.
            FALSE otherwise.
 
    Author: Nadya Travinin
    Python version: Dr. Chansup Byun
    """
    
    if r in m.proc_list:
        # rank is found in the map
        return True
    else:
        return False

