from vorbin.voronoi_2d_binning import voronoi_2d_binning
import numpy as np


def binning(s_n, data, noise):
    x = np.zeros((len(data), len(data[0])))
    y = np.zeros((len(data[0]), len(data)))
    for i in range(len(x)):
        x[i] = np.arange(1, len(data[0]) + 1)
    for i in range(len(y)):
        y[i] = np.arange(1, len(data) + 1)
    x = x.flatten()
    y = y.flatten('F')
    signal = data.flatten()
    n = np.full(len(x), noise)
    binNum, xBin, yBin, xBar, yBar, sn, nPixels, scale = binNum, xBin, yBin, xBar, yBar, sn, nPixels, scale = voronoi_2d_binning(x, y, signal, n, s_n, cvt=True, pixelsize=None, plot=True, quiet=True, sn_func=None, wvt=True)
