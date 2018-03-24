from __future__ import print_function
import time
import boto3
import urllib.request
import json

transcribe = boto3.client('transcribe')
job_name = "studewnsss41111111111111111"
job_uri = "https://s3.amazonaws.com/testquestions-8853-5742-7832/polly2.mp3"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='en-US',
    MediaSampleRateHertz=22050
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print('in progress....')
    time.sleep(5)
url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
response = urllib.request.urlopen(url)
data = response.read()
text = data.decode('utf-8')
d = json.loads(text)
print(d['results']['transcripts'][0]['transcript'])
