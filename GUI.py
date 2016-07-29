""" GUI.py

All classes and functions that are related to the tkinter GUI should be
stored in this module.
"""

import tkinter as tk
import tkinter.messagebox
import bdata
import bdates
import payperiod
from bdata import NoData


class B_GUI_Setup:
    """ B_GUI_Setup Class
    
    This class contains all of the methods that are used for the initial 
    setup of the main Budget GUI window.
    """

    def __init__(self, master):
        """ Initializes the GUI """
        try:
            self.PP = bdata.GetPayPeriod()

        # If the 'data/' folder is empty, a default PayPeriod is created
        # and subsequently the 'FirstUse()' function is later called.
        except NoData:
            self.PP = payperiod.PayPeriod(0, 'First Pay Period')


        self._createMenu(master)

        self.frame1 = tk.Frame(master, width=50, height=100)
        self.frame1.grid(row=0, columnspan=5)

        # frame1 is used for the window title
        self._createTitle(self.frame1)

        self.frame2 = tk.Frame(master, width=700, height=200)
        self.frame2.grid(row=1, column=0)

        # frame2 is used for the initial and remaining amounts
        self._createIR(self.frame2)

        self.frame3 = tk.Frame(master, width=200, height=100)
        self.frame3.grid(row=1, column=2)

        # frame3 is used for the Expense form
        self._createExpenseForm(self.frame3)

        self.SubmitFrame = tk.Frame(master)
        self.SubmitFrame.grid(row=2, column=2)

        # SubmitFrame is used for the 'Submit' button of the Expense form
        self._createSubmit(self.SubmitFrame)

        self.OuterEFrame = tk.Frame(master)
        self.OuterEFrame.grid(row=1, column=1)

        # The OuterEFrame is used to display the expenses and is an "outer"
        # frame so the inner frame can be deleted as needed without affecting
        # the outer frame.
        self._showExpenses(self.OuterEFrame)

        if self.PP.StartDate=='First Pay Period':
            self.FirstUse()

        master.mainloop()

    def _createMenu(self, master):
        """ Creates dropdown menus on the top of the window """
        menu = tk.Menu(master)
        master.config(menu=menu)

        fileMenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='New Pay Period..', command=self.newPP)
        fileMenu.add_separator()
        fileMenu.add_command(label='Quit', command=master.quit)

        viewMenu = tk.Menu(menu)
        menu.add_cascade(label='Pay Periods', menu=viewMenu)

        for date in bdates.getPP_files()[-1:-10:-1]:
            viewMenu.add_command(label=date, command=self._GetPPFactory(date))

    def _GetPPFactory(self, date):
        """ Returns a function ('GetPP') that changes the PP object and then
        refreshes the screen.
        """
        def GetPP():
            self.PP = bdata.GetPayPeriod(date)
            self.refresh_screen()
        return GetPP

    def _createTitle(self, frame):
        """ Creates the title of the window, which is just the pay period
        date.
        """
        self.Lab_PayPeriod_Text = tk.StringVar()
        self.Lab_PayPeriod_Text.set(self.PP.StartDate)
        self.Lab_PayPeriod = tk.Label(frame,
                textvariable=self.Lab_PayPeriod_Text,
                width=50,
                font='Verdana 15 underline')

        self.Lab_PayPeriod.grid(row=2, column=3)

    def _createIR(self, frame):
        """ Used to create the 'initial' and 'remaining' fields of the given
        pay period.
        """
        self.Lab_initial_text = tk.StringVar()
        self.Lab_initial_text.set('Initial: ' + '{0:.2f}'.format(float(self.PP.initial)))
        self.Lab_remaining_text = tk.StringVar()
        self.Lab_remaining_text.set('Remaining: ' + '{0:.2f}'.format(float(self.PP.remaining)))

        self.Lab_initial = tk.Label(frame, textvariable=self.Lab_initial_text)
        self.Lab_initial.grid(row=0)

        self.Lab_remaining = tk.Label(frame,
                             textvariable=self.Lab_remaining_text)
        self.Lab_remaining.grid(row=1)

    def _createExpenseForm(self, frame):
        """ Creates the form that the user uses to input a new expense into
        the database.
        """
        OPTIONS = ['Food', 'Entertainment', 'Monthly Bills', 'Fuel', 'Other']

        self.expense_choice = tk.StringVar(frame)

        # Setting the default value
        self.expense_choice.set('Expense')

        ExpenseOptions = tk.OptionMenu(frame, self.expense_choice, *OPTIONS)
        ExpenseOptions.grid(row=0)

        # Amount Label
        Lab_Amount = tk.Label(frame, text='Amount: ')
        Lab_Amount.grid(row=0, column=1)

        self.ValueEntry = tk.Entry(frame)
        self.ValueEntry.bind('<Return>', self.SubmitFuncBind)
        self.ValueEntry.grid(row=0, column=2)

        Lab_Notes = tk.Label(frame, text='Notes: ')
        Lab_Notes.grid(row=1, column=1)

        self.NotesEntry = tk.Entry(frame)
        self.NotesEntry.bind('<Return>', self.SubmitFuncBind)
        self.NotesEntry.grid(row=1, column=2)

    def _createSubmit(self, frame):
        """ Creates the Expense form Submit button """
        SubmitButton = tk.Button(frame, text='Submit', command=self.SubmitFunc)
        SubmitButton.pack()

    def _showExpenses(self, outer_frame):
        """ Displays all of this pay period's expenses. """

        # If the ExpenseFrame exists, it will be destroyed
        try:
            self.ExpenseFrame.destroy()
        except AttributeError:
            pass

        self.ExpenseFrame = tk.Frame(outer_frame)
        self.ExpenseFrame.pack(fill='both')

        Exp_Attrs = self.PP.expenses.get()

        # Debugging Assistance
        assert True, print(Exp_Attrs)

        self.expense_checkboxes = []

        # The expense_checkboxes list is used to store the status of an
        # arbitrary amount of checkboxes.
        for i, Exp in enumerate(Exp_Attrs):
            self.expense_checkboxes.append(tk.IntVar())

            labelText = ' - '.join(Exp)
            Lab_Expense = tk.Checkbutton(self.ExpenseFrame, text=labelText,
                                font='Helvetica 10',
                                variable=self.expense_checkboxes[i])
            Lab_Expense.pack(side='top')

        deleteButton = tk.Button(self.ExpenseFrame, text="Delete Selected",
                command=self.DeleteSelected)
        deleteButton.pack(side='bottom')


    ########################
    #   Abstract Methods   #
    ########################


    def SubmitFunc(self):
        assert False, "The SubmitFunc function must be overloaded!"

    def SubmitFuncBind(self):
        assert False, "The SubmitFuncBind function must be overloaded!"

    def newPP(self):
        assert False, "The newPP function must be overloaded!"

    def refresh_screen(self):
        assert False, "The refresh_screen function must be overloaded!"

    def DeleteSelected(self):
        assert False, "The DeleteSelected function must be overloaded!"

    def FirstUse(self):
        assert False, "The FirstUse function must be overloaded!"


class BudgetGUI(B_GUI_Setup):
    """ BudgetGUI Class
    
    Contains all of the "dynamic" functionality of the GUI.
    """

    def SubmitFunc(self):
        """ This function is called if the Expense form's 'Submit' button
        is pressed.
        """
        try:
            self.PP.add_expense(self.expense_choice.get(),
                    self.ValueEntry.get(),
                    self.NotesEntry.get())

            self.ValueEntry.delete(0, 'end')
            self.NotesEntry.delete(0, 'end')

            self._createIR(self.frame2)
            self._showExpenses(self.OuterEFrame)
            bdata.SavePP(self.PP)
        except TypeError:
            tkinter.messagebox.showinfo("ERROR",
                                        "You must select an expense type!")
            raise
    
    def SubmitFuncBind(self, event):
        """ Used to allow 'Entry' widgets to bind to the SubmitFunc. Binded
        widgets require that the function they are binded to have an 'event'
        argument.
        """
        self.SubmitFunc()

    def newPP(self):
        """ Creates a new GUI window that prompts the user for the new
        pay period's information.
        """

        self.NPP_root = tk.Tk()

        topFrame = tk.Frame(self.NPP_root)
        topFrame.grid(row=0)

        StartPPLabel = tk.Label(topFrame, text="Start of PayPeriod", font='Verdana 14 underline')
        StartPPLabel.grid(row=0, columnspan=5)

        leftFrame = tk.Frame(self.NPP_root)
        leftFrame.grid(row=1)

        month_label = tk.Label(leftFrame, text="Month: ")
        month_label.grid(row=1)
        self.month_entry = tk.Entry(leftFrame)
        self.month_entry.grid(row=1, column=1)

        day_label = tk.Label(leftFrame, text="Day: ")
        day_label.grid(row=2)
        self.day_entry = tk.Entry(leftFrame)
        self.day_entry.grid(row=2, column=1)

        year_label = tk.Label(leftFrame, text="Year: ")
        year_label.grid(row=3)
        self.year_entry = tk.Entry(leftFrame)
        self.year_entry.grid(row=3, column=1)

        rightFrame = tk.Frame(self.NPP_root)
        rightFrame.grid(row=1, column=1)

        paycheck_label = tk.Label(rightFrame, text='Paycheck Value: ')
        paycheck_label.grid(row=0)
        self.paycheck_entry = tk.Entry(rightFrame)
        self.paycheck_entry.grid(row=0, column=1)

        bottomFrame = tk.Frame(self.NPP_root)
        bottomFrame.grid(row=2)

        submit_button = tk.Button(bottomFrame, text='Submit', command=self._SubmitNewPP)
        submit_button.pack()

        self.NPP_root.mainloop()

    def _SubmitNewPP(self):
        """ This function is called when the user submits the NewPP 
        information.
        """
        M, D, Y = (self.month_entry.get(),
                self.day_entry.get(),
                self.year_entry.get())

        M, D, Y = int(M), int(D), int(Y[-2:])

        StartDate = '{0:02d}-{1:02d}-{2}'.format(M, D, Y)

        NEWPP = payperiod.PayPeriod(self.paycheck_entry.get(), StartDate)

        bdata.SavePP(NEWPP)
        self.PP = NEWPP

        self.refresh_screen()

        self.NPP_root.destroy()

    def refresh_screen(self):
        """ This function is used to refresh the main GUI window. """
        self.Lab_PayPeriod_Text.set(self.PP.StartDate)
        self.Lab_initial_text.set('Initial: ' + '{0:.2f}'.format(float(self.PP.initial)))
        self.Lab_remaining_text.set('Remaining: ' + '{0:.2f}'.format(float(self.PP.remaining)))
        self._showExpenses(self.OuterEFrame)

    def DeleteSelected(self):
        """ This function is called when the user presses the
        Expense form's 'Delete Selected' button.
        """
        deleted_count = 0
        for i, checkbox in enumerate(self.expense_checkboxes):
            if checkbox.get():
                self.PP.remove_expense(i - deleted_count)
                deleted_count += 1
        self.refresh_screen()
        bdata.SavePP(self.PP)

    def FirstUse(self):
        """ This function welcomes a new user to the program and then prompts
        him to setup his first PayPeriod.
        """
        tkinter.messagebox.showinfo("WELCOME!",
                "Welcome to the Budget Program!" 
                "\n\nLet's setup your first pay period!")
        self.newPP()




if __name__ == '__main__':
    root = tk.Tk()

    myGUI = BudgetGUI(root)
