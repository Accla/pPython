def replace_token(old_str,new_str,old_path):
    """Replace an old token with the new token for a given path."""
    # replace() does not work for some reason
    # dir_linux.replace(old_str,new_str)
    # dir_mac.replace(old_str,new_str)
    new_path = ''
    for i, letter in enumerate(old_path):
        if letter == old_str:
            new_path = new_path+new_str
        else:
            new_path = new_path+letter
    
    return new_path

