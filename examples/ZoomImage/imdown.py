import numpy as np
from scipy.interpolate import interp2d

from size import *

def imdown(I,res,alpha):
    """
    # IMDOWN Resamples a grayscale image.
    #    DOWNIMG = IMDOWN(I,R,A) Resamples the input
    #    image I using bilinear interpolation using a sampling
    #    lattice with R point samples at A times the original
    #    sample spacing.  Extrapolated values are set to zero.
    """

    #MATLAB: Vq = interp2(V,Xq,Yq) assumes X=1:N and Y=1:M where [M,N]=SIZE(V).
    #Python:
    [npix,npiy] = size(I)
    X = np.array(range(1,npix+1))
    Y = np.array(range(1,npiy+1))
    f = interp2d(X, Y, I.astype(np.float), kind='linear')
   
    # Create the down-sampling lattice.
    x = alpha*(np.array(range(1,res+1))-((res+1)/2))+((res+1)/2)+(npix-res)/2
    y = alpha*(np.array(range(1,res+1))-((res+1)/2))+((res+1)/2)+(npix-res)/2
    [XI,YI] = np.meshgrid(x,y,indexing='xy')

    # Down-sample the input grayscale image.
    # downimg = interp2(im2double(I),XI,YI,'bilinear')
    # downimg = interp2(double(I),XI,YI,'bilinear')
    # downimg = interp2(double(I),XI,YI,'linear')
    downimg = f(x,y)
    downimg[np.argwhere(np.isnan(downimg))] = 0
 
    # print('imdown: downimg.shape')
    # print(downimg.shape)

    return downimg

