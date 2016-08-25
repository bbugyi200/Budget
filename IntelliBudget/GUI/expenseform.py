""" Renders the Expense Form """

import tkinter as tk
import tkinter.messagebox
from .constants import fonts
from . import style as sty

class ExpenseForm(tk.Frame):
    def __init__(self, parent, master):
        tk.Frame.__init__(self, parent)

        self.master = master

        self.form = tk.Frame(self)
        self.form.pack(side='top')

        self.submit = tk.Frame(self)
        self.submit.pack(side='bottom')

        self.MakeForm()
        self.MakeSubmit()

    def MakeForm(self):
        """ Creates the form that the user uses to input a new expense into
        the database.
        """

        OPTIONS = ['Food', 'Entertainment', 'Monthly Bills', 'Fuel', 'Other']

        row = 0

        text = "New Expense"
        ExpenseFormTitle = tk.Label(self.form, text=text,
                                    font=fonts.title())
        ExpenseFormTitle.grid(row=row, columnspan=2); row += 1

        # Bottom buffer space between expense form title and the actual form
        ETitle_bbuffer = tk.Frame(self.form, height=5)
        ETitle_bbuffer.grid(row=row); row += 1

        self.expense_choice = tk.StringVar(self.form)

        # Setting the default value
        self.expense_choice.set('Food')

        self.ExpenseOptions = tk.OptionMenu(self.form, self.expense_choice, *OPTIONS)

        self.DropdownConfigs()

        # Dropdown width and expense width, respectively
        dwidth = 115
        ewidth = 18

        Lab_Expense_Type = tk.Label(self.form, text='Expense Type: ')
        Lab_Expense_Type.grid(row=row, column=0)
        self.ExpenseOptions.grid(row=row, column=1)
        row += 1

        # Amount Label
        Lab_Amount = tk.Label(self.form, text='Amount: ')
        Lab_Amount.grid(row=row, column=0)

        self.AmountEntry = tk.Entry(self.form)
        self.AmountEntry.bind('<Return>', self.SubmitFuncBind)
        self.AmountEntry.grid(row=row, column=1)
        row += 1

        Lab_Notes = tk.Label(self.form, text='Notes: ')
        Lab_Notes.grid(row=row, column=0)

        self.NotesEntry = tk.Entry(self.form)
        self.NotesEntry.bind('<Return>', self.SubmitFuncBind)
        self.NotesEntry.grid(row=row, column=1)
        row += 1

        # Set widths of all entrys and dropdowns
        self.ExpenseOptions.config(width=dwidth)
        self.AmountEntry.config(width=ewidth)
        self.NotesEntry.config(width=ewidth)

    def DropdownConfigs(self):
        """ Sets all dropdown configurations """

        arrow = tk.PhotoImage(file='img/arrow.gif')

        # Config options for the dropdown expense box
        self.ExpenseOptions.config(indicatoron=0,
                              activebackground=sty.abcolor,
                              compound='right',
                              image=arrow)

        # Needed or the image will not appear
        self.ExpenseOptions.image = arrow

        # Config options for the menu items in the dropdown expense box
        self.ExpenseOptions['menu'].config(activebackground=sty.abcolor)

    def MakeSubmit(self):
        """ Creates the Expense form Submit button """

        # submit_Tbuffer is used to create vertical space between the submit
        # button and the expense form.
        submit_Tbuffer = tk.Frame(self.submit, height=15)
        submit_Tbuffer.pack(side='top')

        # submit_Lbuffer is used to create horizontal space between the submit
        # button and the expense list.
        submit_Lbuffer = tk.Frame(self.submit, width=100)
        submit_Lbuffer.pack(side='left')

        SubmitButton = tk.Button(self.submit,
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
            self.master.Budget.add_expense('DATE', self.expense_choice.get(),
                                    self.AmountEntry.get(),
                                    self.NotesEntry.get())

            self.AmountEntry.delete(0, 'end')
            self.NotesEntry.delete(0, 'end')

            self.master.refresh_screen()

        except AttributeError:
            tkinter.messagebox.showinfo("ERROR",
                                        "You must select an expense type!")
            raise

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
