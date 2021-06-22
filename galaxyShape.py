import math
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.widgets import Button
from prompt import call

angle = None
vertices = []
ax = plt.subplots
fig = plt.subplots
cid = None
globalTyp = ''
globalData = None
globalName = ''
ATTEMPTS = 5


# noinspection PyUnusedLocal
def closer(event):
    global ATTEMPTS
    root = tk.Tk()
    root.withdraw()
    user_str = call('Are you satisfied with the object shape outline?')
    if user_str == 'y':
        fig.canvas.mpl_disconnect(cid)
        plt.savefig("shape_outline.png")
        plt.close()
    else:
        ATTEMPTS = ATTEMPTS - 1
        print(str(ATTEMPTS) + " attempts remaining")
        # shape(globalTyp, globalData, globalName)


def process_vertices(x, y):
    global vertices
    vertices.append([math.floor(x), math.floor(y)])
    [p.remove() for p in reversed(ax.patches)]
    poly = patches.Polygon(vertices, edgecolor='r', facecolor="none")
    ax.add_patch(poly)
    plt.draw_all()
    plt.pause(0.001)  # Extra pause to allow plt to draw box
    plt.draw_all()
    plt.pause(0.001)


def select_vertices(event):
    if (event.xdata is not None) and (event.xdata > 1) and (event.ydata > 1):
        process_vertices(event.xdata, event.ydata)


def process_ellipse(x, y):
    global vertices
    global angle
    vertices.append([math.floor(x), math.floor(y)])
    if len(vertices) == 3:
        angle = math.degrees(math.atan((vertices[0][1] - vertices[1][1]) / (vertices[0][0] - vertices[1][0])))
        ellipse = patches.Ellipse(vertices[0], 2 * np.sqrt(np.square(vertices[0][0] - vertices[1][0]) +
                                                           np.square(vertices[0][1] - vertices[1][1])),
                                  2 * np.sqrt(np.square(vertices[0][0] - vertices[2][0]) +
                                              np.square(vertices[0][1] - vertices[2][1])), angle=angle, edgecolor='r',
                                  facecolor="none")
        ax.add_patch(ellipse)
        plt.draw_all()
        plt.pause(0.001)  # Extra pause to allow plt to draw box
        plt.draw_all()
        plt.pause(0.001)


def select_ellipse(event):
    if (event.xdata is not None) and (event.xdata > 1) and (event.ydata > 1):
        process_ellipse(event.xdata, event.ydata)


def shape(typ, data, name):
    global globalTyp
    globalTyp = typ
    global globalData
    globalData = data
    global globalName
    globalName = name
    global ax
    global fig
    global cid
    fig, ax = plt.subplots(1, num=name + ": Determining Line Regions")
    ax.imshow(data, cmap='jet', origin="lower")
    close_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    close_button = Button(close_ax, 'END')
    close_button.on_clicked(closer)
    if typ == 'p':
        print("Select polygon vertices (click). Click END when finished: ")
        cid = fig.canvas.mpl_connect('button_press_event', select_vertices)
        plt.show()
    elif typ == 'e':
        print("Select ellipse center first, followed by semi-major and semi-minor axes (click). Click END when "
              "finished: ")
        cid = fig.canvas.mpl_connect('button_press_event', select_ellipse)
        plt.show()
    return vertices, angle
