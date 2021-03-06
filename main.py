import math
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from astropy.io import fits
from astropy.visualization import astropy_mpl_style

# Ask about breaking file up into other functions / modules

plt.style.use(astropy_mpl_style)

fitsFile = None

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
    fitsFile = userStr

# Reads in original fits image dimensions
hdul = fits.open(fitsFile)
x = hdul[0].header['NAXIS1']
y = hdul[0].header['NAXIS2']
smallX = 0
bigX = x
smallY = 0
bigY = y
xy = str(x) + '/' + str(y)
print("\nSpatial (x,y) dimensions:", xy, "pixels")
print("Spectral (z) dimension:", str(hdul[0].header['NAXIS3']), "channels")

# ask user if they want to use subregion
userStr = input("\nUse a subregion of the full spatial (x,y) dimensions? (y/n): ")
if userStr == 'y':
    smallX = input("Left x-value (integer, e.g., 100): ")
    bigX = input("Right x-value (integer, e.g., 500): ")
    smallY = input("Lower y-value (integer, e.g., 100): ")
    bigY = input("Upper y-value (integer, e.g., 500: ")
    x = int(bigX) - int(smallX)
    y = int(bigY) - int(smallY)

# ask user if they want to undersample spacial dimensions
userStr = input("\nUndersample the spacial (x,y) dimensions? (y/n): ")
if userStr == 'y':
    userStr = 'y'  # FIXME later

# trim unnecessary channels
cSpeed = 299792.458
channel = abs((hdul[0].header['CDELT3'] / hdul[0].header['RESTFRQ']) * cSpeed)
channel = round(channel, 2)
print("\nCurrent velocity channel binning is", channel, "km/s")
print("Channels over which line is")
print("observed in the ORIGINAL data cube:")
z1 = input("z1 (lowest) channel value: ")
z2 = input("z2 (highest) channel value: ")

# ask user if they want to undersample frequency
userStr = input("\nUndersample the frequency (z) dimension? (y/n): ")
if userStr == 'y':
    userStr = 'y'  # FIXME later

# get target name
targName = input("Enter target name (e.g., NGC 1332): ")

# get molecular transition
molecularTrans = input("\nEnter molecular transition name (e.g., CO21 for CO(2-1)): ")

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
            userStr = input("Are you satisfied with the object fitting box (y/n): ")
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
winStr = targName + " " + molecularTrans + ": Initial Data Cube Inspection"
data = hdul[0].data
data = data[0:1, 0:(hdul[0].header['NAXIS3']), int(smallY):int(bigY), int(smallX):int(bigX)]
data = np.sum(data, axis=(0, 1))
fig, ax = plt.subplots(1, num=winStr)
ax.imshow(data, cmap='gray', origin='lower')

# get line-fitting boundaries
MAX_ATTEMPTS = 5
attempts = 1
coords = [1, 0]
disconnect = False
bl = [1, 0]
ur = [1, 0]
i = 0
print("Line-fitting boundaries (attempt " + str(attempts) + ".)")
print("Choose bottom-left location (click): ")
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
bl = [math.floor(bl[0]), math.floor(bl[1])]
ur = [math.ceil(ur[0]), math.ceil(ur[1])]
# For testing purposes
print(bl, ur)
