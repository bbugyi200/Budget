""" bdata.py

All functions that relate directly to the user data should be stored in
this module.
"""

import pickle
import payperiod
import bdates

""" This exception is raised when no files are found in the 'data/' folder """
class NoData(Exception): pass

def GetPayPeriod(date=None):
    """ Used to return a payperiod object loaded with the pickle module

    GetPayPeriod(date=None) -> PayPeriod Object

    date = the start date of the payperiod that you would like to retrieve
    """
    try:
        if not date:
            filename = bdates.getLatestPP() + '.db'
        else:
            filename = date + '.db'
        with open('data/' + filename, 'rb') as F:
            PP = pickle.load(F)

    # IndexError will be raised if the 'dates' list in 'bdates.py' is empty.
    # Caused by 'dates[-1].month'.
    except IndexError as e:
        raise NoData


    return PP


def SavePP(Obj):
    """ Saves Obj to a file by using the pickle module to 'dump' it.

    SavePP(Obj) -> None

    Obj = The PayPeriod object that will be saved to a file.
    """
    filename = Obj.StartDate + '.db'
    with open('data/' + filename, 'wb') as F:
        pickle.dump(Obj, F)
