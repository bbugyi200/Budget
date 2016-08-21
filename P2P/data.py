import sqlite3
import os
import P2P.dates as dates

DB = 'data/' + dates.getDB()
DB = 'data/example.db'


TypeDictionary = dict()


def createETypeTable():
    conn = sqlite3.connect(DB)

    c = conn.cursor()

    c.execute('''CREATE TABLE Exp_Types
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  type TEXT,
                  parent INTEGER);''')
    conn.commit()
    conn.close()


def createBaseETypes():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    baseTypes = ['Food', 'Monthly Bills', 'Miscellaneous', 'Entertainment']
    for i, etype in enumerate(baseTypes, 1):
        TypeDictionary[etype] = i
        c.execute('''INSERT INTO Exp_Types VALUES (?, ?, ?)''', (i, etype, 0))

    conn.commit()
    conn.close()


def createExpensesTable():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''CREATE TABLE Expenses
                 (Date TEXT,
                  Exp_ID INTEGER,
                  Price REAL,
                  Notes TEXT,
                  FOREIGN KEY(Exp_ID) REFERENCES Exp_Types(ID));''')

    conn.commit()
    conn.close()


def insertExpense(date, exp_type, price, notes):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    exp_id = TypeDictionary[exp_type]
    expense_data = (date, exp_id, price, notes)
    c.execute('''INSERT INTO Expenses VALUES (?, ?, ?, ?)''', expense_data)

    conn.commit()
    conn.close()


def getAllExpenses():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    for row in c.execute('''SELECT * FROM Expenses'''):
        print(row)

    conn.close()


if not os.path.isfile(DB):
    createETypeTable()
    createExpensesTable()
    createBaseETypes()


if __name__ == '__main__':
    insertExpense(date='8-20-16',
                  exp_type='Food',
                  price=22.50,
                  notes='Wawa')

    getAllExpenses()
