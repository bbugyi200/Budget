""" payperiod.py

This module focuses on objects that represent more holistic models
of a single pay cycle
"""

import expenses


class PayPeriod:
    def __init__(self, PayCheck, StartDate):
        self.initial = float(PayCheck)
        self.remaining = float(PayCheck)
        self.expenses = Expense_List()
        self.StartDate = StartDate

    def add_expense(self, expense_type, value, notes):
        self.expenses.add_expense(expense_type, value, notes)
        self.subtract(value)

    def remove_expense(self, index):
        self.add(self.expenses[index].value)
        self.expenses.remove_expense(index)

    def add(self, value):
        self.remaining += float(value)

    def subtract(self, value):
        self.remaining -= float(value)


class Expense_List:
    def __init__(self):
        self.allExpenses = []

    def add_expense(self, expense_type, value, notes):
        expense_type = expense_type.replace(' ', '_')
        exp_obj = getattr(expenses, expense_type)
        expense = exp_obj(value, notes)
        self.allExpenses.append(expense)

    def remove_expense(self, index):
        try:
            self.allExpenses.pop(index)
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
    P = PayPeriod(1200)
    P.add_expense('Food', 150)
