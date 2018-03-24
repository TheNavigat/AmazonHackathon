import boto3
import time
import urllib.request
import json

from vivavoce.models import TranscribeJob


AWS_ACCESS_KEY = 'AKIAIO2NRGA6M25NZLYQ'
AWS_SECRET_ACCESS_KEY = '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'

def transcribeFiles(quiz, questions):
    transcribe = boto3.client('transcribe')
    result = []
    i = 1
    while i <= 2:
        transcribe.start_transcription_job(
        TranscriptionJobName=str(quiz)+'-'+str(i),
        Media={'MediaFileUri': "https://s3.amazonaws.com/testquestions-8853-5742-7832/" + "question"+str(i-1)+".mp3"},
        MediaFormat='mp3',
        LanguageCode='en-US',
        MediaSampleRateHertz=22050
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=str(quiz)+'-'+str(i))
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print(i)
            time.sleep(5)
        url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = urllib.request.urlopen(url)
        data = response.read()
        text = data.decode('utf-8')
        d = json.loads(text)
        string = ''
        for sent in d['results']['transcripts']:
            string+=(sent['transcript'])
        result.append(string)
        i = i + 1
    print(result)
    return result

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
