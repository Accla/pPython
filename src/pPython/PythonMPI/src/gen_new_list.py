# How to construct a new array to include the source of at the left most place 
# and then the destination 
def gen_new_list(source,dest):
    """
    source: a pPython rank (an integer)
    dest: a PYthon list of destination Pid list
    
    Author: Dr. Chansup Byun
    Date: June 1, 2023
    """
    
    DEBUG = 0

    # Check if source is in the destination
    new_list = []
    new_list.append(source)
    if source not in dest:
        new_list += dest
    else:
        # Append except the source
        for elem in dest:
            if elem not in new_list:
                new_list.append(elem)
    if DEBUG:
        print('New list: ',end='')
        print(new_list)
        
    return new_list

