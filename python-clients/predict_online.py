from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
import time
import datetime
credentials = GoogleCredentials.get_application_default()
import firebase_admin
from firebase_admin import credentials as fbCred
from firebase_admin import firestore
from random import randint

cred = fbCred.Certificate("../credentials/rh.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

day_of_year = int(datetime.datetime.now().timetuple().tm_yday)

category = u'Inventory'

def predictOnline(project_id, modelName):
    service = discovery.build('ml', 'v1', credentials=credentials)
    name = 'projects/{}/models/{}'.format(project_id, modelName)

    inst = []

    for i in range(0, 31):
        data = {}
        data['number'] = i+day_of_year
        inst.append(dict(data))

    response = service.projects().predict(
        name=name,
        body={'instances': inst}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])
    else:
        writeResponseToDb(response)


def writeResponseToDb(response):
    predictions = response['predictions']
    predictedData = dict()
    dayNumber = day_of_year
    for pred in predictions:
        predictedData[dayNumber] = pred['predictions'][0]
        dayNumber = dayNumber + 1
    data = {u'data':unicode(predictedData)}
    db.collection(u'predictions').document(category).set(data)


predictOnline('reaching-hands-9fac2', 'model_almond_test')
