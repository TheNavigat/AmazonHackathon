from boto3 import  client
import boto3
import io
from contextlib import closing

x = ['Hello World','Goodbye','What is your name?']
s3= boto3.resource('s3')
polly = client("polly", 'us-east-1' )
i=0
for sample in x:
    response = polly.synthesize_speech( Text=sample, OutputFormat="mp3",VoiceId="Raveena")
    final = 'polly' + str(i) + '.mp3'
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            data = stream.read()
            fo = open(final, "wb")
            fo.write(data)
            fo.close()
    s3.Object('testquestions-8853-5742-7832', final).put(Body=open(final, 'rb'))

    i=i+1