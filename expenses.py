""" expenses.py

This module contains all of the expense related object definitions in the
Budget Program
"""


class Expense:
    """ Meta-Class Expense Object. """
    def __init__(self, expense_type, value, notes):
        self.expense_type = expense_type
        self.value = value
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
