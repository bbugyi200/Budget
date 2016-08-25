import tkinter as tk

from .constants import MONTH, fonts

from .. import dates
from .. import budget


class Menu():
    def __init__(self, parent):
        self.parent = parent
        self.BuildMenu()

    def BuildMenu(self):
        """ Creates dropdown menus on the top of the window """
        menu = tk.Menu(self.parent)
        self.parent.master.config(menu=menu)

        fileMenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='Update Limits', command=self.newLimits)
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

    def newLimits(self):
        """ Creates a new GUI window that prompts the user for the new
        Budget information.
        """

        # Toplevel can be used just like tk.Tk() but it associates the
        # new widget to the original master.
        self.NewMonthRoot = tk.Toplevel(master=self.parent)
        self.NewMonthRoot.title(MONTH + ' - Limit Form')

        TopFrame = tk.Frame(self.NewMonthRoot)
        TopFrame.grid(row=0)

        row = 0
        WindowTitle = tk.Label(TopFrame,
                               text="Spending Limits",
                               font=fonts.title())
        WindowTitle.grid(row=row, columnspan=5); row += 1

        WindowTitleBuffer = tk.Frame(TopFrame, height=10)
        WindowTitleBuffer.grid(row=row); row += 1

        TLimLabel = tk.Label(TopFrame, text="Total Limit: ")
        TLimLabel.grid(row=row)

        self.TLimEntry = tk.Entry(TopFrame)
        self.TLimEntry.grid(row=row, column=1); row += 1

        bottomFrame = tk.Frame(self.NewMonthRoot)
        bottomFrame.grid(row=1, columnspan=5)

        # Adds space between submit button and top Entry boxes
        submitBuffer = tk.Frame(bottomFrame, height=10)
        submitBuffer.pack(side='top')

        submit_button = tk.Button(bottomFrame,
                                  text='Submit',
                                  command=self.SubmitNewLimits,
                                  font=fonts.button())
        submit_button.pack()

    def SubmitNewLimits(self):
        """ This function is called when the user submits the NewPP
        information.
        """
        TotalLimit = self.TLimEntry.get()

        self.parent.Budget.updateLimits(TotalLimit)

        self.parent.refresh_screen()
        self.NewMonthRoot.destroy()
