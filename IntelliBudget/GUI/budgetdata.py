""" Renders all of the user's budget data. """

import tkinter as tk
from .constants import fonts, addBuffer, Field

from ..expenses import Money


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
        TotalContainer = tk.Frame(self)
        TotalContainer.pack(side='top')

        self.TotalLimit = Field()
        self.TotalLimit.const = tk.Label(TotalContainer)
        self.TotalLimit.const.text = 'TOTAL BUDGETED:   '
        self.TotalLimit.const.config(text=self.TotalLimit.const.text)
        self.TotalLimit.const.grid(row=0, column=0, sticky='W')

        self.TotalLimit.money = tk.Label(TotalContainer)
        self.TotalLimit.money.text = tk.StringVar()
        self.TotalLimit.money.config(textvariable=self.TotalLimit.money.text)
        self.TotalLimit.money.grid(row=0, column=1)

        self.TotalRem = Field()
        self.TotalRem.const = tk.Label(TotalContainer)
        self.TotalRem.const.text = 'TOTAL REMAINING:   '
        self.TotalRem.const.config(text=self.TotalRem.const.text)
        self.TotalRem.const.grid(row=1, column=0, sticky='W')

        self.TotalRem.money = tk.Label(TotalContainer)
        self.TotalRem.money.text = tk.StringVar()
        self.TotalRem.money.config(textvariable=self.TotalRem.money.text)
        self.TotalRem.money.grid(row=1, column=1)

        addBuffer(self, side='top', height=30)

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
                             font='Verdana 10 underline bold')
            EType.pack(side='top')

            LimitContainer = tk.Frame(Container)
            LimitContainer.pack(side='top')

            Limit = Field()
            Limit.const = tk.Label(LimitContainer)
            Limit.const.text = 'BUDGETED  ----> '
            Limit.const.config(text=Limit.const.text)
            Limit.const.grid(row=0, column=0, sticky='W')

            Limit.money = tk.Label(LimitContainer)
            Limit.money.text = tk.StringVar()
            Limit.money.config(textvariable=Limit.money.text)
            Limit.money.grid(row=0, column=1, sticky='E')

            Remaining = Field()
            Remaining.const = tk.Label(LimitContainer)
            Remaining.const.text = 'REMAINING  ----> '
            Remaining.const.config(text=Remaining.const.text)
            Remaining.const.grid(row=1, column=0, sticky='W')

            Remaining.money = tk.Label(LimitContainer)
            Remaining.money.text = tk.StringVar()
            Remaining.money.config(textvariable=Remaining.money.text)
            Remaining.money.grid(row=1, column=1, sticky='E')

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

        value = Money(float(TLimit))
        text = str(value)
        self.TotalLimit.money.text.set(text)

        value = Money(float(TRemaining))
        text = str(value)
        self.TotalRem.money.text.set(text)
        if float(value) < 0.0:
            self.TotalRem.money.config(fg='red')
        else:
            self.TotalRem.money.config(fg='black')

        for etype in self.parent.Budget.getExpenseTypes():
            Limit, Remaining = self.Limits[etype]
            value = Money(float(allLimits[etype][0]))
            text = str(value)
            Limit.money.text.set(text)

            value = Money(float(allLimits[etype][1]))
            text = str(value)
            Remaining.money.text.set(text)
            if float(value) < 0.0:
                Remaining.money.config(fg='red')
            else:
                Remaining.money.config(fg='black')
