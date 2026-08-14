import numpy as np

#def beamformer_vectors_freq_first(Nsensors, Nbeams, myFreqs,
def beamformer_vectors(Nsensors, Nbeams, myFreqs, focus_range=None, sound_speed=1500.0):
    """
    Python version of the MATLAB Beamformer_vectors function,
    with frequency as the first dimension.

    Inputs
    ------
    Nsensors : int
        Number of array elements.
    Nbeams : int
        Number of azimuth beams (0 to 360 degrees).
    myFreqs : array-like
        Frequencies in Hz (length F).
    focus_range : float, optional
        Focus range in meters. If None, uses far-field (1e10 m).
    sound_speed : float, optional
        Speed of sound (m/s), default 1500 (typical for water).

    Returns
    -------
    v : np.ndarray
        Steering vectors, shape (Nfreqs, Nelements, Naz, Nel),
        where Naz = Nbeams, Nel = number of elevation angles (here 1),
        and Nfreqs = len(myFreqs).
    """

    # Hard-coded parameters, matching MATLAB code
    el = np.array([0.0])                        # elevation angle(s) in degrees
    az = np.linspace(0.0, 360.0, Nbeams)        # azimuth angles in degrees

    freqs = np.asarray(myFreqs, dtype=float)

    # Array geometry (dimensionless positions, as in MATLAB)
    x = np.linspace(-1000.0, 1000.0, Nsensors)
    y = np.zeros_like(x)
    z = np.zeros_like(x)
    numEls = x.size

    numElev = el.size
    numAz = az.size
    numFreqs = freqs.size

    # Focus range for each azimuth
    if focus_range is None:
        # Default to far-field (plane-wave replica)
        focus_range = np.full(numAz, 1e10, dtype=float)
    else:
        # Same focus range for all azimuths
        focus_range = np.full(numAz, float(focus_range), dtype=float)

    # Array element positions: shape (Nelements, 3)
    P_array = np.stack([x, y, z], axis=1)

    # Replicate array positions for each azimuth: shape (Nelements, 3, Naz)
    P_array_matrix = np.repeat(P_array[:, :, np.newaxis], numAz, axis=2)

    # Output steering vector: (Nfreqs, Nelements, Naz, Nel)
    v = np.zeros((numFreqs, numEls, numAz, numElev), dtype=np.complex128)

    az_rad = np.deg2rad(az)
    el_rad = np.deg2rad(el)

    # Loop over elevation (in this code, only one: 0 deg)
    for ielev in range(numElev):
        cos_el = np.cos(el_rad[ielev])
        sin_el = np.sin(el_rad[ielev])

        # Pointing vectors: shape (3, Naz)
        pointing_vectors = np.zeros((3, numAz), dtype=float)
        pointing_vectors[0, :] = np.cos(az_rad) * cos_el
        pointing_vectors[1, :] = np.sin(az_rad) * cos_el
        pointing_vectors[2, :] = sin_el

        # Focus points (meters): each azimuth scaled by its focus_range
        # shape (3, Naz)
        focus_points = pointing_vectors * focus_range[np.newaxis, :]

        # Replicate focus points for each sensor: shape (Nelements, 3, Naz)
        focus_points_matrix = np.repeat(focus_points[np.newaxis, :, :], numEls, axis=0)

        # Range difference to each element relative to phase center
        diff = P_array_matrix - focus_points_matrix  # (Nelements, 3, Naz)
        element_ranges = np.sqrt(np.sum(diff**2, axis=1))  # (Nelements, Naz)

        # Subtract focus_range replicated for each element: (Nelements, Naz)
        delta_range = element_ranges - (np.ones((numEls, 1)) * focus_range[np.newaxis, :])

        # Vectorized over frequency:
        # delta_range: (Nelements, Naz)
        # freqs[:, None, None]: (Nfreqs, 1, 1)
        phase = 2.0 * np.pi * freqs[:, None, None] * delta_range[None, :, :] / sound_speed
        # phase: (Nfreqs, Nelements, Naz)

        v[:, :, :, ielev] = np.exp(1j * phase)

    return v

