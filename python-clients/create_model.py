from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

credentials = GoogleCredentials.get_application_default()

ml = discovery.build('ml','v1', credentials=credentials)
projectID = 'projects/{}'.format('reaching-hands-9fac2')

requestDict = {'name': 'my_own_model',
               'description': 'your_model_description'}

request = ml.projects().models().create(
              parent=projectID, body=requestDict)

try:
    response = request.execute()
    print(response)
except errors.HttpError, err:
    # Something went wrong, print out some information.
    print('There was an error creating the model. Check the details:')
    print(err._get_reason())