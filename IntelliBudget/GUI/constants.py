""" Contains all constant objects that need to be available to two or more
    other GUI modules.
"""

import tkinter as tk
from . import style as sty

TITLE = 'IntelliBudget'
fonts = sty.Fonts()
debug = True


class Field():
    """ Enables all widgets related to the same field to share their own
        namespace.
    """
    pass


def addBuffer(frame, side, height=sty.height, width=sty.width):
    if side == 'RL':
        addBuffer(frame, side='left')
        addBuffer(frame, side='right')
    elif side in ['top', 'bottom']:
        buffer_frame = tk.Frame(frame, height=height)
        buffer_frame.pack(side=side)
    elif side in ['right', 'left']:
        buffer_frame = tk.Frame(frame, width=width)
        buffer_frame.pack(side=side)
    else:
        raise ValueError
