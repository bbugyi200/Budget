""" This is a Graphical Budget Program  """

import tkinter as tk
import tkinter.messagebox
import bdata
import bdates
import payperiod


class B_GUI_Setup:
    def __init__(self, master):
        self.PP = bdata.GetPayPeriod()

        self._createMenu(master)

        self.frame1 = tk.Frame(master, width=50, height=100)
        self.frame1.grid(row=0, columnspan=5)

        self._createTitle(self.frame1)

        self.frame2 = tk.Frame(master, width=700, height=200)
        self.frame2.grid(row=1, column=0)

        self._createIR(self.frame2)

        self.frame3 = tk.Frame(master, width=200, height=100)
        self.frame3.grid(row=1, column=2)

        self._createExpenseForm(self.frame3)

        self.SubmitFrame = tk.Frame(master)
        self.SubmitFrame.grid(row=2, column=2)

        self._createSubmit(self.SubmitFrame)

        self.OuterEFrame = tk.Frame(master)
        self.OuterEFrame.grid(row=1, column=1)

        self._showExpenses(self.OuterEFrame)

    def _createMenu(self, master):
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
        def GetPP():
            self.PP = bdata.GetPayPeriod(date)
            self.refresh_screen()
        return GetPP

    def _createTitle(self, frame):
        self.Lab_PayPeriod_Text = tk.StringVar()
        self.Lab_PayPeriod_Text.set(self.PP.StartDate)
        self.Lab_PayPeriod = tk.Label(frame,
                textvariable=self.Lab_PayPeriod_Text,
                width=50,
                font='Verdana 15 underline')

        self.Lab_PayPeriod.grid(row=2, column=3)

    def _createIR(self, frame):
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
        OPTIONS = ['Food', 'Entertainment', 'Monthly Bills', 'Fuel', 'Other']

        self.expense_choice = tk.StringVar(frame)
        # Setting the default value
        self.expense_choice.set('Expense')

        ExpenseOptions = tk.OptionMenu(frame, self.expense_choice, *OPTIONS)
        ExpenseOptions.grid(row=0)

        Lab_Amount = tk.Label(frame, text='Amount: ')
        Lab_Amount.grid(row=0, column=1)

        self.ValueEntry = tk.Entry(frame)
        self.ValueEntry.bind('<Return>', self.SubmitFunc)
        self.ValueEntry.grid(row=0, column=2)

        Lab_Notes = tk.Label(frame, text='Notes: ')
        Lab_Notes.grid(row=1, column=1)

        self.NotesEntry = tk.Entry(frame)
        self.NotesEntry.bind('<Return>', self.SubmitFunc)
        self.NotesEntry.grid(row=1, column=2)

    def _createSubmit(self, frame):
        SubmitButton = tk.Button(frame, text='Submit')
        SubmitButton.bind('<Button-1>', self.SubmitFunc)
        SubmitButton.pack()

    def _showExpenses(self, outer_frame):
        try:
            self.ExpenseFrame.destroy()
        except AttributeError:
            pass

        self.ExpenseFrame = tk.Frame(outer_frame)
        self.ExpenseFrame.pack(fill='both')

        Exp_Attrs = self.PP.expenses.get()
        print(Exp_Attrs)

        self.expense_checkboxes = []
        for i, Exp in enumerate(Exp_Attrs):
            self.expense_checkboxes.append(tk.IntVar())

            labelText = ' - '.join(Exp)
            Lab_Expense = tk.Checkbutton(self.ExpenseFrame, text=labelText,
                                font='Helvetica 10',
                                variable=self.expense_checkboxes[i])
            Lab_Expense.pack(side='top')

        deleteButton = tk.Button(self.ExpenseFrame, text="Delete Selected")
        deleteButton.bind('<Button-1>', self.DeleteSelected)
        deleteButton.pack(side='bottom')


    def SubmitFunc(self):
        assert False, "The SubmitFunc function must be overloaded!"

    def newPP(self):
        assert False, "The newPP function must be overloaded!"

    def refresh_screen(self):
        assert False, "The refresh_screen function must be overloaded!"

    def DeleteSelected(self):
        assert False, "The DeleteSelected function must be overloaded!"


class BudgetGUI(B_GUI_Setup):
    def SubmitFunc(self, event):
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

    def newPP(self):
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

        submit_button = tk.Button(bottomFrame, text='Submit')
        submit_button.bind('<Button-1>', self._SubmitNewPP)
        submit_button.pack()

        self.NPP_root.mainloop()

    def _SubmitNewPP(self, event):
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
        self.Lab_PayPeriod_Text.set(self.PP.StartDate)
        self.Lab_initial_text.set('Initial: ' + '{0:.2f}'.format(float(self.PP.initial)))
        self.Lab_remaining_text.set('Remaining: ' + '{0:.2f}'.format(float(self.PP.remaining)))
        self._showExpenses(self.OuterEFrame)

    def DeleteSelected(self, event):
        deleted_count = 0
        for i, checkbox in enumerate(self.expense_checkboxes):
            if checkbox.get():
                self.PP.remove_expense(i - deleted_count)
                deleted_count += 1
        self.refresh_screen()
        bdata.SavePP(self.PP)



if __name__ == '__main__':
    root = tk.Tk()

    myGUI = BudgetGUI(root)

    root.mainloop()