import numpy
import numpy as np
from matplotlib import pyplot as plt

# Simple masking script
def apply_mask(data, mask):
    profile = np.zeros(len(data[:, 0, 0]))

    for i in range(len(profile)):
        profile[i] = np.sum(numpy.multiply(data[i, :, :], mask))

    return profile


def velocities(naxis3, v, profile, win_str):
    fig, ax = plt.subplots(1, num=win_str + ": Velocity Channel Profile")

    lines = np.ones(naxis3)
    lines[0] = v[1] - v[0]
    for i in range(len(lines) - 1):
        lines[i + 1] = v[i + 1] - v[i]

    # cdelt3 my be pos or neg (don't worry about flipped)
    ax.bar(v, profile * 1000, lines, fill=0, color='white', edgecolor='black')  # Histogram plot
    ax.set_ylabel('Flux Density (mJy)', labelpad=10.0, fontsize=12)
    ax.set_xlabel('Velocity Channel (km/s)', labelpad=10.0, fontsize=12)
    plt.gcf().text(0.85, 0.75, "Velocities (km/s):", fontsize=14)
    plt.subplots_adjust(right=0.8)
    plt.show()

    galaxy_velocity = input("\nGalaxy (average) velocity (c*z): ")
    # Have user click on locations, use pop up box (similar to what has been done earlier, same thing for fitting
    # region lower and upper bounds. Remind user to include wing structure if present

    integrated_flux = profile * v  # in jy km / s, only between the channel ranges they selected
    # sum up integrated flux over the range of channels they have selected (lower to upper bound) ^--
    #    maybe relabelling axis would be easier than converting channels to...? -look into
    # print these units on side of figure- see Box demo for example
    return galaxy_velocity, integrated_flux
