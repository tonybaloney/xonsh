"""Matplotlib hooks, for what its worth."""
import shutil

import numpy as np
import matplotlib.pyplot as plt

from xonsh.tools import print_color

def figure_to_rgb_array(fig, width, height):
    """Converts figure to a numpy array of rgb values

    Forked from http://www.icare.univ-lille1.fr/wiki/index.php/How_to_convert_a_matplotlib_figure_to_a_numpy_array_or_a_PIL_image
    """
    w, h = fig.canvas.get_width_height()
    dpi = fig.get_dpi()
    #fig.set_size_inches(width/dpi, height/dpi, forward=True)
    fig.set_size_inches(width/dpi, 2*height/dpi, forward=True)
    width, height = fig.canvas.get_width_height()
    # draw the renderer
    fig.canvas.draw()

    # Get the RGB buffer from the figure
    buf = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8)
    buf.shape = (height, width, 3)
    return buf


def buf_to_color_str(buf):
    """Converts an RGB array to a xonsh color string."""
    same = ' '
    diff = '\u2580'
    fgpix = '{{#{0:02x}{1:02x}{2:02x}}}'
    bgpix = '{{bg#{0:02x}{1:02x}{2:02x}}}'
    pixels = []
    #for h in range(0, buf.shape[0], 2):
    for h in range(0, buf.shape[0], 2):
        last0 = last1 = None
        for w in range(buf.shape[1]):
            rgb0, rgb1 = buf[h:h+2,w]
            if last0 is None and last1 is None:
                pixels.append(bgpix.format(*rgb1))
                if (rgb0 == rgb1).all():
                    pixels.append(same)
                else:
                    pixels += [fgpix.format(*rgb0), diff]
            elif (last0 == rgb0).all() and (last1 == rgb1).all():
                pixels.append(same if (rgb0 == rgb1).all() else diff)
            elif (last0 == rgb0).all():
                pixels += [fgpix.format(*rgb0), diff]
            elif (last1 == rgb1).all():
                pixels += [bgpix.format(*rgb1), diff]
            else:
                pixels += [bgpix.format(*rgb1), fgpix.format(*rgb0), diff]
            last0 = rgb0
            last1 = rgb1
        pixels.append('{NO_COLOR}\n')
    pixels[-1] = pixels[-1].rstrip()
    return ''.join(pixels)


def show():
    fig = plt.gcf()
    w, h = shutil.get_terminal_size()
    h -= 1  # leave space for next prompt
    buf = figure_to_rgb_array(fig, w, h)
    s = buf_to_color_str(buf)
    print_color(s)
