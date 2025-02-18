import numpy as np
from numpy import cos,sin,pi,ones

# import pPython functions
from zeros import *
from ones import *
from sin import *
from cos import *

class Params:
    """
    To hold some code parameters:
    params.az = azimuth angles (deg), 0 = fwde       (1xM)
    params.el = D/E angle (deg) 0= horizontal bea   (1xL)
    params.arrayGeom = structure containing array element (x,y,z) location
    params.freqs = vector of frequencies (Hz)        (1xF)
    params.soundSpeed = speed of sound (m/sec)
    """
    pass

def beamformer_vectors(Nsensors,Nbeams,myFreqs):
    """
    beamformer_vectors - routine to return broadband 3D focused single-path replica vector
    
    Input:       
    params.az = azimuth angles (deg), 0 = fwde       (1xM)
    params.el = D/E angle (deg) 0= horizontal bea   (1xL)
    params.arrayGeom = structure containing array element (x,y,z) location
    params.freqs = vector of frequencies (Hz)        (1xF)
    params.soundSpeed = speed of sound (m/sec)
    focus_range = focus range (m) (OPTIONAL)         (1x1)
                  defaults to a very large number to get plane-wave replica
    Output:     
    v = steering vector (Nelements x M x L x F)
    """
    DEBUG = 1
    if DEBUG:
        print('--> Entering beamformer_vectors')
      
    # Hard some code parameters.
    params = Params()
    params.el = np.array([0])
    params.az = np.linspace(0, 360, Nbeams)

    # frequencies and array positions are dimensionless.
    params.freqs=myFreqs
    params.arrayGeom = Params()
    params.arrayGeom.x = np.linspace(-1000,1000,Nsensors)
    vec_length = len(params.arrayGeom.x)
    if DEBUG:
        print(params.arrayGeom.x.shape)
    params.arrayGeom.y = zeros(vec_length)
    params.arrayGeom.z = zeros(vec_length)
    params.numEls = len(params.arrayGeom.x)
    
    params.soundSpeed=1500
    
    # get dimensions
    numElev = len(params.el)
    numAz = len(params.az)
    numFreqs = len(params.freqs)
    if DEBUG:
        print('numFreqs = %d'%(numFreqs))
    
    # set so all azimuths have the same focus range
    if(hasattr(params, 'focus_range')):
        focus_range = params.focus_range*ones(1,numAz)
    else:
        # default to far-field
        focus_range = 1e10*ones(1,numAz)

    # shoehorn rr structure into P_array.
    P_array = np.concatenate((params.arrayGeom.x,params.arrayGeom.y,params.arrayGeom.z)).reshape((-1, 3), order='F')
    P_array_matrix=np.broadcast_to(P_array, (numAz, *P_array.shape))  
    # Note that the index order in P_array_matrix has changes as
    # MATLAB: (:,:,1) -> Python: [0,:,:]
    #
    # Should do np.swapaxes() twice to make it conpatible with the Matlab results? Yes, it's needed later for subtraction ops
    if DEBUG:
        print('Swap between axes 0 and 1 first. Then, swap between axes 1 and 2.')
    P_array_matrix = np.swapaxes(P_array_matrix,0,1)
    P_array_matrix = np.swapaxes(P_array_matrix,1,2)
    if DEBUG:
        for i in range(P_array_matrix.shape[2]):
            print('P_array_matrix[:,:,%d]'%(i))
            print(P_array_matrix[:,:,i])

    #CB: v is an array of complex numbers. So allocate memory accordingly
    v = zeros(params.numEls,numAz,numElev,numFreqs)
    v = np.vectorize(complex)(v,v)
    if DEBUG:
        print('v.shape')
        print(v.shape)

    pointing_vectors = np.zeros((3,numAz))
    for ielev in range(numElev):
        # Define the vector that points at this azimuth and elevation
        # from the array phase center
        pointing_vectors[0,:] = cos(params.az*pi/180)*cos(params.el[ielev]*pi/180)
        pointing_vectors[1,:] = sin(params.az*pi/180)*cos(params.el[ielev]*pi/180)
        pointing_vectors[2,:] = ones(1,numAz)*sin(params.el[ielev]*pi/180)
    
        # Compute the actual focus point (meters)
        focus_points = np.dot(pointing_vectors,np.diag(focus_range[0]))
        """
        if DEBUG:
            print('focus_points')
            print(focus_points)
            print('pointing_vectors')
            print(pointing_vectors)
        """

    
        # Compute the difference in range to each element in the array with
        # respect to the array phase center
        focus_points_matrix = np.reshape(np.kron(focus_points,ones(params.numEls,1)),(params.numEls,3,numAz),'F')
        """
        if DEBUG:
            print('np.kron(focus_points,ones(params.numEls,1))')
            print(np.kron(focus_points,ones(params.numEls,1)))
            
            print('focus_points_matrix.shape')
            print(focus_points_matrix.shape)
            # print(focus_points_matrix)
            for i in range(focus_points_matrix.shape[2]):
                print('focus_points_matrix[:,:,%d]'%(i))
                print(focus_points_matrix[:,:,i])
        """
    
        delta_range = np.sqrt(np.squeeze(np.sum((P_array_matrix - focus_points_matrix)**2,1))) - ones(params.numEls,1)*focus_range

        if DEBUG:
            print('delta_range')
            print(delta_range)

    
        # Compute the true array response vectors to the source
        # (azimuth,elevation,focus range)
    
        for ifrq in range(numFreqs):
            freq = params.freqs[ifrq]
            v[:,:,ielev,ifrq] = np.exp(1.0j*2*pi*delta_range*freq/params.soundSpeed)
            """
            if DEBUG: 
                print('ifrq = %d'%(ifrq))
                print('1.0j*2*pi*delta_range*freq/params.soundSpeed')
                print(1.0j*2*pi*delta_range*freq/params.soundSpeed)
            """
    
    if DEBUG:
        print('<-- Exiting beamformer_vectors')

    return v


