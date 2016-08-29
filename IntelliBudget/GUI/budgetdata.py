""" Renders all of the user's budget data. """

import tkinter as tk
from .constants import fonts, addBuffer


class BudgetData(tk.Frame):
    def __init__(self, master, parent):
        tk.Frame.__init__(self, master)
        self.parent = parent
        self.Make()

    def Make(self):
        text = "Budget Data"
        BudgetDataTitle = tk.Label(self, text=text,
                                   font=fonts.title())
        BudgetDataTitle.pack(side='top')
        addBuffer(self, side='top', height=5)

        # Temporary Total Frame
        # Eventually, this should be done automatically for expense types that
        # are identified as parents.
        self.TotalLimit = tk.Label(self)
        self.TotalLimit.text = tk.StringVar()
        self.TotalLimit.config(textvariable=self.TotalLimit.text)
        self.TotalLimit.pack(side='top')

        self.TotalRemaining = tk.Label(self)
        self.TotalRemaining.text = tk.StringVar()
        self.TotalRemaining.config(textvariable=self.TotalRemaining.text)
        self.TotalRemaining.pack(side='top')

        addBuffer(self, side='top', height=20)

        # This loop iterates through all of the expense types in the database
        # and creates a label for each one of them.
        self.Limits = dict()
        row = 0
        column = 0
        MasterContainer = tk.Frame(self)
        MasterContainer.pack(side='top')
        for etype in self.parent.Budget.getExpenseTypes():

            Container = tk.Frame(MasterContainer)
            Container.grid(row=row, column=column)

            EType = tk.Label(Container,
                             text=etype,
                             font='Verdana 10 underline')
            EType.pack(side='top')

            Limit = tk.Label(Container)
            Limit.text = tk.StringVar()
            Limit.config(textvariable=Limit.text)
            Limit.pack(side='top')

            Remaining = tk.Label(Container)
            Remaining.text = tk.StringVar()
            Remaining.config(textvariable=Remaining.text)
            Remaining.pack(side='top')

            self.Limits[etype] = (Limit, Remaining)

            if column == 2:
                column = 0
                row += 1
                addBuffer(MasterContainer, row=row, height=10)
                row += 1
            else:
                column = 1
                addBuffer(MasterContainer, row=row, column=column, width=10)
                column += 1

        self.set_dynamic_data()

    def set_dynamic_data(self):
        """ Used to update or initially set the data in the Budget Data
        column.
        """
        allLimits = self.parent.Budget.Limits

        # Temporary Total Dynamic Calculation
        TLimit = sum([float(allLimits[key][0]) for key in allLimits])
        TRemaining = sum([float(allLimits[key][1]) for key in allLimits])

        text = 'TOTAL LIMIT  -  ${0:.2f}'.format(float(TLimit))
        self.TotalLimit.text.set(text)

        text = 'TOTAL REMAINING  -  ${0:.2f}'.format(float(TRemaining))
        self.TotalRemaining.text.set(text)

        for etype in self.parent.Budget.getExpenseTypes():
            Limit, Remaining = self.Limits[etype]
            text = 'LIMIT - ${0:.2f}'.format(float(allLimits[etype][0]))
            Limit.text.set(text)

            text = 'REMAINING - ${0:.2f}'.format(float(allLimits[etype][1]))
            Remaining.text.set(text)
