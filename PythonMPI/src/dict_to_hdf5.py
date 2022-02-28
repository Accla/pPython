import h5py
import numpy as np
import pickle
import sys

"""h5py save() and load() functions

    source: https://codereview.stackexchange.com/questions/120802/recursively-save-python-dictionaries-to-hdf5-files-using-h5py/121308
    Modified to handle general data types

"""
def save_dict_to_hdf5(dic, filename):

    with h5py.File(filename, 'w') as h5file:
        recursively_save_dict_contents_to_group(h5file, '/', dic)

def load_dict_from_hdf5(filename):

    with h5py.File(filename, 'r') as h5file:
        return recursively_load_dict_contents_from_group(h5file, '/')

def recursively_save_dict_contents_to_group( h5file, path, dic):

    # argument type checking
    if not isinstance(dic, dict):
        raise ValueError("must provide a dictionary")        
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    if not isinstance(h5file, h5py._hl.files.File):
        raise ValueError("must be an open h5py file")

    # save items to the hdf5 file
    for key, item in dic.items():
        #print(key,item)
        key = str(key)
        #CB if isinstance(item, list):
        #CB    item = np.array(item)
        #CB    #print(item)
        if not isinstance(key, str):
            raise ValueError("dict keys must be strings to save to hdf5")
        # save strings, numpy.int64, and numpy.float64 types
        if isinstance(item, (np.int64, np.float64, str, float, np.float32, int)):
            #print( 'here' )
            h5file[path + key] = item
            if not h5file[path + key][()] == item:
                raise ValueError('The data representation in the HDF5 file does not match the original dict.')
        # save numpy arrays
        elif isinstance(item, np.ndarray):            
            try:
                h5file[path + key] = item
            except:
                item = np.array(item).astype('|S9')
                h5file[path + key] = item
            if not np.array_equal(h5file[path + key][()], item):
                raise ValueError('The data representation in the HDF5 file does not match the original dict.')
        # save dictionaries
        elif isinstance(item, dict):
            recursively_save_dict_contents_to_group(h5file, path + key + '/', item)
        # other types cannot be saved and will result in an error
        else:
            #print(item)
            #raise ValueError('Cannot save %s type.' % type(item))
            # CB
            # Everything else
            # print('Try to serialixze via pickle.dumps() to save %s type.' % type(item))
            # Serialization using pickle
            sdata = pickle.dumps(item)
            # print('Serialized object size: %d bytes'%sys.getsizeof(sdata))
            # Convert binary into np.asarray
            bdata_np = np.asarray(sdata)
            h5file[path + key] = bdata_np
            if not h5file[path + key][()] == bdata_np:
                raise ValueError('The data representation in the HDF5 file does not match the original dict.')

def recursively_load_dict_contents_from_group( h5file, path): 

    ans = {}
    for key, item in h5file[path].items():
        if isinstance(item, h5py._hl.dataset.Dataset):
            # De-serialize the pickle dumps
            # if type is numpy.bytes_ then, use pickle to de-serialize the object.... [ToDo]
            if isinstance(item[()], (bytes)):
                ans[key] = pickle.loads(item[()])
                # print('+++ pickle loads called to de-serialize the loaded data')
            else:
                ans[key] = item[()]
        elif isinstance(item, h5py._hl.group.Group):
            ans[key] = recursively_load_dict_contents_from_group(h5file, path + key + '/')
    return ans            
