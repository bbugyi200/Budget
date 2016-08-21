""" dates.py

This module holds all functions that relate to dates and their formatting.
"""

import datetime


def getDB():
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec']

    d = datetime.date.today()

    month = MONTHS[d.month - 1]
    year = d.strftime('%y')

    return ''.join([month, '-', year, '.db'])


if __name__ == '__main__':
    M = getDB()
    print(M)
