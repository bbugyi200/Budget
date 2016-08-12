""" fonts.py

Holds GUI fonts and formatting relevant information.
"""

# Default width and height for buffer between frames
width = 25
height = 25


class Fonts:
    """ This class holds methods that return font types for tkinter.
    
    An object of this class is meant to be embedded into the main GUI
    class.
    """
    def __init__(self): pass
        
    def title(self, size='12'):
        return 'Verdana ' + size + ' underline'
