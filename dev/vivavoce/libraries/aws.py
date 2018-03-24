import boto3
import time

from vivavoce.models import TranscribeJob


AWS_ACCESS_KEY = 'AKIAIO2NRGA6M25NZLYQ'
AWS_SECRET_ACCESS_KEY = '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'

def upload_to_s3(blob):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    bucket = s3.Bucket('testquestions-8853-5742-7832')

    count = 0

    for object in bucket.objects.all():
        count += 1

    s3.Object('testquestions-8853-5742-7832', 'answer' + str(count) + '.wav').put(Body=blob)

    return 'answer' + str(count) + '.wav'

def transcribe(answer_uri):
    transcribe = boto3.client('transcribe')

    job_name = str("%.7f" % time.time())

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': answer_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        MediaSampleRateHertz=22050
    )

    t = TranscribeJob(name=job_name, status="In Progress")
    t.save()
