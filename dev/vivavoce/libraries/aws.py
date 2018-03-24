import boto3
import time

from vivavoce.models import TranscribeJob


AWS_ACCESS_KEY = 'AKIAIO2NRGA6M25NZLYQ'
AWS_SECRET_ACCESS_KEY = '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'

def check_results():
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print('in progress....')
        time.sleep(5)

def transcribe(answer_uri, job_name):
    transcribe = boto3.client('transcribe')

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': answer_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        MediaSampleRateHertz=22050
    )

    t = TranscribeJob(name=job_name, status="In Progress")
    t.save()

def upload_to_s3(test_id, question_id, blob):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    file_name = str(test_id) + '-' + str(question_id) + '.wav'

    s3.Object(
        'testquestions-8853-5742-7832', file_name
    ).put(ACL='public-read', Body=blob)

    return file_name
