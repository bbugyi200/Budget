""" Renders the display of all of the user's current expenses. """

import tkinter as tk
from tkinter.font import Font
import tkinter.ttk as ttk

from . import style as sty
from .constants import fonts, debug


class ExpenseDisplay(tk.Frame):
    def __init__(self, parent, master):
        tk.Frame.__init__(self, parent)
        self.master = master
        self.Make()

    def Make(self):
        """ Displays all of this Month's expenses. """

        # If the ExpenseFrame exists, it will be destroyed
        try:
            self.outer.destroy()
        except AttributeError as e:
            if debug: print(e.__class__, ':: ', e)
            else: pass

        # outer is created so the delete button frames can be
        # seperated visually from the expense list frame.
        self.outer = tk.Frame(self)
        self.outer.pack()

        self.Title()

        self.ExpenseFrame = tk.Frame(self.outer)
        self.ExpenseFrame.pack(fill='both')

        # Scrollbar for expense list
        scrollbar = tk.Scrollbar(self.ExpenseFrame)
        scrollbar.pack(side='right', fill='y')

        # Columns for expense list
        dataCols = ['Date', 'Expense Type', 'Cost', 'Notes']

        self.tree = ttk.Treeview(self.ExpenseFrame,
                                 columns=dataCols,
                                 show='headings')

        Exp_Attrs = self.master.Budget.expenses.get()

        # maxWidths is used to store the max width of each column in the
        # TreeView object.
        maxWidths = dict()

        # Loop sets max for each column to 0, so each max has starting value
        for col in dataCols:
            maxWidths[col] = 0

        # Defines the font that the TreeView elements will use
        treeFont = Font(self.ExpenseFrame, 'Times', "12")

        # Inserts each expense into the Treeview object
        for values in Exp_Attrs:
            self.tree.insert('', 'end', values=values, tag='expense')

            # This loop finds the width of the largest string in each column.
            for col, item in zip(dataCols, values):
                stringWidth = treeFont.measure(item)
                if stringWidth > maxWidths[col]:
                    maxWidths[col] = stringWidth

        # This loop serves two functions:
        # 1 - Sets the headings in the expense list.
        #     Without this loop, the headings will not actually show.
        #
        # 2 - Sets the width of each column based on the largest string within
        #     each column.
        for col in dataCols:
            self.tree.heading(col, text=col)
            extra = 100
            MAX = maxWidths[col] + extra
            self.tree.column(col, width=MAX)

        # Sets the font of the TreeView elements
        self.tree.tag_configure('expense', font=treeFont)

        # 'yscroll' option must be set to scrollbar set object
        self.tree['yscroll'] = scrollbar.set

        self.tree.pack(side='left', fill='both')

        # Associates scrollbar with the Treeview object
        scrollbar.config(command=self.tree.yview)

        self.CreateDeleteButton()

    def Title(self):
        title_Bbuffer = tk.Frame(self.outer, height=5)

        title_text = "Expense List"
        self.Lab_PayPeriod = tk.Label(self.outer,
                                      text=title_text,
                                      font=fonts.title())

        self.Lab_PayPeriod.pack(side='top')
        title_Bbuffer.pack(side='top')

    def CreateDeleteButton(self):
        """ Creates a delete button and adds extra vertical space
        between the button and the expense list
        """

        # Outer frame that hold delete button and buffer space
        outer = tk.Frame(self.outer)
        outer.pack(side='bottom')

        # Buffer space between the button and the expense list
        delete_Tbuffer = tk.Frame(outer, height=sty.height)
        delete_Tbuffer.pack(side='top')

        delete_Bbuffer = tk.Frame(outer, height=sty.height)
        delete_Bbuffer.pack(side='bottom')

        # This frame will hold the actual delete button
        delete_frame = tk.Frame(outer)
        delete_frame.pack()

        delete_button = tk.Button(delete_frame,
                                  text='Delete Selected',
                                  activebackground=sty.abcolor,
                                  command=self.DeleteSelected,
                                  font=fonts.button())
        delete_button.pack()

    def DeleteSelected(self):
        """ This function is called when the user presses the
        Delete Selected' button.
        """
        index = None
        try:
            # Sets index to the offset of the selected item in the expense list
            for i, item in enumerate(self.tree.get_children()):
                if item == self.tree.focus():
                    index = i

            # Deletes the expense at the specified index
            self.master.Budget.remove_expense(index)
            self.master.refresh_screen()

        # Does nothing if 'Delete Selected' button is clicked when no item is
        # selected.
        except TypeError as e:
            if debug: print(e.__class__, ':: ', e)
            else: pass
