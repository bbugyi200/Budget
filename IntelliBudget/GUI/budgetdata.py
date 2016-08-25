""" Renders all of the user's budget data. """

import tkinter as tk
from .constants import fonts

class BudgetData(tk.Frame):
    def __init__(self, master, budget):
        tk.Frame.__init__(self, master)
        self.budget = budget
        self.Make()

    def Make(self):
        row = 0

        text = "Budget Data"
        BudgetDataTitle = tk.Label(self, text=text,
                                   font=fonts.title())
        BudgetDataTitle.grid(row=row); row += 1

        # Bottom buffer space between title and the rest of the data
        BTitle_bbuffer = tk.Frame(self, height=5)
        BTitle_bbuffer.grid(row=row); row += 1

        # The dynamic textvariables
        self.Lab_initial_text = tk.StringVar()
        self.Lab_remaining_text = tk.StringVar()
        self.SL_text = tk.StringVar()
        self.RL_text = tk.StringVar()

        self.set_dynamic_data()

        self.Lab_initial = tk.Label(self, textvariable=self.Lab_initial_text)
        self.Lab_initial.grid(row=row); row += 1

        self.Lab_remaining = tk.Label(self,
                                      textvariable=self.Lab_remaining_text)
        self.Lab_remaining.grid(row=row); row += 1

        # Spending Limit Top Buffer
        SL_Tbuffer = tk.Frame(self, height=10)
        SL_Tbuffer.grid(row=row); row += 1

        spending_limit = tk.Label(self, textvariable=self.SL_text)
        spending_limit.grid(row=row); row += 1
        remaining_limit = tk.Label(self, textvariable=self.RL_text)
        remaining_limit.grid(row=row); row += 1

    def set_dynamic_data(self):
        """ Used to update or initially set the data in the Budget Data
        column.
        """
        self.Lab_initial_text.set('LIMIT: ' +
                                  '{0:.2f}'.format(float(self.budget.Limit)))
        self.Lab_remaining_text.set('REMAINING: ' +
                                    '{0:.2f}'.format(float(self.budget.remainingLimit)))
