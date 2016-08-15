""" expenses.py

This module contains all of the expense related object definitions in the
Budget Program
"""


class Money:
    """ Used specifically to enable the string conversion of the expense value
    to pretty-print
    """
    def __init__(self, val):
        self.val = float(val)

    def __str__(self):
        return '${0:.2f}'.format(self.val)

    def __float__(self):
        return self.val

    def __add__(self, x):
        return self.val + x


class Expense:
    """ Meta-Class Expense Object. """
    def __init__(self, expense_type, value, notes):
        self.expense_type = expense_type
        # It is important to convert to float here.
        # This will produce a ValueError exception if 'value' is not nummeric
        self.value = Money(float(value))
        self.notes = notes

    def get(self):
        return (self.expense_type, self.value, self.notes)


class Food(Expense):
    def __init__(self, value, notes):
        Expense.__init__(self, "Food", value, notes)


class Entertainment(Expense):
    def __init__(self, value, notes):
        Expense.__init__(self, "Entertainment", value, notes)


class Monthly_Bills(Expense):
    def __init__(self, value, notes):
        Expense.__init__(self, "Monthly Bills", value, notes)


class Fuel(Expense):
    def __init__(self, value, notes):
        Expense.__init__(self, "Fuel", value, notes)


class Other(Expense):
    def __init__(self, value, notes):
        Expense.__init__(self, "Other", value, notes)


if __name__ == '__main__':
    x = Money(10)
