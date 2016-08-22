import sqlite3
from .InitSQLDB import DB

debug = True


class Base:
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.c = self.conn.cursor()

    def getExpID(self, exp_type):
        self.c.execute("""SELECT ID FROM ExpTypes
                     WHERE type=?;""", (exp_type,))
        exp_id = self.c.fetchone()[0]
        return exp_id


class Expenses(Base):
    """ Holds all expense related database operations. """
    def insertExpense(self, date, exp_type, price, notes):
        exp_id = self.getExpID(exp_type)
        if debug: print('insertExpense ~ ExpID: ', exp_id)
        expense_data = (None, date, exp_id, price, notes)
        self.c.execute('''INSERT INTO Expenses VALUES (?, ?, ?, ?, ?)''',
                       expense_data)

        key = self.c.lastrowid
        if debug: print("insertExpense ~ key: ", key)

        self.conn.commit()

        return key

    def deleteExpense(self, key):
        self.c.execute('''DELETE FROM Expenses WHERE ID=?''', (key,))

        self.conn.commit()

    def getAllExpenses(self):
        expense_list = []
        for row in self.c.execute('''SELECT Expenses.ID, Expenses.Date, ExpTypes.type,
                                Expenses.Price, Expenses.Notes
                                FROM Expenses
                                INNER JOIN ExpTypes
                                ON Expenses.Exp_ID=ExpTypes.ID'''):

            expense_list.append(row)

        if debug: print('getAllExpenses: ', expense_list)

        return expense_list


class Budgets(Base):
    """ Holds all database operations that are related to the BudgetData. """
    def insertBudgetData(self, value, exp_type):
        exp_id = self.getExpID(exp_type)

        budget_data = (None, exp_id, value, value)
        self.c.execute('''INSERT INTO BudgetData VALUES (?, ?, ?, ?)''',
                       budget_data)

        self.conn.commit()

    def UpdateBudgetRemLimit(self, price, exp_type):
        exp_id = self.getExpID(exp_type)
        values = (price, exp_id)
        self.c.execute('''UPDATE BudgetData
                          SET Remaining=?
                          WHERE Exp_ID=?;''', values)

    def getBudgetLimits(self, exp_type):
        exp_id = self.getExpID(exp_type)
        self.c.execute("""SELECT Initial, Remaining
                          FROM BudgetData
                          WHERE Exp_ID=?;""", (exp_id,))
        return self.c.fetchall()


class SQLDB(Expenses, Budgets): pass


if __name__ == '__main__':
    TestDB = SQLDB()
    Limits = TestDB.getBudgetLimits()
    print(Limits)
