import sqlite3
import os
import dates
import collections

debug = True

DB = 'data/' + dates.getDB()
if debug: 
    DB = '/home/bryan/My_Projects/P2P/data/example.db'
    DB = r'H:\\PP\\data\\example.db'

class InitSQLDB:
    """ InitSQLDB initializes the SQLite database. """
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.c = self.conn.cursor()

    def CreateAll(self):
        self.createETypeTable()
        self.createBaseETypes()
        self.createExpensesTable()
        self.createBudgetTable()

    def createETypeTable(self):
        self.c.execute('''CREATE TABLE ExpTypes
                     (ID INTEGER PRIMARY KEY,
                      type TEXT,
                      parent INTEGER);''')
        self.conn.commit()

    def createBaseETypes(self):
        baseTypes = ['ALL', 'Food', 'Monthly Bills', 'Miscellaneous', 'Entertainment']
        for etype in baseTypes:
            self.c.execute('''INSERT INTO ExpTypes VALUES (?, ?, ?)''',
                      (None, etype, None))

        self.conn.commit()

    def createExpensesTable(self):
        self.c.execute('''CREATE TABLE Expenses
                     (ID INTEGER PRIMARY KEY,
                      Date TEXT,
                      Exp_ID INTEGER,
                      Price REAL,
                      Notes TEXT,
                      FOREIGN KEY(Exp_ID) REFERENCES ExpTypes(ID));''')

        self.conn.commit()

    def createBudgetTable(self):
        self.c.execute('''CREATE TABLE BudgetData
                         (ID INTEGER PRIMARY KEY,
                          Exp_ID INTEGER UNIQUE,
                          Initial REAL,
                          Remaining REAL,
                          FOREIGN KEY(Exp_ID) REFERENCES ExpTypes(ID));''')


class SQLDB:
    """ SQLDB objects are used to manipulate the SQLite database. """
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.c = self.conn.cursor()

    def getExpID(self, exp_type):
        self.c.execute("""SELECT ID FROM ExpTypes
                     WHERE type = ?;""", (exp_type,))
        exp_id = self.c.fetchone()[0]
        return exp_id

    def insertExpense(self, date, exp_type, price, notes):
        exp_id = self.getExpID(exp_type)
        if debug: print('insertExpense ~ ExpID: ', exp_id)
        expense_data = (None, date, exp_id, price, notes)
        self.c.execute('''INSERT INTO Expenses VALUES (?, ?, ?, ?, ?)''', expense_data)

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

    def insertBudgetData(self, value, exp_type):
        exp_id = self.getExpID(exp_type)

        budget_data = (None, exp_id, value, value)
        self.c.execute('''INSERT INTO BudgetData VALUES (?, ?, ?, ?)''',
                       budget_data)

        self.conn.commit()

    def getBudgetLimits(self):
        # 0 is the key for 'ALL'
        self.c.execute("""SELECT Initial, Remaining
                          FROM BudgetData
                          WHERE Exp_ID=1;""") 
        return self.c.fetchall()


if not os.path.isfile(DB):
    InitDB = InitSQLDB()
    InitDB.CreateAll()


if __name__ == '__main__':
    DB = SQLDB()
    # for row in DB.c.execute('''SELECT * FROM BudgetData'''):
    #     print(row)
    Limits = DB.getBudgetLimits()
    print(Limits)
