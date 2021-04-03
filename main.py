import math
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from prompt import call
import tkinter as tk

MAX_ATTEMPTS = 5
attempts = 1
coords = [1, 0]
bl = [1, 0]
ur = [1, 0]
i = 0
userStr = ""


def main():
    plt.style.use(astropy_mpl_style)

    fits_file = None

    # print working directory
    print("\nCurrent path is: ")
    cwd = os.getcwd()
    print(cwd)

    # list all .fits files in cwd
    print("\nFITS files are: ")
    for file in os.listdir(cwd):
        if file.endswith(".fits"):
            print(file)

    # verify file name
    userStr = input("\nIs your file in the path (y/n): ")
    if userStr == 'y':
        userStr = input(
            "\nEnter full ALMA file name (*.fits): ")  # copy this for use during testing
        # "NGC315_CO21_C5_bri_10kms.pbcor.fits"
        fits_file = userStr

    # Reads in original fits image dimensions
    hdul = fits.open(fits_file)
    x = hdul[0].header['NAXIS1']
    y = hdul[0].header['NAXIS2']
    small_x = 0
    big_x = x
    small_y = 0
    big_y = y
    xy = str(x) + '/' + str(y)
    print("\nSpatial (x,y) dimensions:", xy, "pixels")
    print("Spectral (z) dimension:", str(hdul[0].header['NAXIS3']), "channels")

    # ask user if they want to use subregion
    userStr = input("\nUse a subregion of the full spatial (x,y) dimensions? (y/n): ")
    if userStr == 'y':
        small_x = input("Left x-value (integer, e.g., 100): ")
        big_x = input("Right x-value (integer, e.g., 500): ")
        small_y = input("Lower y-value (integer, e.g., 100): ")
        big_y = input("Upper y-value (integer, e.g., 500: ")
        int(big_x) - int(small_x)  # Can return x when needed
        int(big_y) - int(small_y)  # Can return y when needed

    # ask user if they want to undersample spacial dimensions
    userStr = input("\nUndersample the spacial (x,y) dimensions? (y/n): ")
    if userStr == 'y':
        userStr = 'y'  # FIXME later

    # trim unnecessary channels
    c_speed = 299792.458
    channel = abs((hdul[0].header['CDELT3'] / hdul[0].header['RESTFRQ']) * c_speed)
    channel = round(channel, 2)
    print("\nCurrent velocity channel binning is", channel, "km/s")
    print("Channels over which line is")
    print("observed in the ORIGINAL data cube:")
    input("z1 (lowest) channel value: ")  # Will return z1 when needed
    input("z2 (highest) channel value: ")  # Will return z2 when needed

    # ask user if they want to undersample frequency
    userStr = input("\nUndersample the frequency (z) dimension? (y/n): ")
    if userStr == 'y':
        userStr = 'y'  # FIXME later

    # get target name
    targ_name = input("Enter target name (e.g., NGC 1332): ")

    # get molecular transition
    molecular_trans = input("\nEnter molecular transition name (e.g., CO21 for CO(2-1)): ")

    # allow user to subtract continuum if necessary
    userStr = input("\nNeed to subtract the continuum? (y/n): ")
    if userStr == 'y':
        userStr = 'y'  # FIXME later

    # check if user is square
    userStr = input("\nAllow for unequal dimensions? (e.g., a wide mosaic- y/n): ")
    if userStr == 'y':
        userStr = 'y'  # FIXME later

    # Function that receives click events and returns valid coordinate pairs
    def onclick(event):
        ix, iy = event.xdata, event.ydata
        if (ix is not None) and (ix > 1) and (iy > 1):
            global i
            global bl
            global ur
            global attempts
            attempts = attempts
            if i == 1:
                rect = patches.Rectangle((bl[0], bl[1]), (ix - bl[0]), (iy - bl[1]), linewidth=attempts,
                                         edgecolor='r', facecolor="none")
                ax.add_patch(rect)
                plt.draw_all()
                plt.pause(0.001)
                i = 2
            global coords
            coords = [ix, iy]
            global userStr
            global MAX_ATTEMPTS
            if i == 0:
                bl = coords
                print("Choose top-right location (click): ")
            if i == 2:
                ur = coords
                global userStr
                # display yes/no prompt with Tkinter
                root = tk.Tk()
                root.withdraw()
                userStr = call()
                root.destroy()
                if userStr == "y":
                    fig.canvas.mpl_disconnect(cid)
                    plt.close()
                if userStr == "n":
                    bl = [1, 0]
                    ur = [1, 0]
                    attempts = attempts + 1
                    print("Line-fitting boundaries (attempt " + str(attempts) + ".)")
                    print("Choose bottom-left location (click): ")
                    i = -1
            if attempts == MAX_ATTEMPTS + 1:
                fig.canvas.mpl_disconnect(cid)
                plt.close()
                print("Wow, something is going seriously wrong for you. Good luck.")
            i = i + 1

    # open initial data cube inspection window
    win_str = targ_name + " " + molecular_trans + ": Initial Data Cube Inspection"
    data = hdul[0].data
    data = data[0:1, 0:(hdul[0].header['NAXIS3']), int(small_y):int(big_y), int(small_x):int(big_x)]
    data = np.sum(data, axis=(0, 1))
    fig, ax = plt.subplots(1, num=win_str)
    ax.imshow(data, cmap='gray', origin='lower')

    # get line-fitting boundaries
    global MAX_ATTEMPTS
    MAX_ATTEMPTS = 5
    global attempts
    attempts = 1
    global coords
    coords = [1, 0]
    # disconnect = False
    global bl
    bl = [1, 0]
    global ur
    ur = [1, 0]
    global i
    i = 0
    print("Line-fitting boundaries (attempt " + str(attempts) + ".)")
    print("Choose bottom-left location (click): ")
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    bl = [math.floor(bl[0]), math.floor(bl[1])]
    ur = [math.ceil(ur[0]), math.ceil(ur[1])]
    # For testing purposes
    print(bl, ur)


if __name__ == '__main__':
    main()

# Do first result panel.
# Seen in emission or absorption, branch if/else emission absorption.
# Is it clearly seen in initial window? y/n. Allow some option to go slice by slice, a skip button, satisfied button,
# is this region complete, etc. Look into mask files to multiply cube, zeroing out any region not included within map
# construction
# region for data analysis later. While loop for polygon drawing. np.fit. Luminosity-weighted moment maps (1st, 2nd,
# 3rd, 4th). Look into Matplotlib button or normalized pixel for exit.
