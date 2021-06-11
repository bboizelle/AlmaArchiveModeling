import numpy
import numpy as np


# Simple masking script
def apply_mask(data, mask):
    profile = np.zeros(len(data[:, 0, 0]))

    for i in range(len(profile)):
        profile[i] = np.sum(numpy.multiply(data[i, :, :], mask))

    return profile
