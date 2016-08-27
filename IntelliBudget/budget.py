""" budget.py

This module focuses on objects that represent more holistic models
of a single pay cycle.
"""

from . import expenses
from .data.SQLDB import SQLDB


class NoneNotAllowed(Exception): pass


class Budget:
    """ Budget object is used to handle budget operations. """
    def __init__(self, limit=None, DB=None):
        if not DB:
            self.DB = SQLDB()
        else:
            self.DB = SQLDB(DB)

        self.getLimits(limit)
        self.expenses = Expense_List(self.DB)

    def __getattr__(self, method):
        """ __getattr__ is called when unknown attribute is qualified.

        Checks if the method is an attribute of the database object and, if so,
        returns the method.
        """
        if hasattr(self.DB, method):
            return getattr(self.DB, method)
        else:
            pass

    def getLimits(self, value=None):
        Limits = self.DB.getBudgetLimits('ALL')
        if Limits:
            self.Limit, self.remainingLimit = Limits
        elif value is None:
            raise NoneNotAllowed('''You must pass in a value for "limit" on
                                    the first load of a monthly budget!''')
        else:
            self.DB.insertBudgetData(value, exp_type='ALL')
            self.Limit = float(value)
            self.remainingLimit = float(value)

    def updateLimits(self, limit):
        limit = float(limit)
        initial = limit
        diff = self.Limit - self.remainingLimit
        remaining = limit - diff

        self.Limit = limit
        self.remainingLimit = remaining
        self.DB.UpdateBudgetLimit(remaining, initial=initial, exp_type='ALL')

    def add_expense(self, date, expense_type, value, notes):
        self.remainingLimit -= float(value)
        self.DB.UpdateBudgetLimit(self.remainingLimit, 'ALL')
        self.expenses.add_expense(date, expense_type, value, notes)

    def remove_expense(self, index):
        value = self.expenses[index].value
        self.remainingLimit += float(value)
        self.DB.UpdateBudgetLimit(self.remainingLimit, 'ALL')
        self.expenses.remove_expense(index)


class Expense_List:
    """ A comprehensive list of all of your expenses in a given Budget.

    This class is meant to be integrated into the Budget class and serves
    as a way to seperate the 'expense' operations that take place each
    Budget from other Budget related operations.
    """
    def __init__(self, DB):
        self.allExpenses = []
        self.DB = DB
        self.LoadExpenses()

    def LoadExpenses(self):
        for Expense in self.DB.getAllExpenses():
            key, date, etype, value, notes = Expense
            self.add_expense(date, etype, value, notes, key=key)

    def add_expense(self, date, expense_type, value, notes, key=None):
        if not key:
            key = self.DB.insertExpense(date, expense_type, value, notes)

        expense = expenses.Expense(key, date, expense_type, value, notes)
        self.allExpenses.append(expense)

    def remove_expense(self, index):
        try:
            key = self.allExpenses[index].key
            self.allExpenses.pop(index)
            self.DB.deleteExpense(key)
        except ValueError:
            print(index)

    def get(self):
        Exp_Attrs = []
        for Exp in self.allExpenses:
            Exp_Attrs.append(Exp.get())
        return Exp_Attrs

    def __getitem__(self, index):
        return self.allExpenses[index]


if __name__ == '__main__':
    B = Budget()
    B.getExpenseTypes
