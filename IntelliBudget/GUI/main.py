""" Main GUI file. Launches all other widgets. """

import tkinter as tk
import tkinter.messagebox

from . import style as sty
from .constants import TITLE, MONTH, fonts, debug
from .menu import Menu
from .budgetdata import BudgetData
from .newlimits import NewLimits
from .expensedisplay import ExpenseDisplay
from .expenseform import ExpenseForm

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
        self.master.title(TITLE)

        Menu(self)

        row = 0

        self.topFrame = tk.Frame(self)
        self.topFrame.grid(row=row, columnspan=5); row += 1

        self.TopTitle(self.topFrame)

        # frame1 is the leftmost frame
        frame1 = tk.Frame(self, width=700, height=200)
        frame1.grid(row=row, column=0)

        frame1_Lbuffer = tk.Frame(frame1, width=sty.width)
        frame1_Lbuffer.pack(side='left')
        frame1_Rbuffer = tk.Frame(frame1, width=sty.width)
        frame1_Rbuffer.pack(side='right')

        self.BD = BudgetData(frame1, self.Budget)
        self.BD.pack()

        frame2 = tk.Frame(self)
        frame2.grid(row=row, column=1)

        self.ED = ExpenseDisplay(frame2, self)
        self.ED.pack()

        frame3 = tk.Frame(self, width=200, height=200)
        frame3.grid(row=row, column=2)

        # Left buffer for fframe3
        frame3_Lbuffer = tk.Frame(frame3, width=sty.width)
        frame3_Lbuffer.pack(side='left')

        # Right buffer for fframe3
        frame3_Rbuffer = tk.Frame(frame3, width=sty.width)
        frame3_Rbuffer.pack(side='right')

        # frame3 is used for the Expense form
        EF = ExpenseForm(frame3, self)
        EF.pack()

        # Asks user to setup limits if this is the first time the program's
        # been run this month.
        if FIRST_USE:
            message = "It looks like this is your first time using {0} in " \
                      "the month of {1}! \n\nBefore you get started, let's " \
                      "setup this month's spending limits!"
            message = message.format(TITLE, MONTH)

            tkinter.messagebox.showinfo("FIRST USE IN " + MONTH + "!!!",
                                        message)
            NL = NewLimits(self)
            NL.Make()

    def TopTitle(self, frame):
        TopTitle = tk.Label(frame,
                            text=TITLE,
                            font='Verdana 40 underline')
        TopTitle.pack(side='top')
        TT_bbuffer = tk.Frame(frame, height=20)
        TT_bbuffer.pack(side='bottom')

    def refresh_screen(self):
        """ This function is used to refresh the main GUI window. """
        self.master.title(TITLE)
        self.BD.set_dynamic_data()
        self.ED.Make()
