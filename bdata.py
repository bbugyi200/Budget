""" bdata.py

All functions that relate directly to the user data should be stored in
this module. """

import pickle
import payperiod
import bdates


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

    # If an exception is raised, create a default PayPeriod
    # object and save it to a file.
    except Exception as e:
        print(str(e))
        PP = payperiod.PayPeriod(1036.03, bdates.getLatestPP())
        SavePP(PP)

    return PP


def SavePP(Obj):
    """ Saves Obj to a file by using the pickle module to 'dump' it.

    SavePP(Obj) -> None

    Obj = The PayPeriod object that will be saved to a file.
    """
    filename = Obj.StartDate + '.db'
    with open('data/' + filename, 'wb') as F:
        pickle.dump(Obj, F)
