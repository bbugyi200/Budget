""" GUI.py

All classes and functions that are related to the tkinter GUI should be
stored in this module.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from .. import bdata
from ..bdata import NoData
from .. import bdates
from .. import payperiod

# Style imports
from . import style as sty
from .style import width, height, abcolor

fonts = sty.Fonts()


class B_GUI_Setup:
    """ B_GUI_Setup Class

    This class contains all of the methods that are used for the initial
    setup of the main Budget GUI window.
    """

    def __init__(self, master):
        try:
            self.PP = bdata.GetPayPeriod()

        # If the 'data/' folder is empty, a default PayPeriod is created
        # and subsequently the 'FirstUse()' function is later called.
        except NoData:
            self.PP = payperiod.PayPeriod(0, 'First Pay Period')

        self.master = master
        master.title('The Budget Program - (' + self.PP.StartDate + ')')

        self._createMenu(master)

        row = 0

        self.topFrame = tk.Frame(master)
        self.topFrame.grid(row=row, columnspan=5); row += 1

        self._createTopTitle(self.topFrame)

        # frame1 is the leftmost frame
        self.frame1 = tk.Frame(master, width=700, height=200)
        self.frame1.grid(row=row, column=0)

        self.frame1_Lbuffer = tk.Frame(self.frame1, width=width)
        self.frame1_Lbuffer.grid()
        self.frame1_Rbuffer = tk.Frame(self.frame1, width=width)
        self.frame1_Rbuffer.grid(column=100)

        self.data_frame = tk.Frame(self.frame1)
        self.data_frame.grid(row=0, column=1)
        self.calculate_data(self.data_frame)

        self.frame2 = tk.Frame(master)
        self.frame2.grid(row=row, column=1)

        self._showExpenses(self.frame2)

        self.frame3 = tk.Frame(master, width=200, height=200)
        self.frame3.grid(row=row, column=2)

        # Left buffer for fframe3
        self.frame3_Lbuffer = tk.Frame(self.frame3, width=width)
        self.frame3_Lbuffer.grid()

        # Right buffer for fframe3
        self.frame3_Rbuffer = tk.Frame(self.frame3, width=width)
        self.frame3_Rbuffer.grid(column=100)

        # frame3 is used for the Expense form
        self.form_frame = tk.Frame(self.frame3)
        self.form_frame.grid(row=0, column=1)
        self._createExpenseForm(self.form_frame)

        # frame3 is used for Submit button.
        # Spacing is added by creating multiple inner frames within frame3.
        self.submit_frame = tk.Frame(self.frame3)
        self.submit_frame.grid(row=1, column=1)
        self._createSubmit(self.submit_frame)

        # Recognizes that there is no payperiod data and asks user to setup
        # first payperiod.
        if self.PP.StartDate == 'First Pay Period':
            self.FirstUse()

        master.mainloop()

    def _createTopTitle(self, frame):
        TopTitle = tk.Label(frame,
                            text='The Budget Program',
                            font='Verdana 40 underline')
        TopTitle.pack(side='top')
        TT_bbuffer = tk.Frame(frame, height=20)
        TT_bbuffer.pack(side='bottom')

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

    def calculate_data(self, frame):
        """ Used to create the 'initial' and 'remaining' fields of the given
        pay period.
        """
        row = 0

        text = "Budget Data"
        BudgetDataTitle = tk.Label(frame, text=text,
                                   font=fonts.title())
        BudgetDataTitle.grid(row=row); row += 1

        # Bottom buffer space between title and the rest of the data
        BTitle_bbuffer = tk.Frame(frame, height=5)
        BTitle_bbuffer.grid(row=row); row += 1

        self.Lab_initial_text = tk.StringVar()
        self.Lab_initial_text.set('Initial: ' +
                                  '{0:.2f}'.format(float(self.PP.initial)))
        self.Lab_remaining_text = tk.StringVar()
        self.Lab_remaining_text.set('Remaining: ' +
                                    '{0:.2f}'.format(float(self.PP.remaining)))

        self.Lab_initial = tk.Label(frame, textvariable=self.Lab_initial_text)
        self.Lab_initial.grid(row=row); row += 1

        self.Lab_remaining = tk.Label(frame,
                                      textvariable=self.Lab_remaining_text)
        self.Lab_remaining.grid(row=row); row += 1

    def _createExpenseForm(self, frame):
        """ Creates the form that the user uses to input a new expense into
        the database.
        """
        OPTIONS = ['Food', 'Entertainment', 'Monthly Bills', 'Fuel', 'Other']

        frame = tk.Frame(frame)
        frame.grid(row=0, column=1)

        row = 0

        text = "New Expense"
        ExpenseFormTitle = tk.Label(frame, text=text,
                                    font=fonts.title())
        ExpenseFormTitle.grid(row=row, columnspan=2); row += 1

        # Bottom buffer space between expense form title and the actual form
        ETitle_bbuffer = tk.Frame(frame, height=5)
        ETitle_bbuffer.grid(row=row); row += 1

        self.expense_choice = tk.StringVar(frame)

        # Setting the default value
        self.expense_choice.set('Food')

        ExpenseOptions = tk.OptionMenu(frame, self.expense_choice, *OPTIONS)

        def DropdownConfigs():
            """ Sets all dropdown configurations """

            arrow = tk.PhotoImage(file='img/arrow.gif')

            # Config options for the dropdown expense box
            ExpenseOptions.config(indicatoron=0,
                                  activebackground=abcolor,
                                  compound='right',
                                  image=arrow)

            # Needed or the image will not appear
            ExpenseOptions.image = arrow

            # Config options for the menu items in the dropdown expense box
            ExpenseOptions['menu'].config(activebackground=abcolor)

        DropdownConfigs()

        # Dropdown width and expense width, respectively
        dwidth = 115
        ewidth = 18

        Lab_Expense_Type = tk.Label(frame, text='Expense Type: ')
        Lab_Expense_Type.grid(row=row, column=0)
        ExpenseOptions.grid(row=row, column=1)
        row += 1

        # Amount Label
        Lab_Amount = tk.Label(frame, text='Amount: ')
        Lab_Amount.grid(row=row, column=0)

        self.ValueEntry = tk.Entry(frame)
        self.ValueEntry.bind('<Return>', self.SubmitFuncBind)
        self.ValueEntry.grid(row=row, column=1)
        row += 1

        Lab_Notes = tk.Label(frame, text='Notes: ')
        Lab_Notes.grid(row=row, column=0)

        self.NotesEntry = tk.Entry(frame)
        self.NotesEntry.bind('<Return>', self.SubmitFuncBind)
        self.NotesEntry.grid(row=row, column=1)
        row += 1

        # Set widths of all entrys and dropdowns
        ExpenseOptions.config(width=dwidth)
        self.ValueEntry.config(width=ewidth)
        self.NotesEntry.config(width=ewidth)

    def _createSubmit(self, frame):
        """ Creates the Expense form Submit button """

        # submit_Tbuffer is used to create vertical space between the submit
        # button and the expense form.
        submit_Tbuffer = tk.Frame(frame, height=15)
        submit_Tbuffer.grid(row=0, column=1)

        # submit_Lbuffer is used to create horizontal space between the submit
        # button and the expense list.
        submit_Lbuffer = tk.Frame(frame, width=100)
        submit_Lbuffer.grid(row=1, column=0)

        # In order to have complete control of the Submit button's horizontal
        # positioning, the columns of frame3 must be seperate from the columns
        # in the Submit button's encapsulating frame. The submit_container
        # fulfills this purpose.
        submit_container = tk.Frame(frame)
        submit_container.grid(row=1, column=1)

        SubmitButton = tk.Button(submit_container,
                                 text='Submit',
                                 activebackground=abcolor,
                                 command=self.SubmitFunc,
                                 font=fonts.button())
        SubmitButton.grid()

    def _showExpenses(self, frame):
        """ Displays all of this pay period's expenses. """

        # If the ExpenseFrame exists, it will be destroyed
        try:
            self.outer_expense_frame.destroy()
        except AttributeError:
            pass

        # outer_expense_frame is created so the delete button frames can be
        # seperated visually from the expense list frame.
        self.outer_expense_frame = tk.Frame(frame)
        self.outer_expense_frame.pack()

        def createTitle(frame):
            title_Bbuffer = tk.Frame(frame, height=5)

            title_text = "Expense List"
            self.Lab_PayPeriod = tk.Label(frame,
                                          text=title_text,
                                          font=fonts.title())

            self.Lab_PayPeriod.pack(side='top')
            title_Bbuffer.pack(side='top')

        createTitle(self.outer_expense_frame)

        self.ExpenseFrame = tk.Frame(self.outer_expense_frame)
        self.ExpenseFrame.pack(fill='both')

        Exp_Attrs = self.PP.expenses.get()

        # Debugging Assistance
        assert True, print(Exp_Attrs)

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

        # Inserts each expense into the Treeview object
        for item in Exp_Attrs:
            self.tree.insert('', 'end', values=item)

        # 'yscroll' option must be set to scrollbar set object
        self.tree['yscroll'] = scrollbar.set

        self.tree.pack(side='left', fill='both')

        # Associates scrollbar with the Treeview object
        scrollbar.config(command=self.tree.yview)

        def Create_Delete_Button():
            """ Creates a delete button and adds extra vertical space
            between the button and the expense list
            """

            # Outer frame that hold delete button and buffer space
            outer_delete_frame = tk.Frame(self.outer_expense_frame)
            outer_delete_frame.pack(side='bottom')

            # Buffer space between the button and the expense list
            delete_Tbuffer = tk.Frame(outer_delete_frame, height=height)
            delete_Tbuffer.pack(side='top')

            delete_Bbuffer = tk.Frame(outer_delete_frame, height=height)
            delete_Bbuffer.pack(side='bottom')

            # This frame will hold the actual delete button
            delete_frame = tk.Frame(outer_delete_frame)
            delete_frame.pack()

            delete_button = tk.Button(delete_frame,
                                      text='Delete Selected',
                                      activebackground=abcolor,
                                      command=self.DeleteSelected,
                                      font=fonts.button())
            delete_button.pack()

        Create_Delete_Button()

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

            self.refresh_screen()
            bdata.SavePP(self.PP)

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

    def newPP(self):
        """ Creates a new GUI window that prompts the user for the new
        pay period's information.
        """

        self.NPP_root = tk.Tk()

        topFrame = tk.Frame(self.NPP_root)
        topFrame.grid(row=0)

        StartPPLabel = tk.Label(topFrame,
                                text="Start of PayPeriod",
                                font=fonts.title())
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

        submit_button = tk.Button(bottomFrame,
                                  text='Submit',
                                  command=self._SubmitNewPP,
                                  font=fonts.button())
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
        self.master.title('The Budget Program - (' + self.PP.StartDate + ')')
        self.Lab_initial_text.set('Initial: ' +
                                  '{0:.2f}'.format(float(self.PP.initial)))
        self.Lab_remaining_text.set('Remaining: ' +
                                    '{0:.2f}'.format(float(self.PP.remaining)))
        self._showExpenses(self.frame2)

    def DeleteSelected(self):
        """ This function is called when the user presses the
        Expense form's 'Delete Selected' button.
        """
        index = None
        try:
            # Sets index to the offset of the selected item in the expense list
            for i, item in enumerate(self.tree.get_children()):
                if item == self.tree.focus():
                    index = i

            # Deletes the expense at the specified index
            self.PP.remove_expense(index)
            self.refresh_screen()
            bdata.SavePP(self.PP)

        # Does nothing if 'Delete Selected' button is clicked when no item is
        # selected.
        except TypeError:
            pass

    def FirstUse(self):
        """ This function welcomes a new user to the program and then prompts
        him to setup his first PayPeriod.
        """
        message = "Welcome to the Budget Program!" \
                  "\n\nLet's setup your first pay period!"
        tkinter.messagebox.showinfo("WELCOME!", message)
        self.newPP()
