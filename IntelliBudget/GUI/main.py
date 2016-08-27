""" Main GUI file. Launches all other widgets. """

import tkinter as tk
import tkinter.messagebox

from .constants import TITLE, addBuffer
from .menu import Menu
from .budgetdata import BudgetData
from .newlimits import NewLimits
from .expensedisplay import ExpenseDisplay
from .expenseform import ExpenseForm

from ..dates import getMonth
from .. import budget
from ..budget import NoneNotAllowed


class Main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        FIRST_USE = False

        try:
            self.Budget = budget.Budget()
        except NoneNotAllowed:
            FIRST_USE = True
            self.Budget = budget.Budget(0)

        self.master = master

        self.SetWindowTitle()

        Menu(self)

        topFrame = tk.Frame(self)
        topFrame.pack(side='top')

        TopTitle = tk.Label(topFrame,
                            text=TITLE,
                            font='Verdana 40 underline')
        TopTitle.pack()
        addBuffer(topFrame, side='bottom', height=20)

        frame1 = tk.Frame(self)
        frame1.pack(side='left')
        addBuffer(frame1, side='RL')

        self.BD = BudgetData(frame1, self.Budget)
        self.BD.pack()

        frame2 = tk.Frame(self)
        frame2.pack(side='left')

        self.ED = ExpenseDisplay(frame2, self)
        self.ED.pack()

        frame3 = tk.Frame(self)
        frame3.pack(side='left')
        addBuffer(frame3, side='RL')

        EF = ExpenseForm(frame3, self)
        EF.pack()

        if FIRST_USE:
            self.FirstUse()

    def FirstUse(self):
        """Asks user to setup limits if this is the first time the program's
           been run this month.
        """
        message = "It looks like this is your first time using {0} in " \
                  "the month of {1}! \n\nBefore you get started, let's " \
                  "setup this month's spending limits!"
        message = message.format(TITLE, getMonth())

        tkinter.messagebox.showinfo("FIRST USE IN " + getMonth() + "!!!",
                                    message)
        NL = NewLimits(self)
        NL.Make()

    def SetWindowTitle(self, month=None):
        self.MONTH = getMonth(month)
        WindowTitle = ''.join([TITLE, ' - ({0})'])
        WindowTitle = WindowTitle.format(self.MONTH)
        self.master.title(WindowTitle)

    def refresh_screen(self, month=None):
        """ This function is used to refresh the main GUI window. """
        self.SetWindowTitle(month)
        self.BD.set_dynamic_data()
        self.ED.Make()
