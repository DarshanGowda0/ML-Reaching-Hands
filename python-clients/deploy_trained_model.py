from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
# Time is for waiting until the request finishes.
import time

projectID = 'projects/{}'.format('reaching-hands-9fac2')
modelName = 'model_almond_test'
modelID = '{}/models/{}'.format(projectID, modelName)
versionName = 'v3'
versionDescription = 'version_description'
trainedModelLocation = 'gs://reaching-hands-9fac2-mlengine/output/my_model_2018_02_21_00_42_59/export/census/1519154151/'

credentials = GoogleCredentials.get_application_default()
ml = discovery.build('ml', 'v1', credentials=credentials)

# Create a dictionary with the fields from the request body.
requestDict = {'name': modelName,
    'description': 'Another model for testing.'}

# Create a request to call projects.models.create.
request = ml.projects().models().create(parent=projectID,
                            body=requestDict)

# Make the call.
try:
    response = request.execute()

    # Any additional code on success goes here (logging, etc.)

except errors.HttpError as err:
    # Something went wrong, print out some information.
    print('There was an error creating the model.' +
        ' Check the details:')
    print(err._get_reason())

    # Clear the response for next time.
    response = None

requestDict = {'name': versionName,
    'description': versionDescription,
    'deploymentUri': trainedModelLocation}

# Create a request to call projects.models.versions.create
request = ml.projects().models().versions().create(parent=modelID,
              body=requestDict)

# Make the call.
try:
    response = request.execute()

    # Get the operation name.
    operationID = response['name']

    # Any additional code on success goes here (logging, etc.)

    done = False
    request = ml.projects().operations().get(name=operationID)

    while not done:
        response = None

        # Wait for 300 milliseconds.
        time.sleep(0.3)

    # Make the next call.
    try:
        response = request.execute()

        # Check for finish.
        done = response.get('done', False)

    except errors.HttpError as err:
        # Something went wrong, print out some information.
        print('There was an error getting the operation.' +
            'Check the details:')
        print(err._get_reason())
        done = True

except errors.HttpError as err:
    # Something went wrong, print out some information.
    print('There was an error creating the version.' +
          ' Check the details:')
    print(err._get_reason())

    # Handle the exception as makes sense for your application.












# projects/reaching-hands-9fac2/jobs/my_model_2018_02_23_14_16_03

# starting training for my_model_2018_02_23_14_16_03
# training submitted succesfully for {u'trainingOutput': {}, u'state': u'QUEUED', u'trainingInput': {u'runtimeVersion': u'1.4', u'region': u'us-central1', u'args': [u'--train-files', u'gs://reaching-hands-9fac2-mlengine/training_data/almond/train_data.csv', u'--eval-files', u'gs://reaching-hands-9fac2-mlengine/training_data/almond/test_data.csv', u'--train-steps', u'30000', u'--eval-steps', u'1000'], u'pythonModule': u'trainer.task', u'jobDir': u'gs://reaching-hands-9fac2-mlengine/output/my_model_2018_02_23_14_16_03', u'packageUris': [u'gs://reaching-hands-9fac2-mlengine/packages/package.tar.gz']}, u'createTime': u'2018-02-23T08:45:50Z', u'jobId': u'my_model_2018_02_23_14_16_03'}
# checking status for projects/reaching-hands-9fac2/jobs/my_model_2018_02_23_14_16_03