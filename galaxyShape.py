import matplotlib.patches as patches
import matplotlib.pyplot as plt

vertices = []

ax = plt.subplots


def process_vertices(x, y):
    global vertices
    vertices.append([x, y])
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


def shape(typ, data, name):
    global ax
    fig, ax = plt.subplots(1, num=name + ": Determining Line Regions")
    ax.imshow(data, cmap='gray', origin='lower')
    if typ == 'p':
        print("Select polygon vertices (click). Click END when finished: ")
        cid = fig.canvas.mpl_connect('button_press_event', select_vertices)
        plt.show()
