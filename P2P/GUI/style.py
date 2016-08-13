""" style.py

Holds GUI fonts and formatting relevant information.
"""

# Default width and height for buffer between frames
width = 25
height = 25

# Colors
abcolor = '#E8E7E7'


class Fonts:
    """ This class holds methods that return font types for tkinter """
    def __init__(self):
        pass

    def title(self, size='15'):
        return 'Verdana ' + size + ' underline'

    def button(self):
        return 'default 13 bold'
