import datetime
from os import listdir
from os.path import isfile, join


def getPP_files():
    files = [f[:-3] for f in listdir('data/') if isfile(join('data/', f))]
    return sorted(files, key=_date_sorter)


def _date_sorter(date):
    return (100*int(date[0:2])) + int(date[3:5]) + (10000*int(date[6:8]))


def getLatestPP():
    files = getPP_files()
    
    months = [int(f[:2]) for f in files]
    days = [int(f[3:5]) for f in files]
    years = [int(f[6:8]) for f in files]

    date_tuples = zip(months, days, years)
    dates = [datetime.date(Y, M, D) for M, D, Y in date_tuples]
    dates = sorted(dates)

    # :02d ensures that a zero is filled for single digit months
    date_string = '{0:02d}-{1:02d}-{2}'.format(dates[-1].month, dates[-1].day, dates[-1].year)

    return date_string

if __name__ == '__main__':
    L = getPP_files()
    print(L)
    
