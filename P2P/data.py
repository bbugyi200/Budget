import sqlite3
import os
import dates

debug = True

DB = 'data/' + dates.getDB()
if debug: 
    DB = '/home/bryan/My_Projects/P2P/data/example.db'
    DB = r'H:\\PP\\data\\example.db'

class InitSQLDB:
    """ InitSQLDB, when instantiated, initializes the SQLite database. """
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.c = self.conn.cursor()

        self.createETypeTable()
        self.createBaseETypes()
        self.createExpensesTable()

    def createETypeTable(self):
        self.c.execute('''CREATE TABLE Exp_Types
                     (ID INTEGER PRIMARY KEY,
                      type TEXT,
                      parent INTEGER);''')
        self.conn.commit()

    def createBaseETypes(self):
        baseTypes = ['Food', 'Monthly Bills', 'Miscellaneous', 'Entertainment']
        for etype in baseTypes:
            self.c.execute('''INSERT INTO Exp_Types VALUES (?, ?, ?)''',
                      (None, etype, None))

        self.conn.commit()

    def createExpensesTable(self):
        self.c.execute('''CREATE TABLE Expenses
                     (ID INTEGER PRIMARY KEY,
                      Date TEXT,
                      Exp_ID INTEGER,
                      Price REAL,
                      Notes TEXT,
                      FOREIGN KEY(Exp_ID) REFERENCES Exp_Types(ID));''')

        self.conn.commit()


class SQLDB:
    """ SQLDB objects are used to manipulate the SQLite database. """
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.c = conn.cursor()

    def insertExpense(self, date, exp_type, price, notes):
        self.c.execute("""SELECT ID FROM Exp_Types
                     WHERE type = ?;""", (exp_type,))
        exp_id = c.fetchone()[0]
        if debug: print('insertExpense ~ ExpID: ', exp_id)
        expense_data = (None, date, exp_id, price, notes)
        self.c.execute('''INSERT INTO Expenses VALUES (?, ?, ?, ?, ?)''', expense_data)

        self.conn.commit()

    def deleteExpense(self, index):
        self.c.execute('''DELETE FROM Expenses WHERE ID=?''', (index,))

        self.conn.commit()

    def getAllExpenses(self):
        expense_list = []
        for row in self.c.execute('''SELECT Expenses.ID, Expenses.Date, Exp_Types.type,
                                Expenses.Price, Expenses.Notes
                                FROM Expenses
                                INNER JOIN Exp_Types
                                ON Expenses.Exp_ID=Exp_Types.ID'''):

            expense_list.append(row)

        if debug: print('getAllExpenses: ', expense_list)

        return expense_list


if not os.path.isfile(DB):
    InitSQLDB()


if __name__ == '__main__':
    pass
