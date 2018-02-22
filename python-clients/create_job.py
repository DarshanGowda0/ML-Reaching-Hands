from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import datetime
from googleapiclient import errors,logging


credentials = GoogleCredentials.get_application_default()

ml = discovery.build('ml','v1', credentials=credentials)

project_name = 'reaching-hands-9fac2'
project_id = 'projects/{}'.format(project_name)

timestamp = str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
my_job_name = 'my_model_'+str(timestamp)
train_files = 'gs://reaching-hands-9fac2-mlengine/training_data/almond/train_data.csv'
eval_files = 'gs://reaching-hands-9fac2-mlengine/training_data/almond/test_data.csv'


training_inputs = {'scaleTier': 'BASIC',
    # 'masterType': 'standard',
    # 'workerType': 'complex_model_m',
    # 'parameterServerType': 'large_model',
    # 'workerCount': 9,
    # 'parameterServerCount': 3,
    'packageUris': ['gs://reaching-hands-9fac2-mlengine/packages/package.tar.gz'],
    'pythonModule': 'trainer.task',
    'args': ['--train-files',train_files,'--eval-files',eval_files,'--train-steps','30000','--eval-steps','1000'],
    'region': 'us-central1',
    'jobDir': 'gs://reaching-hands-9fac2-mlengine/output/'+str(my_job_name),
    'runtimeVersion': '1.4'}

job_spec = {'jobId': my_job_name, 'trainingInput': training_inputs}

request = ml.projects().jobs().create(body=job_spec,
              parent=project_id)

try:
    response = request.execute()
    # You can put your code for handling success (if any) here.

except errors.HttpError, err:
    # Do whatever error response is appropriate for your application.
    # For this example, just send some text to the logs.
    # You need to import logging for this to work.
    logging.error('There was an error creating the training job.'
                  ' Check the details:')
    logging.error(err._get_reason())

