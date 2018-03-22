import boto3
s3= boto3.resource('s3')

s3.Object('testquestions-8853-5742-7832', 'pollytest.mp3').put(Body=open('pollytest.mp3', 'rb'))