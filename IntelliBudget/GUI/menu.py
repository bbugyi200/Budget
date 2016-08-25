""" Renders the top menu bar for the GUI. """

import tkinter as tk

from .constants import MONTH, fonts
from .newlimits import NewLimits

from .. import dates
from .. import budget


class Menu():
    def __init__(self, parent):
        self.parent = parent
        self.Make()

    def Make(self):
        """ Creates dropdown menus on the top of the window """
        menu = tk.Menu(self.parent)
        self.parent.master.config(menu=menu)

        fileMenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=fileMenu)

        NL = NewLimits(self.parent)
        fileMenu.add_command(label='Update Limits', command=NL.Make)
        fileMenu.add_separator()
        fileMenu.add_command(label='Quit', command=self.parent.quit)

        viewMenu = tk.Menu(menu)
        menu.add_cascade(label='Archives', menu=viewMenu)

        for month in dates.getDBFiles():
            viewMenu.add_command(label=month,
                                 command=self.GetBudgetFactory(month))

    def GetBudgetFactory(self, month):
        """ Returns a function that creates a new budget. """
        def GetBudget():
            self.parent.Budget.close()
            self.parent.Budget = budget.Budget(DB=month)
            self.parent.refresh_screen()
        return GetBudget
