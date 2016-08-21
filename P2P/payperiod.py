""" payperiod.py

This module focuses on objects that represent more holistic models
of a single pay cycle.
"""

debug = True

if not debug:
    from . import expenses
    from . import data
else:
    import expenses
    import data


class PP_Base:
    """ PayPeriod object is used to represent a single pay period, the initial
    amount of money received in your paycheck, all of your expenses, and also
    the remaining amount of funds you have left from this pay cycle.
    """
    def __init__(self, PayCheck, StartDate):
        self.initial = float(PayCheck)
        self.remaining = float(PayCheck)
        self.expenses = Expense_List()
        self.StartDate = StartDate

    def add_expense(self, expense_type, value, notes):
        self.remaining -= float(value)
        self.expenses.add_expense(expense_type, value, notes)

    def remove_expense(self, index, value):
        self.remaining += float(value)
        self.expenses.remove_expense(index)


class PP_Goals(PP_Base):
    """ Contains all Budget Goal content. """
    def __init__(self, Paycheck, StartDate, budgeted):
        self.initialBud = float(budgeted)
        self.remainingBud = float(budgeted)
        PP_Base.__init__(self, Paycheck, StartDate)

    def add_expense(self, expense_type, value, notes):
        PP_Base.add_expense(self, expense_type, value, notes)
        self.remainingBud -= float(value)

    def remove_expense(self, index):
        value = self.expenses[index].value
        PP_Base.remove_expense(self, index, value)
        self.remainingBud += float(value)


class PayPeriod(PP_Goals):
    """ Final PayPeriod Class. Inherits all pay-period functionality. This
    class is really just a dummy-class. This was done so the content-specific
    classes could all be named according to their content.
    """
    pass


class Expense_List:
    """ A comprehensive list of all of your expenses in a given PayPeriod.

    This class is meant to be integrated into the PayPeriod class and serves
    as a way to seperate the 'expense' operations that take place each
    PayPeriod from other PayPeriod related operations.
    """
    def __init__(self):
        self.allExpenses = []
        self.DB = data.SQLDB()
        self.LoadExpenses()

    def LoadExpenses(self):
        for Expense in self.DB.getAllExpenses():
            key, date, etype, value, notes = Expense
            self.add_expense(key, date, etype, value, notes)

    def add_expense(self, key, date, expense_type, value, notes):
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
    E = Expense_List()
    print(E.get())
