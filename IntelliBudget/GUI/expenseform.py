""" Renders the Expense Form """

import tkinter as tk
import tkinter.messagebox
from .constants import fonts, Field, addBuffer, debug
from . import style as sty
from .. import dates


class ExpenseForm(tk.Frame):
    def __init__(self, parent, master):
        tk.Frame.__init__(self, parent)

        self.master = master

        self.topFrame = tk.Frame(self)
        self.topFrame.pack(side='top')

        self.bottomFrame = tk.Frame(self)
        self.bottomFrame.pack(side='bottom')

        self.Make()

    def Make(self):
        """ Creates the form that the user uses to input a new expense into
        the database.
        """

        text = "New Expense"
        ExpenseFormTitle = tk.Label(self.topFrame, text=text,
                                    font=fonts.title())
        ExpenseFormTitle.pack(side='top')

        addBuffer(self.topFrame, side='top', height=5)

        # Dropdown width and expense width, respectively
        dwidth = 115
        ewidth = 18

        FormFrame = tk.Frame(self.topFrame)
        FormFrame.pack(side='top')
        FormFrame.row = 0

        # Setup for the ExpenseType OptionMenu
        OPTIONS = self.master.Budget.getExpenseTypes()
        self.expense_choice = tk.StringVar()
        self.expense_choice.set('Food')  # Setting the default value

        self.ExpenseType = Field()
        self.ExpenseType.label = tk.Label(FormFrame, text='Expense Type: ')
        self.ExpenseType.label.grid(row=FormFrame.row, column=0)
        self.ExpenseType.OptionMenu = tk.OptionMenu(FormFrame,
                                                    self.expense_choice,
                                                    *OPTIONS)
        self.ExpenseType.OptionMenu.grid(row=FormFrame.row, column=1)
        self.DropdownConfigs()
        FormFrame.row += 1

        self.Amount = Field()
        self.Amount.label = tk.Label(FormFrame, text='Amount: ')
        self.Amount.label.grid(row=FormFrame.row, column=0)
        self.Amount.entry = tk.Entry(FormFrame)
        self.Amount.entry.bind('<Return>', self.SubmitFuncBind)
        self.Amount.entry.grid(row=FormFrame.row, column=1)
        FormFrame.row += 1

        self.Notes = Field()
        self.Notes.label = tk.Label(FormFrame, text='Notes: ')
        self.Notes.label.grid(row=FormFrame.row, column=0)
        self.Notes.entry = tk.Entry(FormFrame)
        self.Notes.entry.bind('<Return>', self.SubmitFuncBind)
        self.Notes.entry.grid(row=FormFrame.row, column=1)
        FormFrame.row += 1

        # Set widths of all entrys and dropdowns
        self.ExpenseType.OptionMenu.config(width=dwidth)
        self.Amount.entry.config(width=ewidth)
        self.Notes.entry.config(width=ewidth)

        self.CreateSubmitButton()

    def DropdownConfigs(self):
        """ Sets all dropdown configurations """

        arrow = tk.PhotoImage(file='img/arrow.gif')

        # Config options for the dropdown expense box
        self.ExpenseType.OptionMenu.config(indicatoron=0,
                                           activebackground=sty.abcolor,
                                           compound='right',
                                           image=arrow)

        # Needed or the image will not appear
        self.ExpenseType.OptionMenu.image = arrow

        # Config options for the menu items in the dropdown expense box
        self.ExpenseType.OptionMenu['menu'].config(activebackground=sty.abcolor)

    def CreateSubmitButton(self):
        """ Creates the Expense form Submit button """

        addBuffer(self.bottomFrame, side='top', height=15)
        addBuffer(self.bottomFrame, side='left', width=100)

        SubmitButton = tk.Button(self.bottomFrame,
                                 text='Submit',
                                 activebackground=sty.abcolor,
                                 command=self.SubmitFunc,
                                 font=fonts.button())
        SubmitButton.pack()

    def SubmitFunc(self):
        """ This function is called if the Expense form's 'Submit' button
        is pressed.
        """
        try:
            # Today's date
            date = dates.today.strftime('%m-%d-%y')

            self.master.Budget.add_expense(date, self.expense_choice.get(),
                                           self.Amount.entry.get(),
                                           self.Notes.entry.get())

            self.Amount.entry.delete(0, 'end')
            self.Notes.entry.delete(0, 'end')

            self.master.refresh_screen()

        # Catches error if user enters string into 'Value' entrybox
        except ValueError:
            message = "The formatting of this entry is invalid!"
            tkinter.messagebox.showinfo("ERROR", message)

            raise

    def SubmitFuncBind(self, event):
        """ Used to allow 'Entry' widgets to bind to the SubmitFunc. Binded
        widgets require that the function they are binded to have an 'event'
        argument.
        """
        self.SubmitFunc()
