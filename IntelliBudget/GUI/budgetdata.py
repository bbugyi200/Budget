""" Renders all of the user's budget data. """

import tkinter as tk
from .constants import fonts, addBuffer


class BudgetData(tk.Frame):
    def __init__(self, master, budget):
        tk.Frame.__init__(self, master)
        self.budget = budget
        self.Make()

    def Make(self):
        text = "Budget Data"
        BudgetDataTitle = tk.Label(self, text=text,
                                   font=fonts.title())
        BudgetDataTitle.pack(side='top')
        addBuffer(self, side='top', height=5)

        self.Limit = tk.Label(self)
        self.Limit.text = tk.StringVar()
        self.Limit.config(textvariable=self.Limit.text)
        self.Limit.pack(side='top')

        self.LimitRemaining = tk.Label(self)
        self.LimitRemaining.text = tk.StringVar()
        self.LimitRemaining.config(textvariable=self.LimitRemaining.text)
        self.LimitRemaining.pack(side='top')

        self.set_dynamic_data()

    def set_dynamic_data(self):
        """ Used to update or initially set the data in the Budget Data
        column.
        """
        text = 'LIMIT: {0:.2f}'.format(float(self.budget.Limit))
        self.Limit.text.set(text)

        text = 'REMAINING: {0:.2f}'.format(float(self.budget.remainingLimit))
        self.LimitRemaining.text.set(text)
