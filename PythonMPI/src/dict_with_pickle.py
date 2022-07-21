#
import pickle

def save_dict_to_pickle(msg, buffer_file):
    """
    Save a dictionary variable with pickle into a file

    """
    # Save all data into a buffer_file.
    with open(buffer_file, 'wb') as handle:
            pickle.dump(msg, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_dict_from_pickle(buffer_file):
    """
    Load a pickled dictionary variable from a file
    """
    # Read all data out of buffer_file.
    with open(buffer_file, 'rb') as handle:
        buf = pickle.load(handle)
    return buf



