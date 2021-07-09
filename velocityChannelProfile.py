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
v_min = 0
v_max = 0
integrated_flux = 0
vel = np.array([])
prof = np.array([])
background_min = 0
background_max = 0


# Simple masking script
def apply_mask(data, mask):
    profile = np.zeros(len(data[:, 0, 0]))

    for i in range(len(profile)):
        profile[i] = np.sum(np.multiply(data[i, :, :], mask))

    return profile


def process_click(x):
    global L
    global M
    global v_min
    global v_max
    global integrated_flux
    global prof
    global vel
    global background_min
    global background_max

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
            v_max = math.ceil(x)
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

                upper_velocity = np.where(vel > v_min)
                lower_velocity = np.where(vel < v_max)

                integrated_flux = prof * vel  # in jy km / s, only between the channel ranges they selected
                total_flux = np.sum(integrated_flux[np.min(lower_velocity): np.max(upper_velocity)])
                integrated_flux = total_flux / (v_max - v_min)

                plt.gcf().text(0.82, 0.35, "Estimated Flux:", fontsize=11)
                plt.gcf().text(0.82, 0.3, str(round(integrated_flux, 2)) + " Jy km/s", fontsize=11)
                plt.draw_all()
                plt.pause(0.001)  # Extra pause to allow plt to draw box
                plt.draw_all()
                plt.pause(0.001)

                user_str = call('Would you like to calculate uncertainty?')
                if user_str == "y":
                    print("Click minimum and maximum velocities of background region.")
                    L = 3
                else:
                    fig.canvas.mpl_disconnect(cid)
                    plt.savefig("velocity_channel_profile.png")
                    plt.close()
        if M == 0:
            v_min = math.floor(x)
            plt.gcf().text(0.82, 0.55, r"V$_{min}$=" + str(math.floor(x)) + ".", fontsize=11)
            plt.draw_all()
            plt.pause(0.001)  # Extra pause to allow plt to draw box
            plt.draw_all()
            plt.pause(0.001)
            print("CLick maximum velocity to allow for Gaussian peak in line fitting (include wing structure if "
                  "present): ")
            M = 1

    if L == 3:
        background_min = math.ceil(x)
        L = 4
        return
    if L == 4:
        background_max = math.ceil(x)
        print(background_min, background_max)


def on_click(event):
    if (event.xdata is not None) and (event.xdata > 1):
        process_click(event.xdata)


def velocities(naxis3, v, profile, win_str):
    global fig
    global ax
    global cid
    global integrated_flux
    global vel
    global prof

    prof = profile
    vel = v

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

    return integrated_flux
