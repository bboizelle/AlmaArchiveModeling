import os
import tkinter as tk

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from voronoi import binning
from prompt import call
from velocityChannelProfile import apply_mask, velocities

plt.style.use(astropy_mpl_style)

MAX_ATTEMPTS = 5
attempts = 1
coords = [1, 0]
bl = [1, 0]
ur = [1, 0]
bbl = [1, 0]
bur = [1, 0]
rbl = [1, 0]
rur = [1, 0]
i = 0
userStr = ""
background = False


def main():
    fits_file = "NGC315_CO21_C5_bri_10kms.pbcor.fits"

    # print working directory
    print("\nCurrent path is: ")
    cwd = os.getcwd()
    print(cwd)

    # list all .fits files in cwd
    print("\nFITS files are: ")
    for file in os.listdir(cwd):
        if file.endswith(".fits"):
            print(file)

    # Reads in original fits image dimensions
    hdul = fits.open(fits_file)

    bmaj = hdul[0].header['BMAJ'] * 3600
    bmin = hdul[0].header['BMIN'] * 3600
    cdelt2 = hdul[0].header['CDELT2'] * 3600
    beam_area = ((1.1331 * bmaj * bmin) / (cdelt2 ** 2))  # Units in arcseconds

    c_speed = 299792.458  # km/sec

    crval3 = hdul[0].header['CRVAL3']
    cdelt3 = hdul[0].header['CDELT3']
    naxis3 = hdul[0].header['NAXIS3']
    crpix3 = hdul[0].header['crpix3']
    nu_obs = crval3 + cdelt3 * (np.arange(naxis3) - crpix3 + 1)

    nu_0 = hdul[0].header['RESTFRQ']
    v = c_speed * ((nu_0 / nu_obs) - 1)  # Velocity definition due to cosmological expansion

    x = hdul[0].header['NAXIS1']
    y = hdul[0].header['NAXIS2']

    xy = str(x) + '/' + str(y)
    print("\nSpatial (x,y) dimensions:", xy, "pixels")
    print("Spectral (z) dimension:", str(hdul[0].header['NAXIS3']), "channels")

    small_x = 250
    big_x = 390
    small_y = 250
    big_y = 390

    # trim unnecessary channels
    channel = abs((hdul[0].header['CDELT3'] / hdul[0].header['RESTFRQ']) * c_speed)
    channel = round(channel, 2)
    print("\nCurrent velocity channel binning is", channel, "km/s")
    print("Channels over which line is")
    print("observed in the ORIGINAL data cube:")
    z1 = 31
    z2 = 121

    # get target name
    targ_name = "NGC315"

    # get molecular transition
    molecular_trans = "CO21"

    # Function that receives click events and returns valid coordinate pairs
    def onclick(event):
        global background
        global bbl
        global bur
        global rbl
        global rur
        global i
        ix, iy = event.xdata, event.ydata
        if (ix is not None) and (ix > 1) and (iy > 1):
            global bl
            global ur
            global attempts
            attempts = attempts
            if i == 1:
                rect = patches.Rectangle((bl[0], bl[1]), (ix - bl[0]), (iy - bl[1]), linewidth=attempts,
                                         edgecolor='r', facecolor="none")
                # ax.add_patch(rect)
                plt.draw_all()
                plt.pause(0.001)
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
                root = tk.Tk()
                root.withdraw()
                if not background:
                    userStr = call('Are you satisfied with the object fitting box?')
                else:
                    userStr = call('Are you satisfied with the background fitting box?')
                root.destroy()
                if userStr == "y":
                    i = 0
                    attempts = 1
                    # fig.canvas.mpl_disconnect(cid)
                    if not background:
                        rbl = bl
                        rur = ur
                        print("\nBackground uncertainty boundaries (attempt " + str(attempts) + ".)")
                        bl = [1, 0]
                        ur = [1, 0]
                        print("Choose bottom-left location (click): ")
                        background = True
                        # fig.canvas.mpl_connect('button_press_event', onclick)
                        i = -1
                    else:
                        bbl = bl
                        bur = ur
                        # fig.canvas.mpl_disconnect(cid)
                        plt.close()
                if userStr == "n":
                    bl = [1, 0]
                    ur = [1, 0]
                    attempts = attempts + 1
                    if not background:
                        print("\nLine-fitting boundaries (attempt " + str(attempts) + ".)")
                    else:
                        print("\nBackground uncertainty boundaries (attempt " + str(attempts) + ".)")
                    print("Choose bottom-left location (click): ")
                    i = -1
            if attempts == MAX_ATTEMPTS + 1:
                # fig.canvas.mpl_disconnect(cid)
                plt.savefig('line_fitting_boundaries.png')
                plt.close()
                print("Wow, something is going seriously wrong for you. Good luck.")
            i = i + 1

    # open initial data cube inspection window
    win_str = targ_name + " " + molecular_trans
    data = hdul[0].data
    data = data[0:1, z1:z2, int(small_y):int(big_y), int(small_x):int(big_x)]
    data = np.sum(data, axis=(0, 1))
    # fig, ax = plt.subplots(1, num=win_str + ": Initial Data Cube Inspection")
    # ax.imshow(data, cmap='gray', origin="lower")

    # get line-fitting boundaries
    global MAX_ATTEMPTS
    MAX_ATTEMPTS = 5
    global attempts
    attempts = 1
    global coords
    coords = [1, 0]
    global bl
    bl = [1, 0]
    global ur
    ur = [1, 0]
    global i
    i = 0
    global background
    global bbl
    global bur
    global rbl
    global rur
    print("\nLine-fitting boundaries (attempt " + str(attempts) + ".)")
    print("Choose bottom-left location (click): ")
    # cid = fig.canvas.mpl_connect('button_press_event', onclick)

    # plt.show()
    rbl = [29, 31]
    rur = [115, 115]
    if rbl[0] > rur[0]:
        tmp = rbl[0]
        rbl[0] = rur[1]
        rur[0] = tmp
    if rbl[1] > rur[1]:
        tmp = rbl[1]
        rbl[1] = rur[1]
        rur[1] = tmp
    bbl = [21, 14]
    bur = [116, 37]
    limited_data = data[rbl[1]:rur[1], rbl[0]:rur[0]]
    # emission_absorption = input("Is the line seen in emission or absorption? (e/a): ")
    # "a" functionality not implemented currently
    # seen_in_window = input("Is the molecular emission/absorption clearly seen in the Initial Cube Inspection window? "
    #                       "(y/n): ")

    print("\nElliptical or polygon shape? (e/p): ")
    userStr = 'e'
    # vertices, angle = shape(userStr, limited_data, win_str)
    # vertices = list(map(tuple, vertices))
    img = Image.new("L", (limited_data.shape[1], limited_data.shape[0]), 0)
    if userStr == 'e':
        vertices = [(40, 39), (48, 45), (63, 11)]
        ImageDraw.Draw(img).ellipse([vertices[0][0] - (np.sqrt(np.square(vertices[0][0] - vertices[1][0]) +
                                                               np.square(vertices[0][1] - vertices[1][1]))),
                                     vertices[0][1] - (np.sqrt(np.square(vertices[0][0] - vertices[2][0]) +
                                                               np.square(vertices[0][1] - vertices[2][1]))),
                                     vertices[0][0] + (np.sqrt(np.square(vertices[0][0] - vertices[1][0]) +
                                                               np.square(vertices[0][1] - vertices[1][1]))),
                                     vertices[0][1] + (np.sqrt(np.square(vertices[0][0] - vertices[2][0]) +
                                                               np.square(vertices[0][1] - vertices[2][1])))],
                                    outline=1, fill=1)
        angle = 36.86989764584402
        img = img.rotate(-angle, center=vertices[0])
        mask = np.array(img)
    else:
        # ImageDraw.Draw(img).polygon(vertices, outline=1, fill=1)
        mask = np.array(img)

    # Extract data from "data"
    velocity_channels = np.array(hdul[0].data)
    velocity_channels = velocity_channels[0, :, (int(small_y) + rbl[1]):(rur[1] + int(small_y)),
                                                (int(small_x) + rbl[0]):(rur[0] + int(small_x))]

    profile = apply_mask(velocity_channels, mask) / beam_area  # (Jy)

    integrated_flux, error_flux = velocities(naxis3, v, profile, win_str)

    # Moving on to Voronoi binning section

    print("\nMoving on to the next section")
    userStr = input("Press ENTER to continue...")
    while userStr != "":
        userStr = input("Press ENTER to continue...")

    userStr = input("\nDesired Voronoi binning S/N (recommend 7.5): ")
    binning(userStr)


if __name__ == '__main__':
    main()

# TODO- add box showing synthesized beam- how?
# https://www-astro.physics.ox.ac.uk/~mxc/software/ for Voronoi binning info
# TODO- Ask if they would like to select the second window.
# TODO- Return vel and prof from velocity_channel_profile in txt file, with different columns,
#   give descriptive name, line_prof.txt
# TODO- calculate standard deviation/RMS for noise from background fitting box.
