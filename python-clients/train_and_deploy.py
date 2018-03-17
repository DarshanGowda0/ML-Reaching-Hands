from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import datetime
from googleapiclient import errors,logging
import time

credentials = GoogleCredentials.get_application_default()
ml = discovery.build('ml','v1', credentials=credentials)

project_name = 'reaching-hands-e2737'
project_id = 'projects/{}'.format(project_name)


train_files = 'gs://reaching-hands-e2737-mlengine/training_data/almond/train_data.csv'
eval_files = 'gs://reaching-hands-e2737-mlengine/training_data/almond/test_data.csv'

output_dir = 'gs://reaching-hands-e2737-mlengine/output/'

def create_training_job():

    timestamp = str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    my_job_name = 'my_model_'+str(timestamp)
    
    print('starting training for '+str(my_job_name))

    training_inputs = {'scaleTier': 'BASIC',
        'packageUris': ['gs://reaching-hands-e2737-mlengine/packages/package.tar.gz'],
        'pythonModule': 'trainer.task',
        'args': ['--train-files',train_files,'--eval-files',eval_files,'--train-steps','30000','--eval-steps','1000'],
        'region': 'us-central1',
        'jobDir': output_dir + str(my_job_name),
        'runtimeVersion': '1.4'}

    job_spec = {'jobId': my_job_name, 'trainingInput': training_inputs}
    request = ml.projects().jobs().create(body=job_spec,
                parent=project_id)

    try:
        response = request.execute()
        print('training submitted succesfully for '+str(response))
        return my_job_name

    except errors.HttpError, err:
        logging.error('There was an error creating the training job.'
                    ' Check the details:')
        logging.error(err._get_reason())
        return None

def check_train_status(jobName):
    jobId = '{}/jobs/{}'.format(project_id, jobName)
    request = ml.projects().jobs().get(name=jobId)
    print('checking status for '+str(jobId))
    done = False
    while not done:
        response = None
        time.sleep(5)
        try:
            response = request.execute()
            print('consumed ml unit '+str(response['trainingOutput']))
            print(response['state'])
            state = response['state']
            if(state == 'SUCCEEDED'):
                done = True
        except errors.HttpError, err:
            print err

    return response

def create_model(projectId, modelName):
    requestDict = {'name': modelName,
    'description': 'Another model for reaching hands '+str(modelName)}

    request = ml.projects().models().create(parent=projectId,
                            body=requestDict)

    try:
        response = request.execute()
        print response

    except errors.HttpError as err:
        print('There was an error creating the model.' +
            ' Check the details:')
        print(err._get_reason())
        response = None

def deploy_model(projectId, modelName):
    modelID = '{}/models/{}'.format(projectId, modelName)
    requestDict = {'name': 'v1',
    'description': 'just another deploy for reaching hands',
    'deploymentUri': output_dir + str(modelName)+'/export/census/*/saved_model.*'}

    request = ml.projects().models().versions().create(parent=modelID,
                body=requestDict)

    try:
        response = request.execute()
        operationID = response['name']

        done = False
        request = ml.projects().operations().get(name=operationID)

        while not done:
            response = None
            time.sleep(5)
            try:
                response = request.execute()
                print response
                done = response.get('done', False)
            except errors.HttpError as err:
                print('There was an error getting the operation.' +
                    'Check the details:')
                print(err._get_reason())
                done = True

    except errors.HttpError as err:
                print('There was an error getting the operation.' +
                    'Check the details:')
                print(err._get_reason())
                done = True

if __name__ == '__main__':
    job_name = create_training_job()
    if job_name != None:
        response = check_train_status(job_name)
        print('completed '+str(response))
        create_model(project_id,job_name)
        deploy_model(project_id,job_name)
    # deploy_model(project_id,'my_model_2018_/02_23_14_16_03')