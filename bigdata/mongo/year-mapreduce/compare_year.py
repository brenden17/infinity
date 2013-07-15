from datetime import datetime, timedelta
from random import randint
try:
    import mongoengine as me
except:
    print '== error importing mongoengine ='
    import sys
#    sys.exit()


'''
class DailyBalance(me.Document):
    dayat = me.DateTimeField(default=datetime.now)
    income = me.FloatField()
    expense = me.FloatField()

def setup_db():
    DBNAME = 'yearlybalancedb'
    me.connect(DBNAME)
'''

def create_doc(date, income, expense):
    print cdate, income, expense
    #return DailyBalance(date, income, expense)

def generate_data():
    sdate = datetime(2011, 01, 01)
    edate = datetime(2011, 02, 03)
    day = timedelta(days=1)
    cdate = sdate
    valuerange = (10000, 100000)
    fr = randint(*valuerange)
    while cdate < edate:
        create_doc(cdate, frandint(*valuerange), randint(*valuerange))
        d = randint(*valuerange)
        c = randint(*valuerange)
        print cdate, c, d
        cdate += day

if __name__ == '__main__':
    #setup_db()
    generate_data()

