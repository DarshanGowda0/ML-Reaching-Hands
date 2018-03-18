import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from random import randint

cred = credentials.Certificate("../credentials/rh.json")
firebase_admin.initialize_app(cred)

import random
import time

def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%d %I:%M %p', prop)

def generateData():
    data = {
        u'addedBy':u'4uaHJ1zzB9ZWiySnr610oD3oFat2',
        u'category':u'Inventory',
        u'cost':randint(50,60),
        u'date':u''+str(randomDate("2017-1-1 1:30 PM", "2018-1-1 4:50 AM", random.random())),
        u'itemId':u'CPoMrmIlyHrKAb7xtejG',
        u'logId':u''+str(randint(1,1000)),
        u'logType':u'Added',
        u'quantity':randint(1,5),
        u'remarks':u'dsfvdsc',
        u'selectedColumns':u'Boys',
        u'subCategory':u'Assets'
    }
    return data

db = firestore.client()

for i in range(0,100):
    data = generateData()
    db.collection(u'logs').document(data['logId']).set(data)