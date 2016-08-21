import sqlite3
import os
import dates

debug = True

DB = 'data/' + dates.getDB()
if debug: DB = '/home/bryan/My_Projects/P2P/data/example.db'


def createETypeTable():
    conn = sqlite3.connect(DB)

    c = conn.cursor()

    c.execute('''CREATE TABLE Exp_Types
                 (ID INTEGER PRIMARY KEY,
                  type TEXT,
                  parent INTEGER);''')
    conn.commit()
    conn.close()


def createBaseETypes():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    baseTypes = ['Food', 'Monthly Bills', 'Miscellaneous', 'Entertainment']
    for etype in baseTypes:
        c.execute('''INSERT INTO Exp_Types VALUES (?, ?, ?)''',
                  (None, etype, None))

    conn.commit()
    conn.close()


def createExpensesTable():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''CREATE TABLE Expenses
                 (ID INTEGER PRIMARY KEY,
                  Date TEXT,
                  Exp_ID INTEGER,
                  Price REAL,
                  Notes TEXT,
                  FOREIGN KEY(Exp_ID) REFERENCES Exp_Types(ID));''')

    conn.commit()
    conn.close()


def insertExpense(date, exp_type, price, notes):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""SELECT ID FROM Exp_Types
                 WHERE type = ?;""", (exp_type,))
    exp_id = c.fetchone()[0]
    if debug: print('insertExpense ~ ExpID: ', exp_id)
    expense_data = (None, date, exp_id, price, notes)
    c.execute('''INSERT INTO Expenses VALUES (?, ?, ?, ?, ?)''', expense_data)

    conn.commit()
    conn.close()


def deleteExpense(index):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''DELETE FROM Expenses WHERE ID=?''', (index,))

    conn.commit()
    conn.close()


def getAllExpenses():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    expense_list = []
    for row in c.execute('''SELECT Expenses.ID, Expenses.Date, Exp_Types.type,
                            Expenses.Price, Expenses.Notes
                            FROM Expenses
                            INNER JOIN Exp_Types
                            ON Expenses.Exp_ID=Exp_Types.ID'''):

        expense_list.append(row)

    conn.close()

    if debug: print('getAllExpenses: ', expense_list)

    return expense_list


if not os.path.isfile(DB):
    createETypeTable()
    createExpensesTable()
    createBaseETypes()


if __name__ == '__main__':
    insertExpense(date='8-20-16',
                  exp_type='Food',
                  price=22.50,
                  notes='Wawa')

    insertExpense(date='8-20-16',
                  exp_type='Monthly Bills',
                  price=140.16,
                  notes='Verizon')

    getAllExpenses()
