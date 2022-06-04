def get_ind_range(a,s):
    """
    GET_IND_RANGE Creates index ranges from a dictionary S with fields:
    type -- string containing '()', '{}', or '.' specifying the subscript type.
    subs -- tuple of slice objects or [ToDo] string containing the actual subscripts.
     s = {'type':'()','subs':{0:(slice()), 1:':'}} 
     
    Return ind as a list object with index ranges of each dimension
    
    Python version: Dr. Chansup Byun
    Author:   Nadya Travinin
    """
    
    ind = []
    if len(s['subs'])==2: # 2-D
        ind.append( s['subs'][0] )
        ind.append( s['subs'][1] )

    elif len(s['subs'])==3: # 3-D
        ind.append( s['subs'][0] )
        ind.append( s['subs'][1] )
        ind.append( s['subs'][2] )

    elif len(s['subs'])==4: # 4-D
        ind.append( s['subs'][0] )
        ind.append( s['subs'][1] )
        ind.append( s['subs'][2] )
        ind.append( s['subs'][3] )

    else:
        print('GET_IND_RANGE: Only up to 4 dimensional objects are supported.')
        exit()
        
    return ind

