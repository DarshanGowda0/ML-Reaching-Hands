import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage

# Use the application default credentials
# cred = credentials.Certificate("../credentials/rh.json")
firebase_admin.initialize_app()
db = firestore.client()
bucket_name = 'reaching-hands-e2737-mlengine'


categories = [u'Inventory', u'Services', u'Maintenance', u'Education']


def createCsv(fileName, dataDictionary):
    with open(str('../train_data/')+fileName+str('.csv'), 'wb') as f:
        for date in dataDictionary:
            f.write(str(date)+","+str(dataDictionary[date])+str('\n'))


def fetchAndProcessData():
    for category in categories:
        items_ref = db.collection(u'logs').where(u'category', u'==', category)
        docs = items_ref.get()

        itemDict = dict()

        for doc in docs:
            date, cost = str(doc.to_dict()['date'])[:10], doc.to_dict()['cost']
            if itemDict.has_key(date):
                itemDict[date] = itemDict[date] + cost
            else:
                itemDict[date] = cost

        createCsv(category, itemDict)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def uploadToGcs():
    for category in categories:
        filename = str('train_data/')+category+str('.csv')
        upload_blob(bucket_name,str('../')+filename,filename)


if __name__ == "__main__":
    fetchAndProcessData()
    upload_blob(bucket_name, '../train_data/Inventory.csv',
                'train_data/Inventory.csv')
