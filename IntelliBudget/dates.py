""" dates.py

This module holds all functions that relate to dates and their formatting.
"""

import datetime
import os

today = datetime.date.today()

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

SHORT_MONTHS = [M[:3] for M in MONTHS]


def getMonth(month=None):
    if month:
        index = SHORT_MONTHS.index(month[:3])
        return MONTHS[index]
    else:
        index = today.month - 1
        return MONTHS[index]


def getMonthlyDB(File=None):
    if File:
        if File[-3:] != '.db':
            F = File + '.db'
        else:
            F = File

        F = 'data/' + F

        return F

    else:
        index = today.month - 1
        month = MONTHS[index][:3]
        year = today.strftime('%y')

        return ''.join(['data/', month, '-', year, '.db'])


def getDBFiles():
    files = [f for f in os.listdir('data/') if f[-3:] == '.db']

    if 'example.db' in files:
        files.remove('example.db')

    files = [f[:-3] for f in files]

    def MFileSorter(F):
        year = int(F[-2:])

        month = F[:3]
        month = SHORT_MONTHS.index(month)

        return (year * 100) + month

    files.sort(key=MFileSorter)

    return files


if __name__ == '__main__':
    F = getDBFiles()
