from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
# from oauth2client.service_account import ServiceAccountCredentials
# Time is for waiting until the request finishes.
import time



inst = [{'number': [24]},{'number':[2]}]
# inst = []

# for i in range(1,1000):
#     data = {}
#     data['number'] = i
#     inst.append(dict(data))
    
projectID = 'reaching-hands-9fac2'
modelName = 'model_almond_test'
# modelID = '{}/models/{}'.format(projectID, modelName)

# credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account.json')
service = discovery.build('ml', 'v1')
name = 'projects/{}/models/{}'.format(projectID, modelName)

response = service.projects().predict(
    name=name,
    body={'instances': inst}
).execute()

if 'error' in response:
    raise RuntimeError(response['error'])

print response['predictions']
