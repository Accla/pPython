def pyMPI_Save_messages(old_comm,save_message_flag):
    """pyMPI_Save_messages  -  Toggles deleting or saving messages.

    Usage:
    ------
    new_comm = pyMPI_Save_messages(old_comm,save_message_flag)

    PythonMPI helper function for setting the fate of messsages.
    save_message_flag = 1 (save messages).
    save_message_flag = 0 (delete messages: default).
    
    """

    new_comm = old_comm
    new_comm['save_message_flag'] = save_message_flag

    return new_comm

