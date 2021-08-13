from vorbin.voronoi_2d_binning import voronoi_2d_binning
import numpy as np
import matplotlib.pyplot as plt


# Bins Voronoi data using vorbin, opens plot
def binning(s_n, data, noise):
    x = np.zeros((len(data), len(data[0])))
    y = np.zeros((len(data[0]), len(data)))
    for i in range(len(x)):
        x[i] = np.arange(len(data[0]))

    for i in range(len(y)):
        y[i] = np.arange(len(data))

    x = x.flatten()
    y = y.flatten('F')
    signal = data.flatten()
    n = np.full(len(x), noise) / 1000

    binNum, xBin, yBin, xBar, yBar, sn, nPixels, scale = voronoi_2d_binning(x, y, signal, n, float(s_n), plot=True,
                                                                            quiet=False)

    # Save data as text file
    np.savetxt('voronoi_binning_output.txt', np.column_stack([x, y, binNum]),
               fmt=b'%10.6f %10.6f %8i')

    plt.tight_layout()
    plt.savefig("VoronoiBinning.png")  # Save figure to local directory
    plt.show()
