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

    def __repr__(self):
        if self.val >= 0:
            return '${0:.2f}'.format(self.val)
        else:
            return '-${0:.2f}'.format(abs(self.val))

    def __float__(self):
        return self.val

    def __add__(self, x):
        return self.val + x


class Expense:
    """ Meta-Class Expense Object. """
    def __init__(self, key, date, expense_type, value, notes):
        self.key = key
        self.date = date
        self.expense_type = expense_type
        # It is important to convert to float here.
        # This will produce a ValueError exception if 'value' is not nummeric
        self.value = Money(float(value))
        self.notes = notes

    def get(self):
        return (self.date, self.expense_type, self.value, self.notes)


if __name__ == '__main__':
    x = Money(10)
