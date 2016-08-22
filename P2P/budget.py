""" budget.py

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

DB = data.SQLDB()


class NoneNotAllowed(Exception): pass


class Budget:
    """ Budget object is used to handle budget operations. """
    def __init__(self, limit=None):
        self.getLimit()
        self.expenses = Expense_List()

    def getLimit(self):
        Limits = DB.getBudgetLimits()
        if debug: print('Budget ~ Limits: ', Limits, end='\n\n')
        if Limits:
            self.Limit, self.remainingLimit = Limits[0]
        elif not limit:
            raise NoneNotAllowed('''You must pass in a value for "limit" on
                                    the first load of a monthly budget!''')
        else:
            DB.insertBudgetData(limit, exp_type='ALL')
            self.Limit = float(limit)
            self.remainingLimit = float(limit)


    def add_expense(self, date, expense_type, value, notes):
        self.remainingLimit -= float(value)
        self.expenses.add_expense(date, expense_type, value, notes)

    def remove_expense(self, index):
        value = self.expenses[index].value
        self.remainingLimit += float(value)
        self.expenses.remove_expense(index)


class Expense_List:
    """ A comprehensive list of all of your expenses in a given Budget.

    This class is meant to be integrated into the Budget class and serves
    as a way to seperate the 'expense' operations that take place each
    Budget from other Budget related operations.
    """
    def __init__(self):
        self.allExpenses = []
        self.LoadExpenses()

    def LoadExpenses(self):
        for Expense in DB.getAllExpenses():
            key, date, etype, value, notes = Expense
            self.add_expense(date, etype, value, notes, key=key, new=False)

    def add_expense(self, date, expense_type, value, notes, key=None, new=True):
        if new:
            key = DB.insertExpense(date, expense_type, value, notes)
        elif not key:
            raise NoneNotAllowed("""You must pass in a key to use 'add_expense'
                                    with new expenses!""")

        expense = expenses.Expense(key, date, expense_type, value, notes)
        self.allExpenses.append(expense)

    def remove_expense(self, index):
        try:
            key = self.allExpenses[index].key
            self.allExpenses.pop(index)
            DB.deleteExpense(key)
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

    def InsertData():
        B.add_expense('8-21-16', 'Food', 22.15, 'Wawa')
        B.add_expense('8-21-16', 'Monthly Bills', 141.17, 'Verizon')
        B.add_expense('8-21-16', 'Entertainment', 24.50, 'Movies')
