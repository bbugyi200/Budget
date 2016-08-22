import sqlite3
import os
from .. import dates

debug = True

DB = 'data/' + dates.getDB()
if debug:
    DB = '/home/bryan/My_Projects/IntelliBudget/data/example.db'


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
        baseTypes = ['ALL',
                     'Food',
                     'Monthly Bills',
                     'Miscellaneous',
                     'Entertainment']

        for etype in baseTypes:
            values = (None, etype, None)
            self.c.execute('''INSERT INTO ExpTypes VALUES (?, ?, ?)''', values)

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


if not os.path.isfile(DB):
    InitDB = InitSQLDB()
    InitDB.CreateAll()
