""" dates.py

This module holds all functions that relate to dates and their formatting.
"""

import datetime
import os

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
          'Sep', 'Oct', 'Nov', 'Dec']


def getMonthlyDB(File=None):
    if File:
        if File[-3:] != '.db':
            F = File + '.db'
        else:
            F = File

        F = 'data/' + F

        return F

    else:
        d = datetime.date.today()

        month = MONTHS[d.month - 1]
        year = d.strftime('%y')

        return ''.join(['data/', month, '-', year, '.db'])


def getDBFiles():
    files = [f for f in os.listdir('data/') if f[-3:] == '.db']

    if 'example.db' in files:
        files.remove('example.db')

    files = [f[:-3] for f in files]

    def MFileSorter(F):
        year = int(F[-2:])

        month = F[:3]
        month = MONTHS.index(month)

        return (year * 100) + month

    files.sort(key=MFileSorter)

    return files


if __name__ == '__main__':
    F = getDBFiles()
