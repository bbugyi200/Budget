import pickle
import payperiod
import bdates


def GetPayPeriod(date=None):
    try:
        if not date:
            filename = bdates.getLatestPP() + '.db'
        else:
            filename = date + '.db'
        with open('data/' + filename, 'rb') as F:
            PP = pickle.load(F)
    except Exception as e:
        print(str(e))
        PP = payperiod.PayPeriod(1036.03, bdates.getLatestPP())
        SavePP(PP)

    return PP


def SavePP(Obj):
    filename = Obj.StartDate + '.db'
    with open('data/' + filename, 'wb') as F:
        pickle.dump(Obj, F)
