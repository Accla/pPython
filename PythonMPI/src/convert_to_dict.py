def convert_to_dict(input,host):
    """convert_to_dict - convert a list or a set into a dictionary variable
    
    Usage:
    output = convert_to_dict(input)
    
    input: a list or a set (dtype: list or set or dictionary)
    host:  local machine name (dtype: str)
    output: a dictionary variable (dtype: dictionary)
    
    """
    
    DEBUG = 0
    if DEBUG:
        print('--> Entering convert_to_dict')
        print(input)

    islocal = 0
    output = dict()
    if len(input) == 0:    # empty machines list, running locally
        output = {0:host}
        islocal = 1
        return output,islocal
    
    if type(input) == type(set()) or type(input) == type(list()):
        ii = 0
        for machine in input:
            output[ii] = machine
            ii = ii + 1
        return output,islocal
    elif type(input) == type(dict()):
        ii = 0
        for machine in input:
            output[ii] = machine
            ii = ii + 1
        return output,islocal
    else:
        raise Exception('Error in convert_to_dict(). Input is neither list nor set variable.')

