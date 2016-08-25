""" Renders the display of all of the user's current expenses. """

import tkinter as tk
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
        except AttributeError:
            if debug: pass

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
        dataCols = ['Expense Type', 'Cost', 'Notes']

        self.tree = ttk.Treeview(self.ExpenseFrame,
                                 columns=dataCols,
                                 show='headings')

        # Sets the headings in the expense list.
        # Without this loop, the headings will not actually show.
        for c in dataCols:
            self.tree.heading(c, text=c)

        Exp_Attrs = self.master.Budget.expenses.get()

        # Inserts each expense into the Treeview object
        for item in Exp_Attrs:
            self.tree.insert('', 'end', values=item)

        # 'yscroll' option must be set to scrollbar set object
        self.tree['yscroll'] = scrollbar.set

        self.tree.pack(side='left', fill='both')

        # Associates scrollbar with the Treeview object
        scrollbar.config(command=self.tree.yview)

        self.DeleteButton()

    def Title(self):
        title_Bbuffer = tk.Frame(self.outer, height=5)

        title_text = "Expense List"
        self.Lab_PayPeriod = tk.Label(self.outer,
                                      text=title_text,
                                      font=fonts.title())

        self.Lab_PayPeriod.pack(side='top')
        title_Bbuffer.pack(side='top')

    def DeleteButton(self):
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
        except TypeError:
            if debug: pass
