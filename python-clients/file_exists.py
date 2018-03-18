from google.cloud import storage
bucket_name = 'reaching-hands-9fac2-mlengine'
import datetime

url_path = 'gs://reaching-hands-9fac2-mlengine/output/my_model_2018_02_21_00_42_59/export/census'

def getGCSPath(prefix):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    mlist = bucket.list_blobs(prefix=prefix)
    for line in mlist:
        if 'saved_model.pb' in line.name:
            return line.name[:-14]

# print getGCSPath('output/my_model_2018_02_23_17_08_01/export/census/')
day_of_year = int(datetime.datetime.now().timetuple().tm_yday)
inst = []
for i in range(0, 31):
        data = {}
        data['number'] = i+day_of_year
        inst.append(dict(data))
# print day_of_year

print inst