from vorbin import voronoi_2d_binning


def binning(s_n, data, noise):
    binNum, xBin, yBin, xBar, yBar, sn, nPixels, scale = voronoi_2d_binning()
