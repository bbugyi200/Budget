""" bdates.py

This module holds all functions that relate to dates and their formatting.
"""

import datetime
from os import listdir
from os.path import isfile, join


def getPP_files():
    """ Returns a sorted list of all PayPeriod files in the 'data/' folder

    getPP_files() -> Sorted list of PayPeriod files without their .db extension
    """
    files = [f[:-3] for f in listdir('data/') if isfile(join('data/', f))]
    return sorted(files, key=_date_sorter)


def _date_sorter(date):
    """ Used as a key for the 'sorted' function. Sorts files by date. """
    return (100*int(date[0:2])) + int(date[3:5]) + (10000*int(date[6:8]))


def getLatestPP():
    """ Returns a date string that matches the latest PayPeriod on file. """
    files = getPP_files()

    months = [int(f[:2]) for f in files]
    days = [int(f[3:5]) for f in files]
    years = [int(f[6:8]) for f in files]

    date_tuples = zip(months, days, years)
    dates = [datetime.date(Y, M, D) for M, D, Y in date_tuples]
    dates = sorted(dates)

    # Saves and reformats the latest date in 'dates' to the 'date_string' var.
    # :02d ensures that a zero is filled for single digit months
    date_string = '{0:02d}-{1:02d}-{2}'.format(dates[-1].month, dates[-1].day, dates[-1].year)

    return date_string

if __name__ == '__main__':
    L = getPP_files()
    print(L)
