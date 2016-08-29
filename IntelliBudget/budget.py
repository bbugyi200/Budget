""" budget.py

This module focuses on objects that represent more holistic models
of a single pay cycle.
"""

from . import expenses
from .data.SQLDB import SQLDB


class NoneNotAllowed(Exception): pass


class Budget:
    """ Budget object is used to handle budget operations. """
    def __init__(self, value=None, DB=None):
        if not DB:
            self.DB = SQLDB()
        else:
            self.DB = SQLDB(DB)

        self.Limits = dict()
        self.getLimits(value)
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
        for etype in self.DB.getExpenseTypes():
            Limits = self.DB.getBudgetLimits(etype)
            if Limits:
                self.Limits[etype] = Limits
            elif value is None:
                raise NoneNotAllowed('''You must pass in a value for "value" on
                                        the first load of a monthly budget!''')
            else:
                value = float(value)
                self.DB.insertBudgetData(value, exp_type=etype)
                self.Limits[etype] = (value, value)

    def updateLimits(self, value, etype):
        orig_initial, orig_remaining = self.Limits[etype]

        value = float(value)
        new_initial = value
        diff = orig_initial - orig_remaining
        new_remaining = value - diff

        self.Limits[etype] = (new_initial, new_remaining)
        self.DB.UpdateBudgetLimit(new_remaining, initial=new_initial, exp_type=etype)

    def add_expense(self, date, etype, value, notes):
        orig_initial, orig_remaining = self.Limits[etype]
        new_remaining = orig_remaining - float(value)
        self.Limits[etype] = (orig_initial, new_remaining)

        self.DB.UpdateBudgetLimit(new_remaining, etype)
        self.expenses.add_expense(date, etype, value, notes)

    def remove_expense(self, index):
        value = self.expenses[index].value
        etype = self.expenses[index].expense_type

        orig_initial, orig_remaining = self.Limits[etype]
        new_remaining = orig_remaining + float(value)
        self.DB.UpdateBudgetLimit(new_remaining, etype)
        self.expenses.remove_expense(index)
        self.Limits[etype] = (orig_initial, new_remaining)


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
