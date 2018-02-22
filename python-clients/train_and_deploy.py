from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import datetime
from googleapiclient import errors,logging
import time

credentials = GoogleCredentials.get_application_default()
ml = discovery.build('ml','v1', credentials=credentials)

project_name = 'reaching-hands-9fac2'
project_id = 'projects/{}'.format(project_name)


train_files = 'gs://reaching-hands-9fac2-mlengine/training_data/almond/train_data.csv'
eval_files = 'gs://reaching-hands-9fac2-mlengine/training_data/almond/test_data.csv'


def create_training_job():

    timestamp = str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    my_job_name = 'my_model_'+str(timestamp)
    
    print('starting training for '+str(my_job_name))

    training_inputs = {'scaleTier': 'BASIC',
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
        print('training submitted succesfully for '+str(response))
        return my_job_name

    except errors.HttpError, err:
        logging.error('There was an error creating the training job.'
                    ' Check the details:')
        logging.error(err._get_reason())
        return None

def check_status(jobName):
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

if __name__ == '__main__':
    job_name = create_training_job()
    response = check_status(job_name)
    print('completed '+str(response))