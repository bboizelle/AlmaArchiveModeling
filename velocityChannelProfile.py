import tkinter as tk

import numpy as np
from matplotlib import pyplot as plt
import math
from prompt import call

ax = plt.subplots
fig = plt.subplots
cid = None
ATTEMPTS = 5
L = 0
M = 0


# Simple masking script
def apply_mask(data, mask):
    profile = np.zeros(len(data[:, 0, 0]))

    for i in range(len(profile)):
        profile[i] = np.sum(np.multiply(data[i, :, :], mask))

    return profile


def process_click(x):
    global L
    global M
    if L == 0:  # Get avg velocity
        ax.vlines(x, 0, 1, transform=ax.get_xaxis_transform(), colors="green", linestyles="dashed")
        plt.gcf().text(0.82, 0.65, r"V$_{ave}$=" + str(math.floor(x)) + ".", fontsize=11)
        plt.draw_all()
        plt.pause(0.001)  # Extra pause to allow plt to draw box
        plt.draw_all()
        plt.pause(0.001)
        L = 1
    if L == 1:
        root = tk.Tk()
        root.withdraw()
        user_str = call('Are you satisfied with the systemic velocity?')
        if user_str != 'y':
            L = 0
        else:
            print("\nCLick minimum velocity to allow for Gaussian peak in line fitting (include wing structure if "
                  "present): ")
            L = 2
            return
    if L == 2:  # Get velocity bounds
        ax.vlines(x, 0, 1, transform=ax.get_xaxis_transform(), colors="red", linestyles="dashed")
        plt.draw_all()
        plt.pause(0.001)  # Extra pause to allow plt to draw box
        plt.draw_all()
        plt.pause(0.001)
        if M == 1:
            plt.gcf().text(0.82, 0.45, r"V$_{max}$=" + str(math.floor(x)) + ".", fontsize=11)
            plt.draw_all()
            plt.pause(0.001)  # Extra pause to allow plt to draw box
            plt.draw_all()
            plt.pause(0.001)
            root = tk.Tk()
            root.withdraw()
            user_str = call('Are you satisfied with the velocity limits?')
            if user_str != 'y':
                L = 0
            else:
                fig.canvas.mpl_disconnect(cid)
                plt.savefig("velocity_channel_profile.png")
                plt.close()
        if M == 0:
            plt.gcf().text(0.82, 0.55, r"V$_{min}$=" + str(math.floor(x)) + ".", fontsize=11)
            plt.draw_all()
            plt.pause(0.001)  # Extra pause to allow plt to draw box
            plt.draw_all()
            plt.pause(0.001)
            print("CLick maximum velocity to allow for Gaussian peak in line fitting (include wing structure if "
                  "present): ")
            M = 1


def on_click(event):
    if (event.xdata is not None) and (event.xdata > 1):
        process_click(event.xdata)


def velocities(naxis3, v, profile, win_str):
    global fig
    global ax
    global cid

    fig, ax = plt.subplots(1, num=win_str + ": Velocity Channel Profile")

    # For calculating bin sizes / bar widths
    lines = np.ones(naxis3)
    lines[0] = v[1] - v[0]
    for i in range(len(lines) - 1):
        lines[i + 1] = v[i + 1] - v[i]

    # cdelt3 my be pos or neg (don't worry about flipped)
    ax.bar(v, profile * 1000, lines, fill=1, facecolor='grey', edgecolor='grey')
    ax.set_ylabel('Flux Density (mJy)', labelpad=10.0, fontsize=12)
    ax.set_xlabel(r'Velocity Channel (km s$^{-1}$)', labelpad=10.0, fontsize=12)
    plt.gcf().text(0.82, 0.75, "Velocities (km/s):", fontsize=11)
    plt.subplots_adjust(right=0.8)
    print("\nClick on galaxy (average) velocity (c*z): ")
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()

    integrated_flux = profile * v  # in jy km / s, only between the channel ranges they selected
    # sum up integrated flux over the range of channels they have selected (lower to upper bound) ^--
    #    maybe relabelling axis would be easier than converting channels to...? -look into
    return integrated_flux
