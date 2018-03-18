import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from random import randint

cred = credentials.Certificate("../credentials/rh.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

for i in range(0,1000):
    db.collection(u'logs').document(str(i)).delete()